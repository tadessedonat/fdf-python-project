
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
        self.drag_start: tuple[int, int] | None = None

        self.canvas.bind("<MouseWheel>", self.zoom)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan)

        self.draw_map()

    def draw_map(self) -> None:
        self.canvas.delete("all")
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

    def zoom(self, event: tk.Event) -> None:
        factor = 1.1 if event.delta > 0 else 1 / 1.1

        new_scale = self.camera.scale * factor

        if not 0.1 <= new_scale <= 10000:
            return

        mouse_x = event.x
        mouse_y = event.y

        self.camera.offset_x = (
            mouse_x - (mouse_x - self.camera.offset_x) * factor
        )
        self.camera.offset_y = (
            mouse_y - (mouse_y - self.camera.offset_y) * factor
        )
        self.camera.scale = new_scale

        self.draw_map()

    def start_pan(self, event: tk.Event) -> None:
        self.drag_start = (event.x, event.y)

    def pan(self, event: tk.Event) -> None:
        if self.drag_start is None:
            return

        old_x, old_y = self.drag_start

        delta_x = event.x - old_x
        delta_y = event.y - old_y

        self.camera.offset_x += delta_x
        self.camera.offset_y += delta_y

        self.drag_start = (event.x, event.y)

        self.draw_map()

    def run(self) -> None:
        self.root.mainloop()
