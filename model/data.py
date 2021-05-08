import pandas

from model import Task


class Data(pandas.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = Task('Exam')
