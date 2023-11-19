import struct

from hash.Mask import Mask


class Helper:
    @staticmethod
    def basic_rotate_32(val: int, shift: int) -> int:
        return Mask.uint32(val if shift == 0 else ((val >> shift) | (val << (32 - shift))))

    @staticmethod
    def rotate32(val: int, shift: int) -> int:
        return Helper.basic_rotate_32(val, shift)

    @staticmethod
    def fetch32(p: bytes) -> int:
        result = struct.unpack('<I', p[:4])[0]
        return result

    @staticmethod
    def f_mix(h: int) -> int:
        h ^= h >> 16
        h = Mask.uint32(h * 0x85ebca6b)
        h ^= h >> 13
        h = Mask.uint32(h * 0xc2b2ae35)
        h ^= h >> 16
        return h
