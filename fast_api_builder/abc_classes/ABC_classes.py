from abc import ABC, abstractmethod
from typing import Callable

from fast_api_builder.utils.types import HttpMethod


class FastApiBuilderCore(ABC):
    @abstractmethod
    def _add_function_to_api():
        pass

    @abstractmethod
    def start_api():
        pass

    def add_function_to_api_decorator(
        self,
        route_path: str,
        method: HttpMethod,
        function_name: str = "<lambda>",
        function_description: str = "-",
        using_cache: bool = False,
        max_retries: int = 1_000_000,
    ) -> Callable:
        """Decorator function that add a function to the API routes.

        Args:
            route_path (str): The API path to the function.
            method (HttpMethod): The HTTP method to use for the API.
            function_name (str): The name of the function (for the API documentation). Defaults to "<lambda>".
            function_description (str): The description of the function (for the API documentation). Defaults to "-".
            using_cache (bool): Use the `lru_cache` decorator on the function. Defaults to False.
            max_retries (int, optional): The maximum number of call for this function. Defaults to 1_000_000.

        Returns:
            Callable: The modified instance or None if inplace is True.
        """

        def decorator(func: Callable) -> Callable:
            self._add_function_to_api(
                function=func,
                route_path=route_path,
                method=method,
                function_name=function_name,
                function_description=function_description,
                using_cache=using_cache,
                max_retries=max_retries,
            )
            return func

        return decorator
