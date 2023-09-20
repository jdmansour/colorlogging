"""
Colorizes Python's logging output depending on the module name.
"""

__version__ = "0.1.0"

import colorsys
import logging
import random


class ColoredFormatter(logging.Formatter):
    def __init__(self, base_formatter: logging.Formatter):
        self.base_formatter = base_formatter
        self.colorpicker = ColorPicker()

    def format(self, record: logging.LogRecord):
        # bright = tmp % 2
        rgb = self.colorpicker.get_color_rgb(record.name)
        rgbstr = ";".join(str(int(c * 255)) for c in rgb)
        record.name = "\x1B[38;2;%sm" % rgbstr + record.name + "\x1B[0m"
        record.module = "\x1B[38;2;%sm" % rgbstr + record.module + "\x1B[0m"
        # record.name = '\x1B[31m' + record.name + '\x1B[0m'
        # print("Record: %s" % record.name, file=sys.stderr)
        # print("used_hues: %s" % self.used_hues, file=sys.stderr)
        return self.base_formatter.format(record)


class ColorPicker:
    def __init__(self):
        self.used_hues = {}

    def get_color_rgb(self, name: str):
        try:
            hue = self.used_hues[name]
        except KeyError:
            tmp = random.Random(name).randint(0, 31)
            hue = (tmp % 32) / 32
            while hue in self.used_hues.values() and len(self.used_hues) < 32:
                tmp += 1
                hue = (tmp % 32) / 32

        self.used_hues[name] = hue
        lightness = 0.5
        return colorsys.hls_to_rgb(hue, lightness, 0.6)
