"""Точка входа CLI-приложения (Этап 3)."""

import sys
from src.cli import parse_args
from src.graph import load_test_repo, build_dfs_graph


def main() -> None:
    """Запускает рекурсивный DFS на тестовом репозитории."""
    try:
        config = parse_args()
        if config["test_mode"]:
            repo_map = load_test_repo(config["repo"])
            graph = build_dfs_graph(
                repo_map, config["package"], config["max_depth"]
            )
            print("Построенный граф зависимостей:", graph)
    except Exception as err:
        print(f"Ошибка: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
