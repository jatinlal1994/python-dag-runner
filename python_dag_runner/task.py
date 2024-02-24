"""Definition of task and it's metadata"""

import logging
from uuid import uuid4
from uuid import UUID
from enum import StrEnum, auto
from typing import Callable


class TaskStatus(StrEnum):
    """Options for task status"""
    SUCCESS = auto()
    FAILED = auto()


class Task:
    """Represents a task to be executed within a DAG (Directed Acyclic Graph).

    Args:
        name (str): A unique name identifying the task.
        executable (callable): The function or callable object to be executed as the task.

    Attributes:
        name (str): A unique name identifying the task.
        executable (callable): The function or callable object to be executed as the task.

    Raises:
        TypeError: If `executable` is not a callable object.

    Example:
        Consider a DAG (Directed Acyclic Graph) where you want to define tasks.
        You can create a task like this:

        >>> task = Task(name='Fetch resources', executable=fetch_resources)
    """

    def __init__(self, name: str, executable: Callable, dependencies: set['Task'] = None):
        """Task Constructor"""
        self.id: UUID = uuid4()
        self.name: str = name
        self.executable: Callable = executable
        self.dependencies: dependencies = dependencies or set()

    def __repr__(self):
        """Returns name of task to be shown when task object is used"""
        return self.name

    def __hash__(self):
        """Return a hash for the created task"""
        return hash(self.id)

    def __ior__(self, other):
        """Set dependencies of task using '|=' operator"""
        self.dependencies = other
        return self

    def execute(self, dag):
        """Start execution of function"""
        try:
            logging.info("Starting execution of %s", self.name)
            self.executable()
            dag.task_completion_signal(self, TaskStatus.SUCCESS)
        except (TypeError, BaseException) as err:  # pylint: disable=broad-except
            dag.errors[self] = repr(err)
            dag.task_completion_signal(self, TaskStatus.SUCCESS)
            logging.exception(err)
