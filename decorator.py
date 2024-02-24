def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return f"Value error: {ve}"
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"

    return inner
