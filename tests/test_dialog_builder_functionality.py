import unittest

from models.dialog_builder import DialogBuilder
from models.node import Node


class TestDialogBuilderFunctionality(unittest.TestCase):
    # Runs before each test
    def setUp(self):
        self.NODE_MOCK_EMPTY = Node('','')
        self.NODE_MOCK_TEST = Node('test', 'test')
        self.OPTIONS_MOCK_1 = [Node('',''), Node('',''), Node('','')]
        self.OPTIONS_MOCK_2 = [Node('test', 'test'), Node('test', 'test'), Node('test', 'test')]


    # Functionality tests
    def test_set_get_root(self):
        dib = DialogBuilder()
        root = self.NODE_MOCK_EMPTY

        dib.set_root(root)

        self.assertEqual(root, dib.get_root())

    
    def test_add_get_options(self):
        dib = DialogBuilder()
        options1 = self.OPTIONS_MOCK_1
        options2 = self.OPTIONS_MOCK_1

        dib \
            .set_root(Node('','')) \
            .add_options(options1) \
            .add_options(options2)
        
        self.assertEqual(dib.get_current_options(), options1 + options2)


    def test_move_current_node_forward(self):
        dib = DialogBuilder()
        test_node = self.NODE_MOCK_TEST
        options = [Node('',''), test_node, Node('','')]

        dib \
            .set_root(Node('','')) \
            .add_options(options) \
            .move_current_node_forward(1)
        
        self.assertEqual(dib.get_current_node(), test_node)


    def test_move_current_node_backward(self):
        dib = DialogBuilder()
        test_node = self.NODE_MOCK_TEST
        options = self.OPTIONS_MOCK_1

        dib \
            .set_root(test_node) \
            .add_options(options) \
            .move_current_node_forward(1) \
            .move_current_node_backward()
        
        self.assertEqual(dib.get_current_node(), test_node)


    def test_make_stepback_option(self):
        dib = DialogBuilder()
        root = self.NODE_MOCK_EMPTY
        options_of_root = self.OPTIONS_MOCK_1
        options_of_child = self.OPTIONS_MOCK_2

        dib \
            .set_root(root) \
            .add_options(options_of_root) \
            .move_current_node_forward(1) \
            .add_options(options_of_child) \
            .make_stepback_option(1) \
            .move_current_node_forward(1)

        current = dib.get_current_node()
        self.assertEqual(current.options, dib.stack[-3].options)
        self.assertNotIn(current, dib.stack[-3].options)
            

    def test_make_retainer_option(self):
        dib = DialogBuilder()
        root = self.NODE_MOCK_EMPTY
        options_of_root = self.OPTIONS_MOCK_1

        dib \
            .set_root(root) \
            .add_options(options_of_root) \
            .make_retainer_option(1) \
            .move_current_node_forward(1) \
        
        current = dib.get_current_node()
        self.assertEqual(current.options, dib.stack[-2].options)
        self.assertIn(current, dib.stack[-2].options)
