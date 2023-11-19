from hash.Mask import Mask


class MurMur3:
    c1: int = 0xcc9e2d51
    c2: int = 0x1b873593

    @staticmethod
    def mur(a: int, h: int) -> int:
        a = Mask.uint32(MurMur3.c1 * a)
        a = Mask.uint32(a << 15 | a >> 17)
        a = Mask.uint32(MurMur3.c2 * a)
        h ^= a
        h = Mask.uint32(h << 13 | h >> 19)
        h = Mask.uint32(h * 5 + 0xe6546b64)
        return h
