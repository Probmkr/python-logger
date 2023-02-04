import json
import os
from dotenv import load_dotenv
from logvar import *
from datetime import datetime

load_dotenv()
LOG_LEVEL = int(os.getenv("LOG_LEVEL", 3))
USE_LOG_WHITE_LIST = bool(os.getenv("IF_LOG_WHITE_LIST", False))
LOG_WHITE_LIST = json.dumps(os.getenv("LOG_WHITE_LIST", []))
LOG_BLACK_LIST = json.dumps(os.getenv("LOG_BLACK_LIST", []))

class FMTOut:
    def color(text: str, color: ConsoleColor, *, reset = True):
        return "{}{}{}".format(
            color.value,
            text,
            CC.RESET.value if reset else ""
        )

    def label(text: str, label: str):
        text_splitted = text.splitlines(keepends=True)
        return "".join(map(lambda text_piece: "{}{}".format(label, text_piece), text_splitted))

class Logger:
    level: LogLevel

    def __init__(self, level: LogLevel | int = LOG_LEVEL):
        self.level = LL(level)

    def log(self, msg: str, level: LogLevel | int = None, category: str = "others"):
        if level == None:
            level = LL(self.level)
        else:
            level = LL(level)
        if level.value > self.level.value:
            return
        label = "{:17} [{}] [{:12}]: ".format(datetime.now().strftime("%y-%m-%d %H:%m:%S"), level.name[:3], category)
        print(FMTOut.color(FMTOut.label(str(msg), label), LCL[level.name].value))

    def fatal(self, msg: str, category: str = "others"):
        self.log(msg, 1, category)

    def error(self, msg: str, category: str = "others"):
        self.log(msg, 2, category)

    def warn(self, msg: str, category: str = "others"):
        self.log(msg, 3, category)

    def warning(self, msg: str, category: str = "others"):
        self.log(msg, 3, category)

    def info(self, msg: str, category: str = "others"):
        self.log(msg, 4, category)

    def debug(self, msg: str, category: str = "others"):
        self.log(msg, 5, category)

    def trace(self, msg: str, category: str = "others"):
        self.log(msg, 6, category)
