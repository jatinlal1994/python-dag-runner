"""Exceptions for dagger"""

class CyclicDependenciesError(Exception):
    """Raised when a cyclic dependancy is found in graph"""
