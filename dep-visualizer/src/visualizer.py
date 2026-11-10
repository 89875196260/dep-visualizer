"""Модуль генерации диаграмм D2 и рендеринга в формат SVG."""

import os
import subprocess
import tempfile


def generate_d2_text(graph: dict[str, list[str]]) -> str:
    """Формирует текстовое описание графа на языке диаграмм D2."""
    lines: list[str] = ["direction: down"]
    for node, deps in graph.items():
        safe_node = f'"{node}"'
        if not deps:
            lines.append(safe_node)
        for dep in deps:
            safe_dep = f'"{dep}"'
            lines.append(f"{safe_node} -> {safe_dep}")
    return "\n".join(lines)


def render_d2_to_svg(d2_text: str, output_svg: str) -> None:
    """Сохраняет D2-код во временный файл и компилирует его в SVG."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".d2", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(d2_text)
        tmp_path = tmp.name

    try:
        subprocess.run(
            ["d2", tmp_path, output_svg],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as err:
        raise RuntimeError(
            "Утилита 'd2' не найдена. Установите D2."
        ) from err
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
