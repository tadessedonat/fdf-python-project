
import tkinter as tk

from fdf.model import MapData
from fdf.projection import Camera


class FdfApp:
    def __init__(
        self,
        map_data: MapData,
        width: int = 800,
        height: int = 600
    ) -> None:
        self.width = width
        self.height = height
        self.map_data = map_data

        self.root = tk.Tk()
        self.root.title("FdF - Wireframe Viewer")
        self.root.geometry(f"{width}x{height}")

        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            background="black",
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.camera = Camera.fit(map_data, width, height)
        self.draw_map()

    def draw_map(self) -> None:
        points = self.map_data.points

        for y, row in enumerate(points):
            for x, point in enumerate(row):
                current = self.camera.transform(
                    point.x, point.y, point.z
                )

                if x + 1 < self.map_data.width:
                    right_point = row[x + 1]
                    right = self.camera.transform(
                        right_point.x,
                        right_point.y,
                        right_point.z
                    )
                    self.draw_line(current, right, point.color)

                if y + 1 < self.map_data.height:
                    down_point = points[y + 1][x]
                    down = self.camera.transform(
                        down_point.x,
                        down_point.y,
                        down_point.z
                    )
                    self.draw_line(current, down, point.color)

    def draw_line(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        color: str | None = None
    ) -> None:
        line_color = color if color else "#FFFFFF"

        self.canvas.create_line(
            start[0], start[1],
            end[0], end[1],
            fill=line_color,
            width=2
        )

    def run(self) -> None:
        self.root.mainloop()
