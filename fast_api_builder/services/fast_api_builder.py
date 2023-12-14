from __future__ import annotations
from abc import ABC, abstractmethod
from functools import cached_property, lru_cache
from typing import Any, Callable, Final, Iterable, List, Optional, Self, Union
from fastapi import APIRouter, FastAPI
import uvicorn
from services.types import CustomRoute, HttpMethod


class FastApiBuilderCore(ABC):
    @abstractmethod
    def add_function_to_api():
        pass

    @abstractmethod
    def start_api():
        pass


class FastApiBuilderUtility:
    _routes: list[CustomRoute] = []
    __HOST: Final[str] = "0.0.0.0"
    __port: int = 8000

    @staticmethod
    def health_check() -> str:
        return "up & running"

    @cached_property
    def host(self) -> str:
        return self.__HOST

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, port: Union[str, int]) -> None:
        self.__port = int(port)

    @property
    def routes(self) -> list[CustomRoute]:
        return self._routes

    def _get_routes(self):
        return self.routes


class FastApiBuilder(FastApiBuilderCore, FastApiBuilderUtility):
    _instance = None

    def __init__(
        self,
    ) -> None:
        self.__app = FastAPI()
        self.__app_router = APIRouter()

        self.add_function_to_api(
            self.health_check,
            "/health",
            "GET",
            function_description="Perform a health check on the API",
        )

    def add_function_to_api_decorator(
        self,
        route_path: str,
        method: HttpMethod,
        function_name: str = "<lambda>",
        function_description: str = "-",
        using_cache: bool = False,
    ) -> Callable:
        """Decorator function that add a function to the API routes.

        Args:
            route_path (str): The API path to the function.
            method (HttpMethod): The HTTP method to use for the API.
            function_name (str): The name of the function (for the API documentation). Defaults to "<lambda>".
            function_description (str): The description of the function (for the API documentation). Defaults to "-".
            using_cache (bool): Use the `lru_cache` decorator on the function. Defaults to False.
        Returns:
            Callable: The modified instance or None if inplace is True.
        """

        def decorator(func: Callable) -> Callable:
            self.add_function_to_api(
                function=func,
                route_path=route_path,
                method=method,
                function_name=function_name,
                function_description=function_description,
                using_cache=using_cache,
            )
            return func

        return decorator

    def add_function_to_api(
        self,
        function: Callable[[Union[Any, None]], Union[Any, Iterable[Any]]],
        route_path: str,
        method: HttpMethod,
        function_name: str = "<lambda>",
        function_description: str = "-",
        using_cache: bool = False,
    ) -> Union[FastApiBuilder, None]:
        """Function to add a function to the API.

        Args:
            function (Callable[[Union[Any, None]], Union[Any, Iterable[Any]]]) The function to wrap with the API.
            route_path (str): The API path to the function.
            method (HttpMethod): The HTTP method to use for the API.
            function_name (str): The name of the function (for the API documentation). Defaults to "<lambda>".
            function_description (str): The description of the function (for the API documentation). Defaults to "-".
            using_cache (bool): Use the `lru_cache` decorator on the function. Defaults to False.
        Returns:
            Union[FastApiBuilder, None]: The modified instance or None if inplace is True.
        """

        # Add the new route to the list of routes
        self._routes.append(
            CustomRoute(
                route_path,
                function_name
                if hasattr(function, "__name__") and function.__name__ == "<lambda>"
                else function.__name__,
                method,
                function.__doc__
                if function.__doc__ is not None and function_description == "-"
                else function_description,
            )
        )
        # Add the new route to the FastAPI router
        self.__app_router.add_api_route(
            path=route_path,
            endpoint=function
            if using_cache is False
            else lru_cache(maxsize=16)(function),
            methods=[method],
            description=function_description,
        )

    def start_api(self) -> None:
        """Start the API."""
        self.add_function_to_api(
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
            # workers=4,
            # reload=True,
        )

    def __new__(cls, *args, **kwargs) -> Self:
        """Singleton pattern for the FastApiBuilder.

        Returns:
            Self: The unique FastApiBuilder instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
