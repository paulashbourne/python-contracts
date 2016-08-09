from contract import pre, post, param_type, return_type
from test_helper import expect_error, expect_no_error

@param_type('n', int, "n is an integer")
@pre(lambda n: n >= 0, "n is at least zero")
@return_type(int, "returns an integer")
@post(lambda r: r >= 0, "return value is positive")
def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

@return_type(int, "returns an integer")
def returns_string(n):
    return "foobar"

@param_type('a', int, "a is an integer")
@param_type('b', str, "b is a string")
@param_type('c', int, "c is an integer")
@pre('c', lambda c: c < 0, "c is less than zero")
def foobar(a, b, c):
    return a + b + c


def main():
    expect_error(lambda: fib("foobar"), "n is an integer")
    expect_error(lambda: fib(-1), "n is at least zero")
    expect_no_error(lambda: fib(4))

    expect_error(lambda: returns_string(10), "returns an integer")

    expect_error(lambda: foobar(1, 2, 3))
    expect_error(lambda: foobar(1, "", ""))
    expect_error(lambda: foobar("", "", 3))
    expect_no_error(lambda: foobar(1, "", 3))

if __name__ == "__main__":
    main()
