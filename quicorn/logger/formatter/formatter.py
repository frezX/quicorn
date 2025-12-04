from typing import Any

from quicorn.logger.formatter import Colors


class StrFormatter:
    @classmethod
    def set_color(cls, value: Any, color: Colors = Colors.WHITE) -> str:
        return f'<{color}>{value}</{color}>'

    @classmethod
    def dict_to_color_str(
        cls,
        dictionary: dict,
        key_color: Colors = Colors.BLUE,
        value_color: Colors = Colors.WHITE,
        hidden_keys: list[str] | None = None,
    ) -> str:
        string: str = '{'
        for key, value in dictionary.items():
            if isinstance(value, str):
                value: str = f'"{value}"'
            elif isinstance(value, dict):
                try:
                    value: str = cls.dict_to_color_str(
                        dictionary=value, key_color=key_color, value_color=value_color, hidden_keys=hidden_keys
                    )
                except RecursionError:
                    value: str = '...'
            else:
                value: str = str(value)
            if hidden_keys and key in hidden_keys:
                colored_value: str = cls.set_color(value=r'\<hidden>', color=Colors.PURPLE)
            else:
                colored_value: str = cls.set_color(value=value, color=value_color)
            string += f'{cls.set_color(value=key, color=key_color)}: {colored_value}, '
        return string.rstrip(', ') + '}'

    @classmethod
    def join(cls, *data: str, separator: str = ' | ', color: Colors = Colors.LIGHT_RED) -> str:
        return f'{cls.set_color(value=separator, color=color)}'.join(data)

    @classmethod
    def escape(cls, _text: str) -> str:
        return _text.replace('<', r'\<')
