
import sys

from fdf.app import FdfApp
from fdf.parser import FdfError, parse_map


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python main.py <map.fdf>", file=sys.stderr)
        return 2

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            map_data = parse_map(file.read())
    except (OSError, FdfError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    app = FdfApp(map_data)
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
