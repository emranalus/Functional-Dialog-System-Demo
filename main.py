import os

from textual.app import App, ComposeResult
from textual.widgets import Label, ListItem, ListView
from models.node import Node
from models.dialog_builder import DialogBuilder
from beartype.roar import BeartypeHintViolation


# Dynamic dialog building
try:
    dib = DialogBuilder()
    dib \
        .set_root(Node("root", "root")) \
        .add_options([Node("Hi!", f"Long time no see {os.getlogin()} its been awhile."), 
                    Node("Wassup.", "Nothing much fixing my car as you can see..."), 
                    Node("Bye.", "Bye to you to cya!")]) \
        .make_retainer_option(0) \
        .move_current_node_forward(1) \
        .add_options([Node("Nice.", "Isn't she a beauty!")
                    , Node("About...", "Yeah, right what did you wanted to talk to me about?")]) \
        .make_retainer_option(0) \
        .make_stepback_option(1)

except BeartypeHintViolation as e:
    print(e)
    exit()
except IndexError as e:
    print(e)
    print('HINT: This indicates error is probably tree navigation related.')
    exit()

class TryingApp(App):
    CSS_PATH = "dialog_system_demo.tcss"
    TITLE = "Functional Dialog System Demo"

    # Initializes widgets
    def compose(self) -> ComposeResult:
        # Gets computer username and greets user therefore initiating the conversation
        self.dialog_response = Label(f"Hello {os.getlogin()}!", id="dialog_response")
        yield self.dialog_response

        # * operator removes the brackets of the list therefor unpacking it other than that its just a for loop
        # Without * operator only generator object returns so it has to be used despite looking scary
        self.root = dib.get_root()
        self.list_view = ListView( *[ListItem(option.get_option_as_label()) for option in self.root.options] , id="options")
        yield self.list_view


    # Triggered when entered an option
    def on_list_view_selected(self) -> None:
        # Update root
        index = self.list_view.index
        self.root = self.root.options[index]

        # Update ListView
        self.list_view.clear()
        self.list_view.insert(0, [ListItem(option.get_option_as_label()) for option in self.root.options] )

        # Display response
        self.dialog_response.update(self.root.response)

        # If conversation ends terminate the app
        if not self.root.options:
            self.exit()


# Main
if __name__ == "__main__":
    app = TryingApp()
    app.run()
    exit(app.return_code or 0)
