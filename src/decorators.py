from collections.abc import Callable
from functools import wraps
from typing import Optional


def log(filename: Optional[str] = None) -> Callable:


    def log_messages(message: str):
        if not filename:
            print(message)
        else:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(message)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok\n"
                log_messages(message)
                return result
            except Exception as e:
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}\n"
                log_messages(message)
                raise e

        return wrapper

    return decorator


# if __name__ == '__main__':
#     def my_function(x, y):
#         return x + y
#     foo = log(my_function)
#
#     help(foo)


#     @log(filename="mylog.txt")
#     def my_function(x, y):
#         return x + y
#
#
#     # print(my_function(1,'2'))
