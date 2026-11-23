from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Point:
    x: int
    y: int
    z: int
    color: Optional[str] = None


@dataclass
class MapData:
    points: List[List[Point]]
    width: int
    height: int