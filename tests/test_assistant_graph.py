
import unittest

from graphs.assistant_graph import graph


class TestAssistantGraph(unittest.TestCase):

    def test_required_nodes_exist(self):
        graph_structure = graph.get_graph()
        node_names = set(graph_structure.nodes)

        self.assertIn("assistant", node_names)
        self.assertIn("tools", node_names)

    def test_graph_starts_with_assistant(self):
        graph_structure = graph.get_graph()

        edges = {
            (edge.source, edge.target)
            for edge in graph_structure.edges
        }

        self.assertIn(("__start__", "assistant"), edges)

    def test_tools_return_to_assistant(self):
        graph_structure = graph.get_graph()

        edges = {
            (edge.source, edge.target)
            for edge in graph_structure.edges
        }

        self.assertIn(("tools", "assistant"), edges)


if __name__ == "__main__":
    unittest.main()
