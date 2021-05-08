import typing
from tkinter import Entry


class EditTreeViewCellPopup(Entry):
    def __init__(
            self,
            parent,
            text: str, row: str, column: str,
            on_set: typing.Callable[[str, str, str], None], **kw):
        super().__init__(parent, **kw)
        self.on_set: typing.Callable[[str, str, str], None] = on_set
        self.row = row
        self.column = column

        self.insert(0, text)
        self['exportselection'] = False

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Escape>", lambda *ignore: self.destroy())

    def on_return(self, event):
        if self.on_set:
            self.on_set(self.row, self.column, self.get())
        self.destroy()

    def select_all(self, *ignore):
        """ Set selection on the whole text """
        self.selection_range(0, 'end')

        # returns 'break' to interrupt default key-bindings
        return 'break'
