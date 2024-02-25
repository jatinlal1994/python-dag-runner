"""Definition of dag class"""

import logging
from typing import List, Dict

from networkx import DiGraph, is_directed_acyclic_graph

from python_dag_runner.task import Task, TaskStatus
from python_dag_runner.lib.exceptions import CyclicDependenciesError
from python_dag_runner.lib.constants import EXECUTED_TASKS, FAILED_TASKS, TRIGGERED_TASKS, \
    ABORTED_TASKS


class Dag:
    """
    A directed acyclic graph to execute graph according to their dependencies.

    Args:
      name: Name of Dag
      tasks: A sequence of tasks to be executed

    Raises:
      InvalidDependenciesError: Graph has atleast one cyclic dependency
    """

    def __init__(self, name: str, tasks: List[Task]):
        self.name = name
        self.tasks = tasks
        self.graph: DiGraph = DiGraph()
        self.errors: Dict[str, str] = {}
        self.eligible_tasks: List[Task] = []
        self.execution_data = {
            EXECUTED_TASKS: set(),
            FAILED_TASKS: set(),
            TRIGGERED_TASKS: set(),
            ABORTED_TASKS: set(),
        }
        self.__generate_graph_from_tasks()

    def __generate_graph_from_tasks(self):
        """Generate dependancy graph for tasks"""
        for task in self.tasks:
            self.graph.add_node(task)

        for task in self.tasks:
            for sub_task in task.dependencies:
                self.graph.add_edge(sub_task, task)

        if not is_directed_acyclic_graph(self.graph):
            raise CyclicDependenciesError

    def __get_tasks_with_no_dependencies(self) -> List[Task]:
        """Fetch that are not having any dependencies and can start immediately"""
        return [
            task
            for task in self.graph.nodes()
            if not any(self.graph.predecessors(task))
        ]

    def __are_all_dependencies_completed(self, task: Task) -> bool:
        """Checks if all dependencies of the task are completed"""
        return task.dependencies <= self.execution_data[EXECUTED_TASKS]

    def __get_immediate_dependants(self, task: Task) -> List[Task]:
        """Fetch the immediate dependants of the task"""
        return list(self.graph.successors(task))

    def __mark_task_as_triggered(self, task: Task) -> None:
        """Add task to set of triggered tasks"""
        self.execution_data[TRIGGERED_TASKS] |= {task}

    def __is_already_triggered(self, task: Task) -> bool:
        """Is task already triggered or not"""
        return task in self.execution_data[TRIGGERED_TASKS]

    def __get_all_dependants_of_task(self, task: Task) -> List[Task]:
        """Get all the dependants of task"""
        dependants = []
        for node in self.graph.successors(task):
            dependants.append(node)
            dependants.extend(list(self.graph.successors(node)))
        return set(dependants)

    def task_completion_signal(self, task: Task, result: bool) -> None:
        """Signal to be raised when a task finishes execution"""
        if result == TaskStatus.SUCCESS:
            self.execution_data[EXECUTED_TASKS] |= {task}
            for dependant in self.__get_immediate_dependants(task):
                self.eligible_tasks.append(dependant)

        elif result == TaskStatus.FAILED:
            self.execution_data[FAILED_TASKS] |= {task}
            self.execution_data[ABORTED_TASKS] |= self.__get_all_dependants_of_task(task)

        self.execute_tasks()

    def execute_tasks(self):
        """Method to be executed each time a task is """
        eligible_tasks = []

        for task in self.eligible_tasks:
            if self.__are_all_dependencies_completed(task) and \
                not self.__is_already_triggered(task):
                self.__mark_task_as_triggered(task)
                eligible_tasks.append(task)

        logging.info("Tasks %s are eligible to run", eligible_tasks)
        for task in eligible_tasks:
            self.eligible_tasks.remove(task)
            task.execute(self)

    def initiate(self):
        """Initiate execution of tasks"""
        self.eligible_tasks = self.__get_tasks_with_no_dependencies()
        self.execute_tasks()
