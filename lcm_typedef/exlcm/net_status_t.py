"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class net_status_t(object):
    __slots__ = ["socket_status", "ip_address", "signal_str"]

    def __init__(self):
        self.socket_status = ""
        self.ip_address = ""
        self.signal_str = 0

    def encode(self):
        buf = BytesIO()
        buf.write(net_status_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        __socket_status_encoded = self.socket_status.encode('utf-8')
        buf.write(struct.pack('>I', len(__socket_status_encoded)+1))
        buf.write(__socket_status_encoded)
        buf.write(b"\0")
        __ip_address_encoded = self.ip_address.encode('utf-8')
        buf.write(struct.pack('>I', len(__ip_address_encoded)+1))
        buf.write(__ip_address_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">b", self.signal_str))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != net_status_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return net_status_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = net_status_t()
        __socket_status_len = struct.unpack('>I', buf.read(4))[0]
        self.socket_status = buf.read(__socket_status_len)[:-1].decode('utf-8', 'replace')
        __ip_address_len = struct.unpack('>I', buf.read(4))[0]
        self.ip_address = buf.read(__ip_address_len)[:-1].decode('utf-8', 'replace')
        self.signal_str = struct.unpack(">b", buf.read(1))[0]
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if net_status_t in parents: return 0
        tmphash = (0x4468f4d980903473) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if net_status_t._packed_fingerprint is None:
            net_status_t._packed_fingerprint = struct.pack(">Q", net_status_t._get_hash_recursive([]))
        return net_status_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

