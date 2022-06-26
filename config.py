# Hacky way to scale the image
SCALE = 15.0

# Sideways paper for now
DEFAULT_WIDTH = 110*SCALE
#DEFAULT_HEIGHT = 85*SCALE
DEFAULT_HEIGHT = 85*SCALE

# Stright from wikipedia lol
BASE_HEADER = """
<svg width="{width}" height="{width}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n
"""

# Numeric values are stored as proportions of larger element, kinda like css
DEFAULT_SCOREBOOK = {

        "margin": .01,

        # Scorecard grid is base location, consider it global
        "grid_x0": .22,
        "grid_x1": .9,
        "grid_y0": .2,
        "grid_y1": .8,

        # Label size for everything even with scorecard (scorecard, player
        # names, counting stats
        "label_h": .03,

        # Scorecard grid specifis
        "isCount": True,
        "isBases": True,
        "Bases_prop": .75, # Have to be less than .95
        "numInnings": 10,
        "numBatters": 9,
        # How big count boxes are as proportion
        "count_size":.1,
        # Where is play text top left?
        "where_text_x": -.06,
        "where_text_y": .48,
        # Offset to get outs in center of diamond
        "center_offset": .15,

        # Player name grid specifics
        "numSubs": 2,
        "is_player_margin": 0,
        "pname_cell_size": 0.7,

        # Counting stats
        "counting_stats": ["R", "H", "LOB"],
        "is_sum_margin": 0,
}

