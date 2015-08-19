_conditional_callables = {}


def _get_qualname(o):
    try:
        return o.__qualname__
    except AttributeError as _:
        return o.__module__+'.'+o.__class__.__name__+'.'+o.__name__


def _default_condition(*args, **kwargs):
    return True


def _get_callable(qual_name):
    return _conditional_callables.get(qual_name, ([], None))


def _add_callable(condition, f):
    qual_name = _get_qualname(f)
    callable_tuple = _get_callable(qual_name)

    if condition == _default_condition:
        callable_tuple = callable_tuple[0], f
    else:
        callable_list = callable_tuple[0]
        callable_list.append((condition, f))
        callable_tuple = callable_list, callable_tuple[1]

    _conditional_callables[qual_name] = callable_tuple


def _resolve_callable(f, *args, **kwargs):
    qual_name = _get_qualname(f)
    callable_tuple = _get_callable(qual_name)
    callable_iterator = (cc[1] for cc in callable_tuple[0]
                         if cc[0](*args, **kwargs))

    return next(callable_iterator, callable_tuple[1])


def predicate(condition=_default_condition):
    def wrapper(f):
        _add_callable(condition, f)

        def wrapped(*args, **kwargs):
            resolved_callable = _resolve_callable(f, *args, **kwargs)
            if resolved_callable is not None:
                return resolved_callable(*args, **kwargs)
            else:
                raise TypeError('Predicate for \'{fname}\' is not found'
                                .format(fname=_get_qualname(f)))
        return wrapped

    return wrapper


if __name__ == "__main__":
    @predicate()
    def foo(v):
        return 'default'

    @predicate(lambda v: v == 1)
    def foo(v):
        return 'f1'

    @predicate(lambda v: v == 2)
    def foo(v):
        return 'f2'

    @predicate(lambda v: v == 3)
    def foo(v):
        return 'f3'

    @predicate(lambda x, y: x == 3 and y == 2)
    def foo_multiple(x, y):
        return True

    @predicate()
    def foo_multiple(x, y):
        return False

    @predicate(lambda x: x > 1)
    def factorial(x):
        return x*factorial(x-1)

    @predicate()
    def factorial(x):
        return x

    @predicate(lambda x: x == 1)
    def bar(x):
        return True

    assert factorial(1) == 1
    assert factorial(5) == 120
    assert foo(v=1) == 'f1'
    assert foo(1) == 'f1'
    assert foo(2) == 'f2'
    assert foo(3) == 'f3'
    assert foo('x') == 'default'
    assert foo_multiple(4, 5) == False
    assert foo_multiple(3, 2) == True
    assert foo_multiple(x=3, y=3) == False
    assert foo_multiple(3, y=2) == True

    try:
        bar(2)
        assert False, 'Should throw TypeError exception'
    except TypeError as e:
        assert True
