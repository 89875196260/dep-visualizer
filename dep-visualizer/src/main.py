"""Точка входа CLI-приложения (Этап 2)."""

import sys
from src.cli import parse_args
from src.fetcher import download_apkindex, get_direct_deps, parse_apkindex


def main() -> None:
    """Получает и выводит прямые зависимости указанного пакета."""
    try:
        config = parse_args()
        raw_index = download_apkindex(config["repo"])
        packages = parse_apkindex(raw_index)
        deps = get_direct_deps(
            packages, config["package"], config["version"]
        )
    except Exception as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        sys.exit(1)

    print(f"Прямые зависимости для {config['package']} ({config['version']}):")
    for dep in deps:
       print(f" - {dep}")


if __name__ == "__main__":
    main()
