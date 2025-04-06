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
    digits: int
    header_string: ClassVar[str] = " ".join((
        "DGTS",
        "EFFCNCY",
        "BITS",
        "BYTS",
        "R",
        "WASTE[bits/dgt]",
    ))
    row_string: ClassVar[str] = " ".join((
        "{:{digits_alignment}{digits_width}}",
        "{:.{efficiency_precision}{efficiency_notation}}",
        "{:{bits_alignment}{bits_width}}",
        "{:{bytes_alignment}{bytes_width}}",
        "{}",
        "{:.{wasted_bits_per_digit_precision}{wasted_bits_per_digit_notation}}",
    ))
    format_params: ClassVar[dict[str, int | str]] = {
        "digits_alignment": ">",
        "digits_width": 4,
        "efficiency_precision": 5,
        "efficiency_notation": "f",
        "bits_alignment": ">",
        "bits_width": 4,
        "bytes_alignment": ">",
        "bytes_width": 4,
        "wasted_bits_per_digit_precision": 6,
        "wasted_bits_per_digit_notation": "f",
    }

    def __post_init__(self, base: int):
        biggest_needed = base ** self.digits - 1
        self.bits = int.bit_length(biggest_needed)
        self.bytes = int(ceil(float(self.bits)/8))
        self.residual_bits = self.bytes * 8 - self.bits
        biggest_possible = 2 ** self.bits - 1
        self.efficiency = biggest_needed / biggest_possible
        probability_of_waste = 1 - (base ** self.digits / 2 ** self.bits)
        self.wasted_bits_per_digit = probability_of_waste * self.bits / self.digits

    @classmethod
    def print_header(cls) -> None:
        print(cls.header_string)

    def print_row(self) -> None:
        print(self.__class__.row_string.format(
                self.digits,
                self.efficiency,
                self.bits,
                self.bytes,
                self.residual_bits,
                self.wasted_bits_per_digit,
                **self.__class__.format_params
            )
        )


Efficiency.print_header()
for digits in range(1, 2049):
    base = int(argv[1])
    e = Efficiency(base, digits)
    if e.efficiency < 0.999:
        continue
    e.print_row()
    if e.efficiency >= 1.0:
        break
