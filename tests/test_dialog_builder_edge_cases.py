import unittest

from models.dialog_builder import DialogBuilder
from models.node import Node
from beartype.roar import BeartypeHintViolation


class TestDialogBuilderEdgeCases(unittest.TestCase):
    # Runs before each test
    def setUp(self):
        self.NODE_MOCK_EMPTY = Node('','')
        self.NODE_MOCK_TEST = Node('test', 'test')
        self.OPTIONS_MOCK_1 = [Node('',''), Node('',''), Node('','')]
        self.OPTIONS_MOCK_2 = [Node('test', 'test'), Node('test', 'test'), Node('test', 'test')]

    
    # @beartype decorator is used on the class itself eliminating the need for other type check errors
    def test_set_root_wrong_parameter(self):
        dib = DialogBuilder()

        def set_root_wrong(dib):
            dib.set_root('wrong type')

        self.assertRaises(BeartypeHintViolation, set_root_wrong, dib)


    
