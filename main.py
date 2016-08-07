from contract import pre, post

@pre(lambda n: type(n) == int, "n is an integer")
@pre(lambda n: n >= 0, "n is at least zero")
@post(lambda r: type(r) == int, "returns an integer")
@post(lambda r: r >= 0, "return value is positive")
def fib(n):
    return "hello"
    if n <= 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def main():
    fib(4)

if __name__ == "__main__":
    main()
