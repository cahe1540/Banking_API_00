from utils.catch_invalid_inputs import catch_invalid_inputs


# success passing string
def test_string_success():
    result = catch_invalid_inputs("string", "abc")
    assert result == "abc"


# fail passing string because non alphanumeric
def test_string_fail_space():
    try:
        result = catch_invalid_inputs("string", "a bc")
        assert False
    except TypeError:
        assert True


# fail passing string because non alphanumeric
def test_string_fail_underscore():
    try:
        result = catch_invalid_inputs("string", "a_bc")
        assert False
    except TypeError:
        assert True


def test_string_fail_period():
    try:
        result = catch_invalid_inputs("string", "a.bc")
        assert False
    except TypeError:
        assert True


# fail passing string because wrong data type
def test_string_fail_invalid_data():
    try:
        result = catch_invalid_inputs("string", 5)
        assert False
    except TypeError:
        assert True


# success passing int
def test_int_success():
    result = catch_invalid_inputs("int", 4)
    assert result == 4


# fail passing int because <= 0
def test_passing_int_lt_0():
    try:
        result = catch_invalid_inputs("int", -3)
        assert False
    except TypeError:
        assert True


# fail passing int because wrong data type
def test_int_bad_data_type():
    try:
        result = catch_invalid_inputs("int", "apple")
        assert False
    except TypeError:
        assert True


# success passing number as float
def test_number_as_float():
    result = catch_invalid_inputs("number", 4.2)
    assert result == 4.2


# success passing number as int
def test_number_as_int():
    result = catch_invalid_inputs("number", 2)
    assert result == 2


# fail passing float because <= 0 as int
def test_number_as_int_fail():
    try:
        result = catch_invalid_inputs("number", -3)
        assert False
    except TypeError:
        assert True


# fail passing number because <= 0 as float
def test_number_as_float_fail():
    try:
        result = catch_invalid_inputs("number", -4.44)
        assert False
    except TypeError:
        assert True


# fail passing number because wrong data type
def test_number_invalid_input():
    try:
        result = catch_invalid_inputs("number", None)
        assert False
    except TypeError:
        assert True


# fail pass a dict
def test_pass_dict():
    try:
        result = catch_invalid_inputs("number", {1: "apple"})
        assert False
    except TypeError:
        assert True


# fail pass a list
def test_pass_list():
    try:
        result = catch_invalid_inputs("int", [1,2,3])
        assert False
    except TypeError:
        assert True

# fail pass a list
def test_pass_list():
    try:
        result = catch_invalid_inputs("int", [True, False, True, True, True])
        assert False
    except TypeError:
        assert True
