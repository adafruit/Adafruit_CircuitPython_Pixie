# SPDX-FileCopyrightText: 2016 Damien P. George for Adafruit Industries
# SPDX-FileCopyrightText: 2018 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pixie` - Pixie LED driver
====================================================
* Author(s): Damien P. George, Limor Fried, Kattni Rembor
"""

import time
import math

try:
    from typing import Union, Tuple
    from busio import UART
except ImportError:
    pass

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Pixie.git"


class Pixie:
    """
    PIxie LEDs.

    :param busio.UART uart: The UART object.
    :param int n: The number of Pixies in the chain.
    :param float brightness: Brightness of the pixels between 0.0 and 1.0.
    :param bool auto_write: True if the Pixies should immediately change when
        set. If False, `show` must be called explicitly.

    Example for two Pixie LEDs chained:

    .. code_block::python

        import time
        import board
        import busio
        import adafruit_pixie

        uart = busio.UART(board.TX, rx=None, baudrate=115200)
        pixies = adafruit_pixie.Pixie(uart, 2, brightness=0.5)

        # Colors can be either tuples or integer representing RGB values
        # red = (255, 0, 0)
        # green = 0x00FF00

        while True:
            pixies.fill((255, 0, 0))
            time.sleep(1)
            pixies[0] = (0, 255, 0)
            pixies[1] = (0, 0, 255)
            time.sleep(1)
    """

    def __init__(
        self, uart: UART, n: int, *, brightness: float = 1.0, auto_write: bool = True
    ) -> None:
        self._uart = uart
        self._n = n
        self._buf = bytearray(self._n * 3)
        # Set auto_write to False temporarily so brightness setter does _not_
        # call show() while in __init__.
        self.auto_write = False
        self._brightness = brightness
        self.auto_write = auto_write

    def _set_item(self, index: int, value: Union[int, Tuple[int, int, int]]) -> None:
        if index < 0:
            index += len(self)
        if index >= self._n or index < 0:
            raise IndexError
        offset = index * 3
        r = 0
        g = 0
        b = 0
        if isinstance(value, int):
            r = value >> 16
            g = (value >> 8) & 0xFF
            b = value & 0xFF
        elif len(value) == 3:
            r, g, b = value
        self._buf[offset + 0] = r
        self._buf[offset + 1] = g
        self._buf[offset + 2] = b

    def __setitem__(
        self, index: Union[int, slice], val: Union[int, Tuple[int, int, int]]
    ) -> None:
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self._buf) // 3)
            length = stop - start
            if step != 0:
                length = math.ceil(length / step)
            if len(val) != length:
                raise ValueError("Slice and input sequence size do not match.")
            for val_i, in_i in enumerate(range(start, stop, step)):
                self._set_item(in_i, val[val_i])
        else:
            self._set_item(index, val)

        if self.auto_write:
            self.show()

    def __len__(self):
        return len(self._buf) // 3

    @property
    def brightness(self) -> float:
        """Overall brightness of the pixel"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: float) -> None:
        self._brightness = min(max(brightness, 0.0), 1.0)
        if self.auto_write:
            self.show()

    def fill(self, color: Union[int, Tuple[int, int, int]]) -> None:
        """Colors all pixels the given color.

        :param color: Either a tuple or integer representing RGB values, such as
            (255, 0, 0) or 0xFF0000
        :type color: int|(int, int, int)
        """
        auto_write = self.auto_write
        self.auto_write = False
        for i in range(self._n):
            self[i] = color
        if auto_write:
            self.show()
        self.auto_write = auto_write

    def show(self) -> None:
        """
        Shows the new colors on the pixels themselves if they haven't already
        been autowritten.
        """
        self._uart.write(bytes([int(i * self.brightness) for i in self._buf]))
        time.sleep(0.005)
