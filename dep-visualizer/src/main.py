"""Точка входа CLI-приложения (Этап 4)."""

import sys
from src.cli import parse_args
from src.graph import load_test_repo, get_load_order


def main() -> None:
    """Вычисляет и выводит порядок загрузки зависимостей пакетов."""
    try:
        config = parse_args()
        if config["test_mode"]:
            repo_map = load_test_repo(config["repo"])
            order = get_load_order(
                repo_map, config["package"], config["max_depth"]
            )
            print("Порядок загрузки:", " -> ".join(order))
    except Exception as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
