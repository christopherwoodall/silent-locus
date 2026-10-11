#!/usr/bin/env python3
"""Pure-python snappy raw-block decompressor (as used inside parquet pages).
No framing, no CRC — just the raw block format: varint uncompressed-length,
then literal / copy tags."""

def snappy_decompress(data: bytes) -> bytes:
    p = 0
    shift = 0; ulen = 0
    while True:
        b = data[p]; p += 1
        ulen |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
    out = bytearray()
    while p < len(data):
        tag = data[p]; p += 1
        typ = tag & 0x03
        if typ == 0:  # literal
            ln = tag >> 2
            if ln < 60:
                ln += 1
            else:
                nb = ln - 59
                ln = int.from_bytes(data[p:p+nb], 'little') + 1
                p += nb
            out += data[p:p+ln]; p += ln
        else:
            if typ == 1:  # copy, 1-byte offset
                ln = 4 + ((tag >> 2) & 0x7)
                off = ((tag >> 5) << 8) | data[p]; p += 1
            elif typ == 2:  # copy, 2-byte offset
                ln = 1 + (tag >> 2)
                off = int.from_bytes(data[p:p+2], 'little'); p += 2
            else:  # copy, 4-byte offset
                ln = 1 + (tag >> 2)
                off = int.from_bytes(data[p:p+4], 'little'); p += 4
            start = len(out) - off
            for i in range(ln):
                out.append(out[start + i])
    if len(out) != ulen:
        raise ValueError(f'snappy length mismatch: got {len(out)} want {ulen}')
    return bytes(out)
