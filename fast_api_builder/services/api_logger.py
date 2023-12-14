from datetime import datetime
from functools import wraps
from typing import Callable


class ApiLogger:
    def __init__(self, log_file="api_log.txt", comment: str = ""):
        """Constructor for ApiLogger that will be used as a decorator function.

        Args:
            log_file (str, optional): The file to output the logs. Defaults to "api_log.txt".
            comment (str, optional): The comment to add to the logs. Defaults to "".
        """
        self.log_file = log_file.replace(".txt", ".log")
        self.comment = comment

    def __call__(self, func: Callable) -> Callable:
        """The decorator function.

        Args:
            func (Callable): The function to decorate.

        Returns:
            Callable: The decorated function.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            with open(self.log_file, "a") as file:
                date = datetime.now()
                file.write(
                    f"{date} | INFO | {self.comment} | function: {func.__name__}\n"
                )
                return func(*args, **kwargs)

        return wrapper
