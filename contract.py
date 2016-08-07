class ContractedFunction(object):

    def __init__(self, func):
        print "ContractedFunction.__init__"
        self.func = func

        self.preconditions  = []
        self.postconditions = []

    def execute(self, *args, **kwargs):
        print "ContractedFunction.execute"
        # Check preconditions
        for precondition in self.preconditions:
            precondition.execute_check(*args, **kwargs)

        # Execute the function call
        result = self.func(*args, **kwargs)

        # Check postconditions
        for postcondition in self.postconditions:
            postcondition.execute_check(result)

        return result

    def add_precondition(self, condition):
        print "ContractedFunction.add_precondition"
        self.preconditions.append(condition)

    def add_postcondition(self, condition):
        print "ContractedFunction.add_postcondition"
        self.postconditions.append(condition)

    def __call__(self, *args, **kwargs):
        print "ContractedFunction.__call__"
        return self.execute(*args, **kwargs)

class ContractDecorator(object):

    DEFAULT_ERROR = "A contract check failed"

    def __init__(self, check, description = None):
        self.check       = check
        self.description = description

class Precondition(ContractDecorator):

    DEFAULT_ERROR = "A precondition failed"

    # Two ways to define precondition
    #
    # 1. Precondition(param_name, check, error):
    # => param_name: string, param to restrict the precondition to
    # => check: lambda check, will be called with the argument specified by param_name
    # => description: string error message (optional)
    #
    # 2. Precondition(check, error):
    # => check: lambda check, will be called with all args/kwargs
    # => description: string error message (optional)
    def __init__(self, arg1, arg2 = None, arg3 = None):
        print "Precondition.__init__"
        if isinstance(arg1, basestring):
            # Precondition(param_name, check, description)
            self.param_name  = arg1
            self.check       = arg2
            self.description = arg3
        else:
            # Precondition(check, description)
            self.param_name  = None
            self.check       = arg1
            self.description = arg2

    @property
    def error(self):
        return self.description if self.description else self.DEFAULT_ERROR

    def execute_check(self, *args, **kwargs):
        if self.param_name:
            assert self.check(arg), self.error
        else:
            assert self.check(*args, **kwargs), self.error

    def __call__(self, func):
        print "Precondition.__call__"
        if isinstance(func, ContractedFunction):
            func.add_precondition(self)
            return func
        else:
            wrap = ContractedFunction(func)
            wrap.add_precondition(self)
            return wrap

class Postcondition(ContractDecorator):

    DEFAULT_ERROR = "A postcondition failed"

    def __init__(self, check, description = None):
        print "Postcondition.__init__"
        self.check       = check
        self.description = description

    def execute_check(self, result):
        assert self.check(result), self.error

    @property
    def error(self):
        return self.description if self.description else self.DEFAULT_ERROR

    def __call__(self, func):
        print "Postcondition.__call__"
        if isinstance(func, ContractedFunction):
            func.add_postcondition(self)
            return func
        else:
            wrap = ContractedFunction(func)
            wrap.add_postcondition(self)
            return wrap

pre  = Precondition
post = Postcondition

# Preconditions:
# @pre(check, error)
# => check is a lambda which will be called with all the args/kwargs of
#    the function call, error is a string error to be thrown when the check fails.
#    Useful for constraints between arguments
# @pre(argName, check, error):
# => restrict the check to a specific argument. check is a lambda which is called
#    only with the value of the variable as given in the string argName

# Postconditions:
# @post(check, error)
# => check is a lambda which will be called with the return value of the function
