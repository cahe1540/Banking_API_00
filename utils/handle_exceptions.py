from utils.response_as_json import response_as_json
from exceptions.client_not_found_error import ClientNotFoundError
from exceptions.account_not_found_error import AccountNotFoundError
from exceptions.overdraft_exception import OverDraftError


# no args
def handle_exceptions_no_args(route_handler):
    def handler():
        try:
            return route_handler()
        except ValueError as e:
            return response_as_json(str(e), 404), 404
        except OverDraftError as e:
            return response_as_json(str(e), 422), 422
        except TypeError as e:
            return response_as_json(str(e), 400), 400
        except AccountNotFoundError as e:
            return response_as_json(str(e), 404), 404
        except ClientNotFoundError as e:
            return response_as_json(str(e), 404), 404
        except LookupError as e:
            return response_as_json(str(e), 400), 400
        except Exception as e:
            return response_as_json(str(e), 500), 500
    handler.__name__ = route_handler.__name__
    return handler


# handle exceptions with args
def handle_exceptions_w_args(route_handler):
    def handler(*args, **kwargs):
        try:
            return route_handler(*args, **kwargs)
        except ValueError as e:
            return response_as_json(str(e), 404), 404
        except OverDraftError as e:
            return response_as_json(str(e), 422), 422
        except TypeError as e:
            return response_as_json(str(e), 400), 400
        except AccountNotFoundError as e:
            return response_as_json(str(e), 404), 404
        except ClientNotFoundError as e:
            return response_as_json(str(e), 404), 404
        except LookupError as e:
            return response_as_json(str(e), 400), 400
        except Exception as e:
            return response_as_json(str(e), 500), 500
    handler.__name__ = route_handler.__name__
    return handler
