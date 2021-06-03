
# function to check if inputs are valid
# string, int, or number

def catch_invalid_inputs(input_type: str, arg):
    # edge case for boolean
    if isinstance(str, bool):
        raise TypeError(f"Input {arg} must be of type 'int', 'float' or 'string'.")
    # check for string type entries
    if input_type == "string" and type(arg) == str:
        # arg can only be alphanumeric
        if arg.isalnum():
            return arg
        # raise exception if fails test
        else:
            raise TypeError(f"Input {arg} must be of type 'string' and alphanumeric.")
    # check for int type entries
    elif input_type == "int":
        # verify input is int and non negative
        if isinstance(arg, int) and arg > 0:
            return arg
        # raise exception if not
        else:
            raise TypeError(f"Input {arg} must be of type 'int' and greater than 0.")
    elif input_type == "number":
        if (isinstance(arg, float) or isinstance(arg, int)) and arg > 0:
            return arg
        else:
            raise TypeError(f"Input {arg} must be of type 'float' or 'int' and greater than 0.")
    raise TypeError(f"Input {arg} must be of type 'int', 'float' or 'string'.")