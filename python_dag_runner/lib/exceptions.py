"""Exceptions for python-dag-runner"""

class CyclicDependenciesError(Exception):
    """Raised when a cyclic dependancy is found in graph"""

class InvalidTaskError(Exception):
    """Task provided is not a valid task"""
