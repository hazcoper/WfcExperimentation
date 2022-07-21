from wfc import WaveFunctionCollapse

CONFIG = {
	"clean_edges": False,
	"overlapping": False,
	"color_divider": 1,
	"tiles": [
		{
			"filename": "./tiles/subway/connector.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": True,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/subway/orange.png",
			"rotate90": True,
			"rotate180": True,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
		{
			"filename": "./tiles/subway/red.png",
			"rotate90": True,
			"rotate180": False,
			"rotate270": False,
			"flip_vertical": False,
			"flip_horizontal": False,
		},
	]
}

OUTPUT_FILE = "subway.png"
TILESHEET_FILE = "subway-tilesheet.png"

X_TILES = 5
Y_TILES = 5

def main():
	wfc = WaveFunctionCollapse(silent = False)
	wfc.load_config(CONFIG)
	wfc.create_tilesheet(TILESHEET_FILE)
	wfc.collapse(X_TILES, Y_TILES)
	wfc.save(OUTPUT_FILE)

if __name__ == "__main__":
	main()
