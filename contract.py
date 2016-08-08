class FunctionCall(object):

    def __init__(self, func, *args, **kwargs):
        self.func   = func
        self.args   = args
        self.kwargs = kwargs

        # Init argument dict
        self.arg_dict = {}
        for pos, param_name in enumerate(func.func_code.co_varnames):
            if param_name in kwargs:
                self.arg_dict[param_name] = kwargs[param_name]
            else:
                self.arg_dict[param_name] = args[pos]

    def get_argument(self, param_name):
        # Gets the value of the argument from either args or kwargs
        return self.arg_dict[param_name]

class ContractedFunction(object):

    def __init__(self, func):
        self.func = func

        self.preconditions  = []
        self.postconditions = []

    def execute(self, *args, **kwargs):
        # Check preconditions
        for precondition in self.preconditions:
            precondition.execute_check(self.func, *args, **kwargs)

        # Execute the function call
        result = self.func(*args, **kwargs)

        # Check postconditions
        for postcondition in self.postconditions:
            postcondition.execute_check(result)

        return result

    def add_precondition(self, condition):
        self.preconditions.append(condition)

    def add_postcondition(self, condition):
        self.postconditions.append(condition)

    def __call__(self, *args, **kwargs):
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

    def execute_check(self, func, *args, **kwargs):
        if self.param_name:
            arg = FunctionCall(func, *args, **kwargs).get_argument(self.param_name)
            assert self.check(arg), self.error
        else:
            assert self.check(*args, **kwargs), self.error

    def __call__(self, func):
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
        self.check       = check
        self.description = description

    def execute_check(self, result):
        assert self.check(result), self.error

    @property
    def error(self):
        return self.description if self.description else self.DEFAULT_ERROR

    def __call__(self, func):
        if isinstance(func, ContractedFunction):
            func.add_postcondition(self)
            return func
        else:
            wrap = ContractedFunction(func)
            wrap.add_postcondition(self)
            return wrap

pre  = Precondition
post = Postcondition

def param_type(param_name, _type, description = None):
    if description is None:
        description = "%s is of type %s" % (param_name, type)
    return pre(param_name, lambda p: isinstance(p, _type), description)

def return_type(_type, description = None):
    if description is None:
        description = "return value is of type %s" % (param_name, type)
    return post(lambda p: isinstance(p, _type), description)

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
