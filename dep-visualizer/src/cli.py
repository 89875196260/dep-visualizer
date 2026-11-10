"""Модуль парсинга и валидации аргументов командной строки."""

import argparse
import os
import re
from urllib.parse import urlparse

MIN_DEPTH = 1
VERSION_PATTERN = r"^[a-zA-Z0-9._~+-]+$"
PKG_PATTERN = r"^[a-zA-Z0-9._+-]+$"


def validate_url_or_path(value: str, is_test: bool) -> str:
    """Проверяет корректность пути к файлу или URL репозитория."""
    if is_test:
        if not os.path.isfile(value):
            raise ValueError(f"Тестовый файл не найден: {value}")
        return value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(f"Некорректный URL репозитория: {value}")
    return value


def parse_args(argv: list[str] | None = None) -> dict:
    """Разбирает и валидирует параметры командной строки."""
    parser = argparse.ArgumentParser(
        description="Визуализатор зависимостей пакетов Alpine (apk)."
    )
    parser.add_argument(
        "-p", "--package", required=True, help="Имя пакета"
    )
    parser.add_argument(
        "-r", "--repo", required=True, help="URL репозитория или файл"
    )
    parser.add_argument(
        "-t", "--test-mode", action="store_true", help="Режим теста"
    )
    parser.add_argument(
        "-v", "--version", required=True, help="Версия пакета"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Выходной SVG-файл"
    )
    parser.add_argument(
        "-d", "--max-depth", type=int, required=True, help="Глубина"
    )
    args = parser.parse_args(argv)
    return validate_config(vars(args))


def validate_config(config: dict) -> dict:
    """Выполняет строгую проверку значений всех параметров."""
    if not re.match(PKG_PATTERN, config["package"]):
        raise ValueError("Недопустимое имя пакета.")
    if not re.match(VERSION_PATTERN, config["version"]):
        raise ValueError("Недопустимый формат версии пакета.")
    if config["max_depth"] < MIN_DEPTH:
        raise ValueError("Глубина анализа должна быть >= 1.")
    if not config["output"].lower().endswith(".svg"):
        raise ValueError("Выходной файл должен иметь расширение .svg.")
    validate_url_or_path(config["repo"], config["test_mode"])
    return config
