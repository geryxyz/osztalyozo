import tkinter
import tkinter.ttk

import model
from gui.editable_treeview import EditTreeViewCellPopup
from model.data import Data


class Main(object):
    def display_task(self, task: model.Task, parent_task: model.Task = None, iid: str = ''):
        parent_iid = '' if parent_task is None else iid
        current_iid = parent_iid + '::' + task.name
        self.task_hierarchy.insert(
            parent=parent_iid,
            iid=current_iid,
            index='end',
            text=task.name,
            value=(f'{task.weight:.3%}',),
            open=True
        )
        for sub_task in task.sub_tasks.values():
            self.display_task(sub_task, task, current_iid)

    def insert_task_after_selected(self):
        print(self.task_hierarchy.selection())

    def engage_edit(self, event):
        if self.edit_popup:
            self.edit_popup.destroy()
        rowid = self.task_hierarchy.identify_row(event.y)
        column_indexing: str = self.task_hierarchy.identify_column(event.x)
        column_index: int = int(column_indexing.lstrip('#'))
        column_id = self.task_hierarchy.column(column_indexing)

        x, y, width, height = self.task_hierarchy.bbox(rowid, column_indexing)

        if column_index > 0:
            text = self.task_hierarchy.item(rowid, 'values')[column_index - 1]
        else:
            text = self.task_hierarchy.item(rowid, 'text')

        def on_set(row: str, column: str, value: str) -> None:
            ...
        self.edit_popup = EditTreeViewCellPopup(self.task_hierarchy, text, rowid, column_id, on_set)
        self.edit_popup.place(x=x, y=y, width=width, height=height)

    def __init__(self):
        self.model = Data()

        self.application = tkinter.Tk()
        self.application.title("Osztályozó")

        self.insert_after = tkinter.Button(
            self.application,
            text='insert new task after',
            command=self.insert_task_after_selected
        )
        self.insert_after.pack()

        self.task_hierarchy = tkinter.ttk.Treeview(self.application, columns=('weight',))
        self.task_hierarchy.heading('weight', text='Weight')
        self.edit_popup = None
        self.display_task(self.model.task)
        self.task_hierarchy.bind(
            '<<TreeviewSelect>>',
            lambda args: print(self.task_hierarchy.selection()))
        self.task_hierarchy.bind("<Button-3>", self.engage_edit)
        self.task_hierarchy.pack()

        self.application.mainloop()


if __name__ == '__main__':
    Main()
