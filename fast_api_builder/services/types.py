from dataclasses import dataclass, field
from typing import Literal
from collections import namedtuple

HttpMethod = Literal["GET", "POST", "PUT", "DELETE"]


@dataclass
class CustomRoute:
    route_path: str
    function_name: str
    http_method: HttpMethod
    description: str = field(default="-")
