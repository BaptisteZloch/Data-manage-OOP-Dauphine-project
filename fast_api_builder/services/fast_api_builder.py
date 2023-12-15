from __future__ import annotations
from functools import lru_cache
from typing import Any, Callable, Iterable, Self, Union
from fastapi import APIRouter, FastAPI
import uvicorn
from fast_api_builder.abc_classes.ABC_classes import FastApiBuilderCore
from fast_api_builder.utils.utils import FastApiBuilderUtility
from fast_api_builder.services.api_logger import ApiLogger
from fast_api_builder.utils.types import CustomRoute, HttpMethod


class FastApiBuilder(FastApiBuilderCore, FastApiBuilderUtility):
    _instance = None

    def __init__(
        self,
        log_paths: str = "api_log.log",
    ) -> None:
        self.__log_paths = log_paths
        self.__app = FastAPI()
        self.__app_router = APIRouter()

        self._add_function_to_api(
            self.health_check,
            "/health",
            "GET",
            function_description="Perform a health check on the API",
        )

    def _add_function_to_api(
        self,
        function: Callable,
        route_path: str,
        method: HttpMethod,
        function_name: str = "<lambda>",
        function_description: str = "-",
        using_cache: bool = False,
        max_retries: int = 1_000_000,
    ) -> Union[FastApiBuilder, None]:
        """Function to add a function to the API.

        Args:
            function (Callable) The function to wrap with the API.
            route_path (str): The API path to the function.
            method (HttpMethod): The HTTP method to use for the API.
            function_name (str): The name of the function (for the API documentation). Defaults to "<lambda>".
            function_description (str): The description of the function (for the API documentation). Defaults to "-".
            using_cache (bool): Use the `lru_cache` decorator on the function. Defaults to False.
            max_retries (int, optional): The maximum number of call for this function. Defaults to 1_000_000.

        Returns:
            Union[FastApiBuilder, None]: The modified instance or None if inplace is True.
        """
        if function.__name__ == "<lambda>":
            function.__name__ = function_name

        # Add the new route to the list of routes
        function_name = (
            function_name
            if hasattr(function, "__name__") and function.__name__ == "<lambda>"
            else function.__name__
        )
        self._routes[function_name] = CustomRoute(
            route_path,
            function_name,
            method,
            function.__doc__
            if function.__doc__ is not None and function_description == "-"
            else function_description,
            max_calls=max_retries,
        )
        if method == "GET":
            # Add the new route to the FastAPI router
            self.__app_router.add_api_route(
                path=route_path,
                endpoint=ApiLogger(self.__log_paths, "Calling function")(
                    self.handle_exceptions(
                        self.max_retries(function)
                        if using_cache is False
                        else lru_cache(maxsize=16)(self.max_retries(function))
                    )
                ),
                methods=[method],
                description=function_description,
            )
        elif method == "POST":
            self.__app_router.add_api_route(
                path=route_path,
                endpoint=ApiLogger(self.__log_paths, "Calling function")(
                    self.handle_exceptions(
                        self.max_retries(function)
                        if using_cache is False
                        else lru_cache(maxsize=16)(self.max_retries(function))
                    )
                ),
                methods=[method],
                description=function_description,
            )
        else:
            raise NotImplementedError(f"Method {method} not supported")

    def start_api(self) -> None:
        """Start the API."""
        self._add_function_to_api(
            self._get_routes,
            "/functions",
            "GET",
            function_description="Get the list of functions",
        )
        self.__app.include_router(self.__app_router)

        uvicorn.run(
            self.__app,
            host=self.host,
            port=self.port,
        )

    def __new__(cls, *args, **kwargs) -> Self:
        """Singleton pattern for the FastApiBuilder.

        Returns:
            Self: The unique FastApiBuilder instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
