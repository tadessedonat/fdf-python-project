

# FdF - Wireframe Viewer

## About

FdF is a Python project that displays a 3D wireframe representation of a map using isometric projection.

The map is read from a `.fdf` file containing height values.

## Features

- Reads `.fdf` map files.
- Parses height values and optional colors.
- Displays maps using isometric projection.
- Draws a wireframe using connected points.
- Supports zooming and panning.
- Supports top view mode.

## Requirements

- Python 3.13

## Usage

Run the application from the project directory:

```bash
python3.13 main.py test.fdf
```

Replace `test.fdf` with the path to your map file.

## Controls

- **Mouse wheel:** Zoom in and out.
- **Left mouse button + drag:** Move the map.
- **T:** Toggle between isometric view and top view.

