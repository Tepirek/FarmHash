import sys
import timeit

import farmhash

from console import Writer
from hash.FarmHash import FarmHash

test_cases: [str] = [
    "a.D  asdd \\nasdb",
    "abc",
    "test",
    "john doe",
    "!@#$%^&*()_+",
    "konstantynopolitańczykowianeczka",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
]

test_cases_files: [str] = [
    'lorem_small.txt',
    'lorem_big.txt',
]


def run_test_case(message: str) -> None:
    print(f"{''.join(['-' for _ in range(96)])}")
    preview: str = f'{message[:24]}[...]{message[-24:]}' if len(message) > 48 else message
    print(f'Testing input "{preview}" of length {len(message)}.')

    def func() -> None:
        original_result: int = farmhash.hash32(message)
        custom_result: int = FarmHash.hash32(message)
        print(f"Numeric: {hex(original_result)} =?= {hex(custom_result)}")
        print(f"Hexadecimal: {original_result} =?= {custom_result}")
        if original_result == custom_result:
            Writer.success('Passed!', before='Result: ')
        else:
            Writer.error('Failed!', before='Result: ')

    elapsed_time = timeit.timeit(stmt=func, number=1)
    Writer.info('%.10f seconds' % elapsed_time, before='Elapsed time: ')


def run_tests() -> None:
    print("Running tests...")

    for message in test_cases:
        run_test_case(message)

    for filename in test_cases_files:
        with open(f'files/{filename}') as f:
            lines = f.readlines()
            lines = ''.join(lines)
            run_test_case(lines)


def main() -> None:
    message: str = input('Enter your message: ')
    run_test_case(message)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        run_tests()
    else:
        main()
