from datetime import datetime


class ApiLogger:
    def __init__(self, log_file="api_log.log"):
        self.log_file = log_file.replace(".txt", ".log")

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(self.log_file, "a") as file:
                date = datetime.now()
                file.write(f"{date} |  | Details: {result}\n")
            return result

        return wrapper
