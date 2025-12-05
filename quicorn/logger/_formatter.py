from typing import Any
from enum import StrEnum


class Colors(StrEnum):
    BLACK = 'k'
    WHITE = 'w'
    RED = 'r'
    GREEN = 'g'
    BLUE = 'e'
    CAYAN = 'c'
    MAGENTA = 'm'
    YELLOW = 'fg #ffff00'
    ORANGE = 'fg #eca71e'
    PURPLE = 'fg #9b4baf'

    LIGHT_RED = 'lr'


class StrFormatter:
    @staticmethod
    def escape(_obj: Any) -> str:
        if not isinstance(_obj, str):
            _obj: str = repr(_obj)
        return _obj.replace('<', r'\<')

    @staticmethod
    def set_color(value: Any, color: Colors = Colors.WHITE) -> str:
        return f'<{color}>{value}</{color}>'

    @classmethod
    def join(cls, *data: str, separator: str = ' | ', color: Colors = Colors.LIGHT_RED) -> str:
        return f'{cls.set_color(value=separator, color=color)}'.join(data)
