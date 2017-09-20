"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class eng_control_t(object):
    __slots__ = ["eng_mode", "start_ignite", "martin"]

    def __init__(self):
        self.eng_mode = ""
        self.start_ignite = False
        self.martin = False

    def encode(self):
        buf = BytesIO()
        buf.write(eng_control_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        __eng_mode_encoded = self.eng_mode.encode('utf-8')
        buf.write(struct.pack('>I', len(__eng_mode_encoded)+1))
        buf.write(__eng_mode_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">bb", self.start_ignite, self.martin))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != eng_control_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return eng_control_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = eng_control_t()
        __eng_mode_len = struct.unpack('>I', buf.read(4))[0]
        self.eng_mode = buf.read(__eng_mode_len)[:-1].decode('utf-8', 'replace')
        self.start_ignite = bool(struct.unpack('b', buf.read(1))[0])
        self.martin = bool(struct.unpack('b', buf.read(1))[0])
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if eng_control_t in parents: return 0
        tmphash = (0xee78add5a62c4e27) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if eng_control_t._packed_fingerprint is None:
            eng_control_t._packed_fingerprint = struct.pack(">Q", eng_control_t._get_hash_recursive([]))
        return eng_control_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

