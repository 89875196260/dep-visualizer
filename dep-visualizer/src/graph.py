"""Модуль построения графа зависимостей и дополнительных операций."""

START_DEPTH = 0


def load_test_repo(filepath: str) -> dict[str, list[str]]:
    """Загружает граф зависимостей из тестового файла формата 'A: B C'."""
    graph: dict[str, list[str]] = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            clean = line.strip()
            if not clean or ":" not in clean:
                continue
            pkg, raw_deps = clean.split(":", 1)
            graph[pkg.strip()] = raw_deps.strip().split()
    return graph


def simplify_index(
    packages: dict[tuple[str, str], list[str]], root_pkg: str, root_ver: str
) -> dict[str, list[str]]:
    """Преобразует индекс (имя, версия) в карту {имя: зависимости}."""
    simple: dict[str, list[str]] = {}
    for (pkg, _), deps in packages.items():
        if pkg not in simple:
            simple[pkg] = deps
    if (root_pkg, root_ver) not in packages:
        raise ValueError(f"Пакет {root_pkg} ({root_ver}) не найден.")
    simple[root_pkg] = packages[(root_pkg, root_ver)]
    return simple


def build_dfs_graph(
    repo_map: dict[str, list[str]], start_pkg: str, max_depth: int
) -> dict[str, list[str]]:
    """Строит граф зависимостей рекурсивным алгоритмом DFS."""
    result_graph: dict[str, list[str]] = {}
    visited_path: set[str] = set()

    def _dfs(current: str, depth: int) -> None:
        if current not in result_graph:
            result_graph[current] = []
        if depth >= max_depth:
            return
        visited_path.add(current)
        for dep in repo_map.get(current, []):
            if dep not in result_graph[current]:
                result_graph[current].append(dep)
            if dep not in visited_path:
                _dfs(dep, depth + 1)
        visited_path.remove(current)

    _dfs(start_pkg, START_DEPTH)
    return result_graph


def get_load_order(
    repo_map: dict[str, list[str]], start_pkg: str, max_depth: int
) -> list[str]:
    """Вычисляет порядок загрузки зависимостей (post-order DFS)."""
    order: list[str] = []
    visited: set[str] = set()
    in_stack: set[str] = set()

    def _visit(current: str, depth: int) -> None:
        if current in visited or depth > max_depth:
            return
        in_stack.add(current)
        for dep in repo_map.get(current, []):
            if dep not in in_stack and depth + 1 <= max_depth:
                _visit(dep, depth + 1)
        in_stack.remove(current)
        visited.add(current)
        order.append(current)

    _visit(start_pkg, START_DEPTH)
    return order
