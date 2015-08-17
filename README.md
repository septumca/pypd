Predicative dispatch decorator for python, based on idea from http://www.oreilly.com/programming/free/functional-programming-python.csp

Module is providing means to specify condition that determine which function is called. Number of arguments in condition function in @predicate decorator must be equal to number of arguments of wrapped function

usage:
from predicate_dispatch import predicate

@predicate(lambda x: x>1)
def factorial(x):
  return x*factorial(x-1)

@predicate()
def factorial(x):
  return x
        
factorial(5) == 120
