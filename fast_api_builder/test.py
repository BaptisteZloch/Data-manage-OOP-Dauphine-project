from datetime import datetime
from typing import Callable, Dict

from services.fast_api_builder import FastApiBuilder


# class ApiLogger:
#     def __init__(self, log_file="api_log.txt", comment: str = ""):
#         self.log_file = log_file
#         self.comment = comment

#     def __call__(self, func: Callable):
#         def wrapper(*args, **kwargs):
#             result = func(*args, **kwargs)
#             with open(self.log_file, "a") as file:
#                 date = datetime.now()
#                 file.write(
#                     f"{date} | {self.comment} | {func.__name__} | result: {result}\n"
#                 )
#             return result

#         return wrapper


# @ApiLogger(log_file="api_log.txt", comment="test")
# def mafunc(k: int) -> int:
#     return k**2


# @ApiLogger(log_file="api_log.txt", comment="test2")
# def mafunc2(k: int) -> int:
#     return k**3


if __name__ == "__main__":
    # mafunc(2)
    # mafunc2(2)
    api_builder = FastApiBuilder()

    @api_builder.add_function_to_api_decorator("/foo/{rest_of_path:path}", "GET")
    def foo(rest_of_path: str) -> Dict[str, str]:
        """Function to test the API."""
        return {"rest_of_path": rest_of_path}

    api_builder.add_function_to_api(
        lambda rest_of_path: {"rest_of_path": rest_of_path},
        "/bar/{rest_of_path:path}",
        "GET",
        function_name="bar",
        using_cache=True,
    )
    api_builder.start_api()
