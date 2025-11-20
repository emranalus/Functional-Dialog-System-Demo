from textual.widget import Widget
from textual.widgets import Label
from beartype import beartype


@beartype
class Node(Widget):
    def __init__(self, option: str, response: str):
        self.option = option
        self.response = response
        self.options = []

    
    def get_response_as_label(self) -> Label:
        return Label(self.response)
    

    def get_option_as_label(self) -> Label:
        return Label(self.option)
