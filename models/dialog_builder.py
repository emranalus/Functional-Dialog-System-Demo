from typing import List
from models.node import Node
from collections import deque
from beartype import beartype


@beartype
class DialogBuilder:
    # Class attributes
    CURRENT_NODE_INDEX = -1
    PARENT_NODE_INDEX = -2
    GRANDPARENT_NODE_INDEX = -3

    def __init__(self):
        # Instance attributes
        self.root = None
        self.current_node = None
        self.selected_option = None
        self.stack = deque()


    def _print_children_of_current_node(self):
        for i in self.get_current_options():
            print(i.option)
        return self
    

    # Select 1 option from a list of options - requires at least one node present in the tree
    def _select_option(self, index: int) -> Node:
        selected_option = self.get_current_node().options[index]
        return selected_option
        

    # Sets the current node in object scope than pushes it into stack
    def _set_current_node(self, node: Node, dont_stack=False):
        self.current_node = node
        if not dont_stack:
            self.stack.append(self.current_node)
        return self


    def set_root(self, node: Node):
        self.root = node
        self.stack.append(self.root)
        return self


    def get_root(self) -> Node:
        return self.root


    def get_current_node(self) -> Node:
        return self.stack[self.CURRENT_NODE_INDEX]


    def get_current_options(self) -> List[Node]:
        return self.get_current_node().options


    # By taking in an index number to index a list of dialog options we assign a dialog option in object scope
    # Than we set the current option/node as root therefore pushing it into stack and updating in object scope
    def move_current_node_forward(self, index: int):
        self.selected_option = self._select_option(index)
        self._set_current_node(self.selected_option)
        return self
    

    # We set the current node to the previous node and pop the stack to go a step back in guidance with the stack 
    def move_current_node_backward(self):
        self._set_current_node(self.stack[self.PARENT_NODE_INDEX], True)
        self.stack.pop()
        return self


    def add_options(self, options: list[Node]):
        self.get_current_node().options += options
        return self
    

    # A stepback option is defined by having its grandparents options as its own therefore not containing itself.
    def make_stepback_option(self, index: int):
        self.move_current_node_forward(index)
        self.selected_option.options = self.stack[self.GRANDPARENT_NODE_INDEX].options
        self.move_current_node_backward()
        return self


    # A retainer option is defined by having its parents options as its own therefore containing itself.
    # PS. An ender option is defined by having no options its the job of the main code block to end the dialog
    def make_retainer_option(self, index: int):
        self.move_current_node_forward(index)
        self.selected_option.options = self.stack[self.PARENT_NODE_INDEX].options
        self.move_current_node_backward()
        return self

