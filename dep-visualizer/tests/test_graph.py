"""Модульные тесты для проверки корректности алгоритмов графа."""

import unittest
from src.graph import build_dfs_graph, get_load_order
from src.visualizer import generate_d2_text


class TestDependencyGraph(unittest.TestCase):
    """Набор тестов алгоритмов обхода графа."""

    def setUp(self) -> None:
        self.sample_repo = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["A", "E"],
            "D": [],
            "E": [],
        }

    def test_dfs_cycle_and_depth(self) -> None:
        """Проверяет обход с циклом и ограничением глубины."""
        graph = build_dfs_graph(self.sample_repo, "A", max_depth=2)
        self.assertEqual(graph["A"], ["B", "C"])
        self.assertEqual(graph["B"], ["D"])
        self.assertEqual(graph["C"], ["A", "E"])

    def test_load_order(self) -> None:
        """Проверяет топологический порядок загрузки зависимостей."""
        order = get_load_order(self.sample_repo, "A", max_depth=3)
        self.assertEqual(order[-1], "A")
        self.assertTrue(order.index("D") < order.index("B"))

    def test_d2_generation(self) -> None:
        """Проверяет генерацию текста D2."""
        d2_text = generate_d2_text({"A": ["B"], "B": []})
        self.assertIn('"A" -> "B"', d2_text)


if __name__ == "__main__":
    unittest.main()
