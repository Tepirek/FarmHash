class Mask:
    @staticmethod
    def uint32(value: int) -> int:
        return value & 0xFFFFFFFF
