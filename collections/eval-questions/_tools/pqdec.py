#!/usr/bin/env python3
"""Decode parquet data pages (stdlib only).

Empirical notes (parquet-cpp-arrow 23.0.1, sealqa):
- Pages are SNAPPY-compressed (codec=1); decompress before parsing.
- Data page header's `encoding` / level-encoding enums are unreliable
  (e.g. claims BYTE_STREAM_SPLIT for what is structurally RLE_DICTIONARY,
  BIT_PACKED for RLE levels). Decode by structure instead:
  levels are always [int32 LE length][RLE/bit-packed hybrid]; a dictionary
  page present => values are [1-byte bit width][RLE hybrid indices].
"""
import struct, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from pqread import CReader, parse_footer, leaf_columns
from snappy import snappy_decompress

PH_SPEC={'type':1,'uncompressed_page_size':2,'compressed_page_size':3,'crc':4,
 'data_page_header':5,'index_page_header':6,'dictionary_page_header':7,'data_page_header_v2':8}
DPH_SPEC={'num_values':1,'encoding':2,'definition_level_encoding':3,'repetition_level_encoding':4,'statistics':5}
DICTPH_SPEC={'num_values':1,'encoding':2,'is_sorted':3}
PH_SPEC['_sub']={5:DPH_SPEC,7:DICTPH_SPEC}
PAGE_TYPES={0:'DATA_PAGE',1:'INDEX_PAGE',2:'DICTIONARY_PAGE',3:'DATA_PAGE_V2'}

def read_page_header(buf, off):
    r=CReader(buf[off:])
    ph=r.read_struct(PH_SPEC)
    return ph, off+r.p

def bit_width_for_max(m):
    b=0
    while (1<<b)<=m: b+=1
    return b

def rle_hybrid(data, bit_width, count):
    out=[]; p=0
    while len(out)<count:
        shift=0; h=0
        while True:
            b=data[p]; p+=1; h|=(b&0x7F)<<shift
            if not (b&0x80): break
            shift+=7
        if h&1==0:
            run=h>>1
            nbytes=max(1,(bit_width+7)//8)
            v=int.from_bytes(data[p:p+nbytes],'little'); p+=nbytes
            v &= (1<<bit_width)-1 if bit_width<64 else (1<<bit_width)-1
            out.extend([v]*run)
        else:
            ngroups=(h>>1); total=ngroups*8
            nbytes=(total*bit_width+7)//8
            bits=int.from_bytes(data[p:p+nbytes],'little'); p+=nbytes
            mask=(1<<bit_width)-1
            for i in range(total):
                out.append((bits>>(i*bit_width))&mask)
                if len(out)>=count: break
    return out[:count]

def decode_levels_section(data, dp, max_level, num_values):
    (ln,)=struct.unpack('<i', data[dp:dp+4]); dp+=4
    lv=rle_hybrid(data[dp:dp+ln], bit_width_for_max(max_level), num_values)
    return lv, dp+ln

def decode_plain_bytearray(data, n):
    out=[]; p=0
    for _ in range(n):
        (ln,)=struct.unpack('<i', data[p:p+4]); p+=4
        out.append(data[p:p+ln]); p+=ln
    return out

def maybe_decompress(raw, codec, uncompressed_size):
    if codec==0: return raw
    if codec==1:
        # NOTE: snappy output can equal input size; always try, fall back to raw
        try:
            u=snappy_decompress(raw)
            if len(u)==uncompressed_size: return u
        except Exception:
            pass
        return raw
    raise ValueError(f'unsupported codec {codec}')

def decode_column(path, col_path):
    """Return list of rows; repeated columns become list-of-lists, optional scalars may be None."""
    buf=open(path,'rb').read()
    md=parse_footer(buf)
    leaves={lp:(r,d) for lp,r,d in leaf_columns(md)}
    max_rep,max_def=leaves[col_path]
    rows=[]
    for rg in md['row_groups']:
        for cc in rg['columns']:
            m=cc['meta_data']
            if tuple(x.decode() for x in m['path_in_schema'])!=col_path: continue
            codec=m.get('codec',0)
            dictionary=None
            doff=m.get('dictionary_page_offset')
            if doff is not None:
                ph,p=read_page_header(buf,doff)
                assert PAGE_TYPES[ph['type']]=='DICTIONARY_PAGE'
                raw=buf[p:p+ph['compressed_page_size']]
                u=maybe_decompress(raw,codec,ph['uncompressed_page_size'])
                dictionary=decode_plain_bytearray(u, ph['dictionary_page_header']['num_values'])
            off=m['data_page_offset']
            target=m['num_values']; got=0
            while got<target:
                ph,p=read_page_header(buf,off)
                assert PAGE_TYPES[ph['type']]=='DATA_PAGE', (PAGE_TYPES[ph['type']],col_path)
                dh=ph['data_page_header']; nv=dh['num_values']
                raw=buf[p:p+ph['compressed_page_size']]
                data=maybe_decompress(raw,codec,ph['uncompressed_page_size'])
                dp=0
                rep_lv=def_lv=None
                if max_rep>0: rep_lv,dp=decode_levels_section(data,dp,max_rep,nv)
                if max_def>0: def_lv,dp=decode_levels_section(data,dp,max_def,nv)
                if dictionary is not None:
                    bw=data[dp]; dp+=1
                    n_idx=sum(1 for d in def_lv if d==max_def) if def_lv is not None else nv
                    idx=rle_hybrid(data[dp:],bw,n_idx)
                    vals=[dictionary[i] for i in idx]
                else:
                    n_v=sum(1 for d in def_lv if d==max_def) if def_lv is not None else nv
                    vals=decode_plain_bytearray(data[dp:],n_v)
                # reassemble rows
                if max_rep==0:
                    if def_lv is None:
                        rows.extend(vals)
                    else:
                        it=iter(vals)
                        rows.extend(next(it) if d==max_def else None for d in def_lv)
                else:
                    it=iter(vals); cur=None
                    for r_,d_ in zip(rep_lv,def_lv):
                        if r_==0:
                            cur=[]; rows.append(cur)
                        if d_==max_def:
                            cur.append(next(it))
                        # def < max_def: null/empty slot, no value consumed
                got+=nv
                off=p+ph['compressed_page_size']
    return rows

if __name__=='__main__':
    path,col=sys.argv[1],tuple(sys.argv[2].split(','))
    rows=decode_column(path,col)
    print('rows:',len(rows))
    for r in rows[:3]:
        print(repr(r)[:200])
