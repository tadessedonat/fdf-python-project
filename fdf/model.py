from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int
    z: int
    color: str | None = None


@dataclass
class MapData:
    points: list[list[Point]]
    width: int
    height: int