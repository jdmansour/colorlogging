import logging
from . import ColorPicker
import tornado.log


class ColorTornadoLogFormatter(tornado.log.LogFormatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colorpicker = ColorPicker()

    def format(self, record: logging.LogRecord):
        rgb = self.colorpicker.get_color_rgb(record.module)
        rgbstr = ";".join(str(int(c * 255)) for c in rgb)
        record.name = "\x1B[38;2;%sm" % rgbstr + record.name + "\x1B[0m"
        record.module = "\x1B[38;2;%sm" % rgbstr + record.module + "\x1B[0m"
        return super().format(record)
