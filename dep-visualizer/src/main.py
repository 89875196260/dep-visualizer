"""Точка входа CLI-приложения (Этап 1)."""

import sys
from src.cli import parse_args


def main() -> None:
    """Запускает разбор конфигурации и выводит параметры."""
    try:
        config = parse_args()
    except ValueError as err:
        print(f"Ошибка конфигурации: {err}", file=sys.stderr)
        sys.exit(1)

    for key, value in config.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
