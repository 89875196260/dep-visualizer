"""Главная точка входа инструмента визуализации зависимостей."""

import sys
from src.cli import parse_args
from src.fetcher import download_apkindex, parse_apkindex
from src.graph import (
    build_dfs_graph,
    get_load_order,
    load_test_repo,
    simplify_index,
)
from src.visualizer import generate_d2_text, render_d2_to_svg


def _prepare_repo_map(config: dict) -> dict[str, list[str]]:
    """Загружает карту зависимостей из тестового файла или сети."""
    if config["test_mode"]:
        return load_test_repo(config["repo"])
    raw_index = download_apkindex(config["repo"])
    packages = parse_apkindex(raw_index)
    return simplify_index(packages, config["package"], config["version"])


def main() -> None:
    """Выполняет полный цикл анализа и визуализации зависимостей."""
    try:
        config = parse_args()
        repo_map = _prepare_repo_map(config)
        graph = build_dfs_graph(
            repo_map, config["package"], config["max_depth"]
        )
        order = get_load_order(
            repo_map, config["package"], config["max_depth"]
        )
        d2_code = generate_d2_text(graph)
        print("Порядок загрузки:", " -> ".join(order))
        print("\nКод диаграммы D2:\n" + d2_code)
        render_d2_to_svg(d2_code, config["output"])
        print(f"\nГраф успешно сохранен в {config['output']}")
    except Exception as err:
        print(f"Ошибка выполнения: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
