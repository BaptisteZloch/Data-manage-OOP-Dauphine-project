from dataclasses import dataclass, field
from typing import Literal

HttpMethod = Literal["GET", "POST"]  # , "PUT", "DELETE"


@dataclass
class CustomRoute:
    route_path: str
    function_name: str
    http_method: HttpMethod
    description: str = field(default="-")
    n_calls: int = field(
        default=0,
    )
    max_calls: int = field(default=1_000_000)

    def update_calls(self) -> None:
        self.n_calls += 1
