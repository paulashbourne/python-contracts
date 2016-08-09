def expect_error(test_func, error_message = None):
    errored = False
    try:
        test_func()
    except Exception as e:
        errored = True
        if error_message:
            assert e.message == error_message, "Invalid error. Got '%s', expected '%s'" % (
                e.message, error_message
            )
    if error_message:
        assert errored, "Expected error to be thrown: '%s'" % error_message
    else:
        assert errored, "Expected an error to be thrown."

def expect_no_error(test_func):
    try:
        test_func()
    except Exception as e:
        "Expected no error to be thrown but got: '%s'" % e.message
