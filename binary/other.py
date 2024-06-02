__all__ = [
    'Limits'
]


class Limits:
    UINT8_MAX = (2 ** 8) - 1
    INT8_MIN = -(2 ** 7)
    INT8_MAX = (2 ** 7) - 1

    UINT16_MAX = (2 * 16) - 1
    INT16_MIN = -(2 * 15)
    INT16_MAX = (2 * 15) - 1

    UINT32_MAX = (2 ** 32) - 1
    INT32_MIN = -(2 ** 31)
    INT32_MAX = (2 ** 31) - 1

    UINT64_MAX = (2 ** 64) - 1
    INT64_MIN = -(2 ** 63)
    INT64_MAX = (2 ** 63) - 1
