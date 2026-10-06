#!/usr/bin/env python3
"""Minimal stdlib-only parquet footer reader (thrift compact protocol).
Verified against parquet-cpp-arrow 23.0.1 output (sealqa)."""
import struct

CTYPES = {0:'stop',1:'bool_true',2:'bool_false',3:'byte',4:'i16',5:'i32',6:'i64',7:'double',
          8:'binary',9:'list',10:'set',11:'map',12:'struct'}

class CReader:
    def __init__(self, buf):
        self.b = buf; self.p = 0
    def rb(self, n):
        r = self.b[self.p:self.p+n]; self.p += n
        if len(r) < n: raise EOFError('short read')
        return r
    def byte(self): return self.rb(1)[0]
    def varint(self):
        shift=0; out=0
        while True:
            bb=self.byte(); out |= (bb&0x7F)<<shift
            if not (bb&0x80): return out
            shift+=7
    def zigzag(self):
        v=self.varint(); return (v>>1)^-(v&1)
    def binary(self):
        n=self.varint(); return self.rb(n)
    def read_val(self, ctype, spec):
        if ctype=='bool_true': return True
        if ctype=='bool_false': return False
        if ctype=='byte': return struct.unpack('b', self.rb(1))[0]
        if ctype in ('i16','i32','i64'): return self.zigzag()
        if ctype=='double': return struct.unpack('<d', self.rb(8))[0]
        if ctype=='binary': return self.binary()
        if ctype=='struct': return self.read_struct(spec)
        if ctype in ('list','set'): return self.read_list(spec)
        raise ValueError('ctype '+str(ctype))
    def read_struct(self, spec):
        out={}; last=0
        rev = {v:k for k,v in spec.items() if isinstance(v,int)} if spec else {}
        submap = (spec or {}).get('_sub', {})
        while True:
            bb=self.byte()
            if bb==0: break
            delta=(bb>>4)&0xF; ctn=bb&0xF
            if delta==0xF: last+=self.zigzag()
            else: last+=delta
            fid=last
            if ctn==0xF: ctn=CTYPES[self.byte()]
            else: ctn=CTYPES[ctn]
            out[rev.get(fid, f'field_{fid}')]=self.read_val(ctn, submap.get(fid))
        return out
    def read_list(self, spec):
        # compact list header: single byte, size in HIGH nibble, elem type in LOW nibble
        b=self.byte(); elem_ctype=CTYPES[b&0xF]; n=b>>4
        if n==0xF: n=self.varint()
        sub=(spec or {}).get('_elem')
        return [self.read_val(elem_ctype, sub) for _ in range(n)]

# Field-id specs per parquet.thrift (name -> field id).
# NOTE: SchemaElement order is type=1, type_length=2, repetition_type=3, name=4 (not name first!).
LT_SPEC={'STRING':8,'MAP':9,'LIST':10,'ENUM':11,'DECIMAL':12,'DATE':13,'TIME':14,'TIMESTAMP':15,
 'INTEGER':16,'UNKNOWN':17,'JSON':18,'BSON':19,'UUID':20}
SE_SPEC={'type':1,'type_length':2,'repetition_type':3,'name':4,'num_children':5,'converted_type':6,
 'scale':7,'precision':8,'field_id':9,'logicalType':10,'_sub':{10:LT_SPEC}}
RG_SPEC={'columns':1,'total_byte_size':2,'num_rows':3,'sorting_columns':4,'file_offset':5,
 'total_compressed_size':6,'ordinal':7}
CC_SPEC={'file_path':1,'file_offset':2,'meta_data':3,'offset_index_offset':4,'offset_index_length':5,
 'bloom_filter_offset':6,'bloom_filter_length':7,'_sub':{}}
# NOTE: ColumnMetaData order is type=1, encodings=2, path_in_schema=3, codec=4, num_values=5...
CCM_SPEC={'type':1,'encodings':2,'path_in_schema':3,'codec':4,'num_values':5,'total_uncompressed_size':6,
 'total_compressed_size':7,'key_value_metadata':8,'data_page_offset':9,'index_page_offset':10,
 'dictionary_page_offset':11,'statistics':12,'encoding_stats':13,'bloom_filter_offset':14,
 'bloom_filter_length':15,'geospatial_statistics':16,
 '_sub':{3:{'_elem':None},2:{'_elem':None},13:{'_elem':None}}}
CC_SPEC['_sub']={3:CCM_SPEC}
RG_SPEC['_sub']={1:{'_elem':CC_SPEC}}
FMD_SPEC={'version':1,'schema':2,'num_rows':3,'row_groups':4,'key_value_metadata':5,
 'created_by':6,'column_orders':7,'file_path':8,'encryption_algorithm':9,'footer_signing_key_metadata':10,
 '_sub':{2:{'_elem':SE_SPEC},4:{'_elem':RG_SPEC}}}

ENCODINGS={0:'PLAIN',1:'PLAIN_DICTIONARY',2:'RLE',3:'BIT_PACKED',4:'DELTA_BINARY_PACKED',
           5:'DELTA_LENGTH_BYTE_ARRAY',6:'DELTA_BYTE_ARRAY',7:'RLE_DICTIONARY',8:'BYTE_STREAM_SPLIT'}
CODECS={0:'UNCOMPRESSED',1:'SNAPPY',2:'GZIP',3:'LZO',4:'BROTLI',5:'LZ4',6:'ZSTD',7:'LZ4_RAW'}

def parse_footer(buf):
    if buf[:4]!=b'PAR1' or buf[-4:]!=b'PAR1': raise ValueError('bad magic')
    (mlen,)=struct.unpack('<i', buf[-8:-4])
    return CReader(buf[-8-mlen:-8]).read_struct(FMD_SPEC)

def leaf_columns(md):
    """Return [(path_tuple, max_rep, max_def)] for each leaf column. Root not counted."""
    schema=md['schema']; leaves=[]
    def walk(i, rep, dfn, prefix):
        se=schema[i]
        name=se['name'].decode() if isinstance(se['name'],bytes) else se['name']
        rt=se.get('repetition_type')  # 0=REQUIRED 1=OPTIONAL 2=REPEATED
        if rt==1: dfn+=1
        elif rt==2: rep+=1; dfn+=1
        nc=se.get('num_children')
        if nc:
            j=i+1
            for _ in range(nc): j=walk(j,rep,dfn,prefix+(name,))
            return j
        leaves.append((prefix+(name,),rep,dfn))
        return i+1
    # start at root's children (root itself contributes no rep/def)
    root=schema[0]; j=1
    for _ in range(root.get('num_children',0)): j=walk(j,0,0,())
    return leaves
