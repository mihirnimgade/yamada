"""
Unit tests for yamada.py

@author: Dakota Hawkins
@date: July 11, 2018
"""

import unittest

from yamada import yamada
import networkx as nx


class YamadaTest(unittest.TestCase):

    def setUp(self):
        example = {1: {2: {'weight': 2},
                       3: {'weight': 1}},
                   2: {1: {'weight': 2},
                       3: {'weight': 3},
                       4: {'weight': 1}},
                   3: {1: {'weight': 1},
                       2: {'weight': 3},
                       4: {'weight': 2},
                       5: {'weight': 2}},
                   4: {2: {'weight': 1},
                       3: {'weight': 2},
                       5: {'weight': 1},
                       6: {'weight': 3}},
                   5: {3: {'weight': 2},
                       4: {'weight': 1},
                       6: {'weight': 3}},
                   6: {4: {'weight': 3},
                       5: {'weight': 3}}}
        graph = nx.Graph(example)
        tree = {1: {2: {'weight': 2},
                    3: {'weight': 1}},
                2: {4: {'weight': 1}},
                4: {5: {'weight': 1},
                    6: {'weight': 3}}}
        self.tree = nx.Graph(tree)
        self.yamada = yamada.Yamada(graph)

    def test_edge_replacement_presence(self):
        tree = self.yamada.replace_edge(self.tree, (4, 5), (3, 5))
        self.assertTrue((3, 5) in tree.edges)

    def test_edge_replacement_presence(self):
        tree = self.yamada.replace_edge(self.tree, (4, 5), (3, 5))
        self.assertTrue(tree[3][5]['weight'] == 2)

    def test_edge_replacement_removal(self):
        tree = self.yamada.replace_edge(self.tree, (4, 5), (3, 5))
        self.assertTrue((4, 5) not in tree.edges)

    def test_edge_replacement_new_edge_set(self):
        tree = self.yamada.replace_edge(self.tree, (4, 5), (3, 5))
        new_tree_edge_set = set(tree.edges)
        old_tree_edge_set = set(self.tree.edges) 
        self.assertTrue(new_tree_edge_set.difference(old_tree_edge_set) == set((3, 5)))

    def test_edge_replacement_old_edge_set(self):
        tree = self.yamada.replace_edge(self.tree, (4, 5), (3, 5))
        new_tree_edge_set = set(tree.edges)
        old_tree_edge_set = set(self.tree.edges) 
        self.assertTrue(old_tree_edge_set.difference(new_tree_edge_set) == set((4, 5)))

class SubstituteTest(unittest.TestCase):
    """Test Substitute class in yamada.py"""

    def setUp(self):
        sub_example = {1: {2: {'weight': 3},
                           3: {'weight': 12},
                          10: {'weight': 12}},
                       2: {1: {'weight': 3},
                           8: {'weight': 12},
                           10: {'weight': 12}},
                       3: {1: {'weight': 12},
                           4: {'weight': 7},
                           5: {'weight': 10},
                           6: {'weight': 10}},
                       4: {3: {'weight': 7},
                           7: {'weight': 1},
                           10: {'weight': 10}},
                       5: {3: {'weight': 10},
                           6: {'weight': 3},
                           7: {'weight': 13},
                           8: {'weight': 10}},
                       6: {3: {'weight': 10},
                           5: {'weight': 3},
                           7: {'weight': 10}},
                       7: {4: {'weight': 1},
                           5: {'weight': 13},
                           6: {'weight': 10},
                           9: {'weight': 10}},
                       8: {2: {'weight': 12},
                           9: {'weight': 6},
                           5: {'weight': 10}},
                       9: {7: {'weight': 10},
                           8: {'weight': 6},
                           10: {'weight': 7}},
                       10: {1: {'weight': 12},
                            2: {'weight': 12},
                            4: {'weight': 10},
                            9: {'weight': 7}}}
        sub_tree_example = {1: {2: {'weight': 3}},
                            2: {10: {'weight': 12}},
                            10: {9: {'weight': 7}},
                            9: {8: {'weight': 6},
                                7: {'weight': 10}},
                            7: {4: {'weight': 1},
                                6: {'weight': 10}},
                            4: {3: {'weight': 7}},
                            6: {5: {'weight': 3}}}
        self.graph = nx.Graph(sub_example)
        self.tree = nx.Graph(sub_tree_example)

    def test_substitute_edges(self):
        sub = yamada.Substitute(graph=self.graph, tree=self.tree,
                                fixed_edges=set(), restricted_edges=set(),
                                ordered=True)
        sub_edges = sub.substitute()
        self.assertTrue(sub_edges[(1, 2)] is None)
        self.assertTrue(sub_edges[(2, 10)] == (1, 3))
        self.assertTrue(sub_edges[(3, 4)] is None)
        self.assertTrue(sub_edges[(4, 7)] is None)
        self.assertTrue(sub_edges[(5, 6)] is None)
        self.assertTrue(sub_edges[(6, 7)] == (5, 3))
        self.assertTrue(sub_edges[(7, 9)] == (4, 10))
        self.assertTrue(sub_edges[(8, 9)] is None)
        self.assertTrue(sub_edges[(9, 10)] is None)

    def test_no_substitute_edges(self):
        sub = yamada.Substitute(graph=self.tree, tree=self.tree,
                                fixed_edges=set(), restricted_edges=set(),
                                ordered=True)
        sub_edges = sub.substitute()
        self.assertTrue(sub_edges is None)


if __name__ == "__main__":
    unittest.main()