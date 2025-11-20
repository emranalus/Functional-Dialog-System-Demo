import unittest

from models.node import Node
from beartype.roar import BeartypeHintViolation


class TestNode(unittest.TestCase):
    def test_node_types(self):
        def test_node_with_wrong_types():
            test = Node(1, 2)

        self.assertRaises(BeartypeHintViolation, test_node_with_wrong_types)

