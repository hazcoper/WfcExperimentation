from wfc import WaveFunctionCollapse

CONFIG = {
    "clean_edges": False,
    "overlapping": False,
    "color_divider": 1,
    "tiles": [
        {
            "filename": "./tiles/newSubway/vertical.png",
            "rotate90": True,
            "rotate180": False,
            "rotate270": False,
            "flip_vertical": False,
            "flip_horizontal": False,
        },
        {
            "filename": "./tiles/newSubway/leftToUp.png",
            "rotate90": True,
            "rotate180": True,
            "rotate270": True,
            "flip_vertical": False,
            "flip_horizontal": False,
        },
        {
            "filename": "./tiles/newSubway/blank.png",
            "rotate90": True,
            "rotate180": True,
            "rotate270": True,
            "flip_vertical": False,
            "flip_horizontal": False,
        },
    ]
}

OUTPUT_FILE = "subway.png"
TILESHEET_FILE = "subway-tilesheet.png"


def main():
    wfc = WaveFunctionCollapse(silent = False)
    wfc.load_config(CONFIG)
    wfc.create_tilesheet(TILESHEET_FILE)

if __name__ == "__main__":
    main()
