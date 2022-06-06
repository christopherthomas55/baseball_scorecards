import config
from SVG_base import SVGBase

class Scorebook(SVGBase):
    # Inherits add_SHAPE and save
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.options = kwargs

        #TODO - Fill with default, not replace
        if not self.options:
            self.options = config.DEFAULT_SCOREBOOK

        self._gen_grid()
        self._gen_player_names()
        self._gen_counting_stats()

        self._gen_pitching_stats()
        self._gen_meta_stats()

    def _gen_grid(self):
        numInnings = self.options["numInnings"]
        numBatters = self.options["numBatters"]

        grid_start_x = self.options["grid_x0"]*self.width
        grid_end_x   = self.options["grid_x1"]*self.width
        grid_start_y = self.options["grid_y0"]*self.height
        grid_end_y   = self.options["grid_y1"]*self.height
        cell_x_size  = (grid_end_x - grid_start_x)/float(numInnings)
        cell_y_size  = (grid_end_y - grid_start_y)/float(numBatters)


        # Generate in order of use, for ease in future
        for x in range(numInnings):
            for y in range(numBatters):
                self._add_ab_cell(
                        grid_start_x + x*cell_x_size,
                        grid_start_x + (x+1)*cell_x_size,
                        grid_start_y + y*cell_y_size,
                        grid_start_y + (y+1)*cell_y_size
                )

    # TODO - THink about making square
    def _add_ab_cell(self, x0, x1, y0, y1):
        self.add_rect({"fill":"white", "fill-opacity":"0.0", "width":str(x1-x0),
            "height":str(y1-y0), "stroke":"black", "x":str(x0), "y":str(y0)})


        # Diamond is always a diamond not rhombus
        max_height = self.options["Bases_prop"]*(y1-y0)
        max_width  = self.options["Bases_prop"]*(x1-x0)
        diamond_size = min(max_height, max_width)

        # Aligning diamond based of max height and width allowed
        # If scoresheet grids aren't very square may have issues
        d_center_x = x1 - diamond_size/2.0 - (x1 - x0)*.05
        d_center_y = y1 - diamond_size/2.0 - (y1 - y0)*.05

        polyline_points = ""
        # Home
        polyline_points += str(d_center_x) + "," + str(d_center_y + diamond_size/2.0) + " "
        # 1st
        polyline_points += str(d_center_x + diamond_size/2.0)+ "," + str(d_center_y)  + " "
        # 2rd
        polyline_points += str(d_center_x) + "," + str(d_center_y - diamond_size/2.0) + " "
        # 3rd
        polyline_points += str(d_center_x - diamond_size/2.0)+ "," + str(d_center_y)  + " "
        # Home again
        polyline_points += str(d_center_x) + "," + str(d_center_y + diamond_size/2.0) + " "

        self.add_polyline({"fill":"none", "stroke": "black", "points": polyline_points})






    def _gen_player_names(self):
        pass

    def _gen_counting_stats(self):
        pass

    def _gen_pitching_stats(self):
        pass

    def _gen_meta_stats(self):
        pass



if __name__ == "__main__":
    test = Scorebook()
    test.save("blank_scorebook.svg")
