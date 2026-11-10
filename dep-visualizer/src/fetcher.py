"""Модуль загрузки и парсинга индекса пакетов Alpine Linux (APKINDEX)."""

import io
import re
import tarfile
import urllib.request

INDEX_FILENAME = "APKINDEX.tar.gz"
INNER_INDEX = "APKINDEX"
PREFIX_LEN = 2


def download_apkindex(repo_url: str) -> str:
    """Скачивает APKINDEX.tar.gz и извлекает содержимое APKINDEX."""
    url = f"{repo_url.rstrip('/')}/{INDEX_FILENAME}"
    with urllib.request.urlopen(url, timeout=15) as response:
        archive_bytes = response.read()
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
        member = tar.extractfile(INNER_INDEX)
        if member is None:
            raise RuntimeError("Файл APKINDEX не найден в архиве.")
        return member.read().decode("utf-8", errors="replace")


def parse_apkindex(raw_text: str) -> dict[tuple[str, str], list[str]]:
    """Парсит текст APKINDEX в словарь {(имя, версия): [зависимости]}."""
    packages: dict[tuple[str, str], list[str]] = {}
    for block in raw_text.strip().split("\n\n"):
        pkg, ver, deps = _parse_block(block)
        if pkg and ver:
            packages[(pkg, ver)] = deps
    return packages


def _parse_block(block: str) -> tuple[str, str, list[str]]:
    """Извлекает имя, версию и список прямых зависимостей из блока."""
    pkg, ver, deps = "", "", []
    for line in block.splitlines():
        if line.startswith("P:"):
            pkg = line[PREFIX_LEN:].strip()
        elif line.startswith("V:"):
            ver = line[PREFIX_LEN:].strip()
        elif line.startswith("D:"):
            deps = _clean_deps(line[PREFIX_LEN:].strip())
    return pkg, ver, deps


def _clean_deps(raw_deps: str) -> list[str]:
    """Очищает имена зависимостей от версионных ограничений."""
    cleaned: list[str] = []
    for item in raw_deps.split():
        if item.startswith("!"):
            continue
        parts = re.split(r"[<>=~]", item)
        name = parts[0].strip()  # Исправлено: берём первый элемент строки
        if name and name not in cleaned:
            cleaned.append(name)
    return cleaned


def get_direct_deps(
    packages: dict[tuple[str, str], list[str]], pkg: str, ver: str
) -> list[str]:
    """Возвращает прямые зависимости для заданного пакета и версии."""
    if (pkg, ver) not in packages:
        raise ValueError(f"Пакет {pkg} версии {ver} не найден в индексе.")
    return packages[(pkg, ver)]
