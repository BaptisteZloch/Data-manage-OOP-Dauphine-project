from datetime import datetime
from typing import Callable, Dict

from fast_api_builder.services.fast_api_builder import FastApiBuilder
from pydantic import BaseModel


class MultiplyPostInput(BaseModel):
    x1: int
    x2: int


if __name__ == "__main__":
    api_builder = FastApiBuilder()

    @api_builder.add_function_to_api_decorator(
        "/test/{path_param:path}", "GET", max_retries=2
    )
    def path_param_test(path_param: str) -> Dict[str, str]:
        return {"result": path_param}

    @api_builder.add_function_to_api_decorator("/square", "GET", max_retries=100)
    def square(x1: int) -> int:
        return int(x1) ** 2

    @api_builder.add_function_to_api_decorator("/multiply", "GET", max_retries=100)
    def multiply(x1: int, x2: int) -> int:
        return int(x1) * int(x2)

    @api_builder.add_function_to_api_decorator("/multiply", "POST", max_retries=100)
    def multiply_with_post(param: MultiplyPostInput):
        return {"result": param.x1 * param.x2}

    api_builder._add_function_to_api(
        lambda x1, x2: {"result": int(x1) + int(x2)},
        "/sum",
        "GET",
        function_name="sum",
        using_cache=True,
        max_retries=100,
    )

    api_builder.start_api()
