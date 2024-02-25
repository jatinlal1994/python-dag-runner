"""Definition of task and it's metadata"""

import logging
from enum import Enum
from uuid import UUID, uuid4
from typing import Callable, Set

from python_dag_runner.lib.exceptions import InvalidTaskError


class TaskStatus(Enum):
    """Options for task status"""
    SUCCESS = "success"
    FAILED = "failed"


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

    def __init__(self, name: str, executable: Callable, dependencies: Set['Task'] = None):
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
        if not isinstance(other, set):
            raise InvalidTaskError

        for task in other:
            if not isinstance(task, Task):
                raise InvalidTaskError

        self.dependencies = other
        return self

    def execute(self, dag):
        """Start execution of function"""
        try:
            logging.info("Starting execution of %s", self.name)
            self.executable()
            dag.task_completion_signal(self, TaskStatus.SUCCESS)
        except Exception as err:  # pylint: disable=broad-except
            dag.errors[self] = repr(err)
            dag.task_completion_signal(self, TaskStatus.SUCCESS)
            logging.exception(err)
