import logging
from logger.color_stream import ColorStream


class AppLogger():
    def __init__(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(ColorStream())
        console_stream = logging.getLogger('console_stream')
        console_stream.addHandler(console_handler)
        console_stream.setLevel(logging.DEBUG)
        self.logger = console_stream
