from __future__ import annotations

import typing


class WeightError(ValueError):
    ...


class Task(object):
    def __init__(self, name, *sub_tasks: Task):
        self.name = name
        self.weight = 0
        self._check_weights(sub_tasks)
        self.sub_tasks: typing.Dict[Task] = {t.name: t for t in sub_tasks}

    @staticmethod
    def _check_weights(sub_tasks):
        if not (0 <= sum([t.weight for t in sub_tasks]) <= 1):
            raise WeightError('weight must be greater than 0 and less than 1')

