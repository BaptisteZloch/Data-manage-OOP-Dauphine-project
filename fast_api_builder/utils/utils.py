from functools import cached_property, wraps
from typing import Callable, Dict, Final, Union

from fast_api_builder.utils.types import CustomRoute


class FastApiBuilderUtility:
    _routes: Dict[str, CustomRoute] = {}
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
    def routes(self) -> Dict[str, CustomRoute]:
        return self._routes

    def _get_routes(self):
        return self.routes

    def max_retries(self, func: Callable) -> Callable:
        """The decorator function to limit the number of calls to a function.

        Args:
            func (Callable): The function to limit the number of calls.

        Raises:
            ValueError: The maximum number of calls has been reached.

        Returns:
            Callable: The wrapper for the function.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Increment the call count before calling the original function
            self._routes[func.__name__].update_calls()
            if (
                self._routes[func.__name__].n_calls
                > self._routes[func.__name__].max_calls
            ):
                raise ValueError(f"Max retries reached for function {func.__name__}")
            return func(*args, **kwargs)

        return wrapper

    def handle_exceptions(self, func: Callable) -> Callable:
        """Handle exceptions for the API.

        Args:
            func (Callable): The function to secure.

        Returns:
            Callable: The wrapper for exceptions handling.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Increment the call count before calling the original function
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return {"error": str(e)}

        return wrapper
