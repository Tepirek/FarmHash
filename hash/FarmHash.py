from hash.Helper import Helper
from hash.Mask import Mask
from hash.MurMur3 import MurMur3


class FarmHash:
    @staticmethod
    def hash32(text: str) -> int:
        l: int = len(text)

        if l <= 4:
            return FarmHash.hash_32_len_0_to_4(text, l)
        if l <= 12:
            return FarmHash.hash_32_len_5_to_12(bytes(text, 'utf-8'), l)
        if l <= 24:
            return FarmHash.hash_32_len_13_to_24(bytes(text, 'utf-8'), l)

        s = bytes(text, 'utf-8')
        h = l
        g = MurMur3.c1 * l
        f = g

        a0 = Mask.uint32(Helper.rotate32(Mask.uint32(Helper.fetch32(s[l - 4:]) * MurMur3.c1), 17) * MurMur3.c2)
        a1 = Mask.uint32(Helper.rotate32(Mask.uint32(Helper.fetch32(s[l - 8:]) * MurMur3.c1), 17) * MurMur3.c2)
        a2 = Mask.uint32(Helper.rotate32(Mask.uint32(Helper.fetch32(s[l - 16:]) * MurMur3.c1), 17) * MurMur3.c2)
        a3 = Mask.uint32(Helper.rotate32(Mask.uint32(Helper.fetch32(s[l - 12:]) * MurMur3.c1), 17) * MurMur3.c2)
        a4 = Mask.uint32(Helper.rotate32(Mask.uint32(Helper.fetch32(s[l - 20:]) * MurMur3.c1), 17) * MurMur3.c2)

        h = Mask.uint32(h ^ a0)
        h = Helper.rotate32(h, 19)
        h = Mask.uint32(h * 5 + 0xe6546b64)
        h = Mask.uint32(h ^ a2)
        h = Helper.rotate32(h, 19)
        h = Mask.uint32(h * 5 + 0xe6546b64)

        g = Mask.uint32(g ^ a1)
        g = Helper.rotate32(g, 19)
        g = Mask.uint32(g * 5 + 0xe6546b64)
        g = Mask.uint32(g ^ a3)
        g = Helper.rotate32(g, 19)
        g = Mask.uint32(g * 5 + 0xe6546b64)

        f = Mask.uint32(f + a4)
        f = Helper.rotate32(f, 19) + 113
        iters = int((l - 1) / 20)

        while True:
            a = Helper.fetch32(s)
            b = Helper.fetch32(s[4:])
            c = Helper.fetch32(s[8:])
            d = Helper.fetch32(s[12:])
            e = Helper.fetch32(s[16:])
            h = Mask.uint32(h + a)
            g = Mask.uint32(g + b)
            f = Mask.uint32(f + c)
            h = Mask.uint32(MurMur3.mur(d, h) + e)
            g = Mask.uint32(MurMur3.mur(c, g) + a)
            f = Mask.uint32(MurMur3.mur(b + e * MurMur3.c1, f) + d)
            f = Mask.uint32(f + g)
            g = Mask.uint32(g + f)
            s = s[20:]
            iters -= 1
            if iters != 0:
                continue
            else:
                break
        g = Mask.uint32(Helper.rotate32(g, 11) * MurMur3.c1)
        g = Mask.uint32(Helper.rotate32(g, 17) * MurMur3.c1)
        f = Mask.uint32(Helper.rotate32(f, 11) * MurMur3.c1)
        f = Mask.uint32(Helper.rotate32(f, 17) * MurMur3.c1)
        h = Helper.rotate32(h + g, 19)
        h = Mask.uint32(h * 5 + 0xe6546b64)
        h = Mask.uint32(Helper.rotate32(h, 17) * MurMur3.c1)
        h = Helper.rotate32(h + f, 19)
        h = Mask.uint32(h * 5 + 0xe6546b64)
        h = Mask.uint32(Helper.rotate32(h, 17) * MurMur3.c1)
        return h

    @staticmethod
    def hash_32_len_0_to_4(s: str, length: int) -> int:
        b: int = 0
        c: int = 9
        for i in range(length):
            v = ord(s[i])
            b = Mask.uint32(b * MurMur3.c1 + v)
            c ^= b
        return Helper.f_mix(MurMur3.mur(b, MurMur3.mur(length, c)))

    @staticmethod
    def hash_32_len_5_to_12(s: bytes, length: int) -> int:
        a: int = length
        b: int = length * 5
        c: int = 9
        d: int = b
        a = Mask.uint32(a + Helper.fetch32(s))
        b = Mask.uint32(b + Helper.fetch32(s[length - 4:]))
        shift: int = (length >> 1) & 4
        c = Mask.uint32(c + Helper.fetch32(s[shift:shift + 4]))
        return Helper.f_mix(MurMur3.mur(c, MurMur3.mur(b, MurMur3.mur(a, d))))

    @staticmethod
    def hash_32_len_13_to_24(s: bytes, length: int, seed: int = 0) -> int:
        a = Helper.fetch32(s[-4 + (length // 2):])
        b = Helper.fetch32(s[4:])
        c = Helper.fetch32(s[length - 8:])
        d = Helper.fetch32(s[length // 2:])
        e = Helper.fetch32(s)
        f = Helper.fetch32(s[length - 4:])
        h = Mask.uint32(d * MurMur3.c1 + length + seed)
        a = Mask.uint32(Helper.rotate32(a, 12) + f)
        h = Mask.uint32(MurMur3.mur(c, h) + a)
        a = Mask.uint32(Helper.rotate32(a, 3) + c)
        h = Mask.uint32(MurMur3.mur(e, h) + a)
        a = Mask.uint32(Helper.rotate32(a + f, 12) + d)
        h = Mask.uint32(MurMur3.mur(Mask.uint32(b ^ seed), h) + a)
        return Helper.f_mix(h)
