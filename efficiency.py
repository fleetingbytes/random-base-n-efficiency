#!/usr/bin/env python

from sys import argv
from math import ceil
from dataclasses import dataclass, field, InitVar
from typing import ClassVar


@dataclass
class Efficiency:
    efficiency: float = field(init=False)
    bits: int = field(init=False)
    bytes: int = field(init=False)
    residual_bits: int = field(init=False)
    wasted_bits_per_digit: float = field(init=False)
    base: InitVar[int]
    digits: InitVar[int]
    formatting: ClassVar[dict[str, str]]

    def __post_init__(self, base: int, digits: int):
        biggest_needed = base ** digits - 1
        self.bits = int.bit_length(biggest_needed)
        self.bytes = int(ceil(float(self.bits)/8))
        self.residual_bits = self.bytes * 8 - self.bits
        biggest_possible = 2 ** self.bits - 1
        self.efficiency = biggest_needed / biggest_possible
        probability_of_waste = 1 - (base ** digits / 2 ** self.bits)
        self.wasted_bits_per_digit = probability_of_waste * self.bits / digits

for digits in range(1, 2049):
    base = int(argv[1])
    e = Efficiency(base, digits)
    if e.efficiency < 0.999:
        continue
    print(f"{digits:>4} {e.efficiency:.4f} {e.bits:>4} {e.bytes:>3} {e.residual_bits} {e.wasted_bits_per_digit:.6f} wasted bits/digit")
    if e.efficiency >= 1.0:
        break

def print_header():
    pass
