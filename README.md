# python-contracts
=============================
A library for specifying and validating contracts on methods

Example Use:

```
from python-contracts import pre, post, param_type, return_type

@param_type('n', int, "n is an integer")
@pre(lambda n: n >= 0, "n is at least zero")
@return_type(int, "returns an integer")
@post(lambda r: r >= 0, "return value is positive")
def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
```

Will throw errors if any of the pre or post conditions are violated.
