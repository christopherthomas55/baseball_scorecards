# Hacky way to scale the image
SCALE = 15.0

# Sideways paper for now
DEFAULT_WIDTH = 110*SCALE
DEFAULT_HEIGHT = 85*SCALE

# Stright from wikipedia lol
BASE_HEADER = """
<svg width="{width}" height="{width}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n
"""

# Numeric values are stored as proportions of larger element, kinda like css
DEFAULT_SCOREBOOK = {
        # Scorecard grid
        "grid_x0": .2,
        "grid_x1": .9,
        "grid_y0": .2,
        "grid_y1": .8,
        "isCount": True,
        "isBases": True,

        # Have to be less than .95
        "Bases_prop": .75,
        "numInnings": 10,
        "numBatters": 9,
}
