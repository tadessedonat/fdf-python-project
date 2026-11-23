import math

from fdf.model import MapData


def project_point(
    x: int,
    y: int,
    z: int,
    scale: float,
    z_scale: float
) -> tuple[float, float]:
    angle = math.radians(30)

    projected_x = (x - y) * math.cos(angle)
    projected_y = (x + y) * math.sin(angle) - z * z_scale

    screen_x = projected_x * scale
    screen_y = projected_y * scale

    return screen_x, screen_y


class Camera:
    def __init__(
        self,
        scale: float,
        z_scale: float,
        offset_x: float,
        offset_y: float
    ) -> None:
        self.scale = scale
        self.z_scale = z_scale
        self.offset_x = offset_x
        self.offset_y = offset_y

    def transform(
        self,
        x: int,
        y: int,
        z: int
    ) -> tuple[float, float]:
        screen_x, screen_y = project_point(
            x,
            y,
            z,
            self.scale,
            self.z_scale
        )

        screen_x += self.offset_x
        screen_y += self.offset_y

        return screen_x, screen_y

    @classmethod
    def fit(
        cls,
        map_data: MapData,
        window_width: int,
        window_height: int
    ) -> "Camera":
        projected_points = []

        for row in map_data.points:
            for point in row:
                x, y = project_point(
                    point.x,
                    point.y,
                    point.z,
                    1.0,
                    1.0
                )
                projected_points.append((x, y))

        min_x = min(point[0] for point in projected_points)
        max_x = max(point[0] for point in projected_points)
        min_y = min(point[1] for point in projected_points)
        max_y = max(point[1] for point in projected_points)

        map_width = max(max_x - min_x, 1.0)
        map_height = max(max_y - min_y, 1.0)

        scale_x = window_width * 0.9 / map_width
        scale_y = window_height * 0.9 / map_height
        scale = min(scale_x, scale_y)

        offset_x = window_width / 2 - ((min_x + max_x) / 2) * scale
        offset_y = window_height / 2 - ((min_y + max_y) / 2) * scale

        return cls(
            scale=scale,
            z_scale=1.0,
            offset_x=offset_x,
            offset_y=offset_y
        )