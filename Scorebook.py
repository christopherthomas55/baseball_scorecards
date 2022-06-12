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
            self._add_label(str(x), grid_start_x + x*cell_x_size,
                    grid_start_x + (x+1)*cell_x_size,
                    grid_start_y - self.height*self.options["label_h"],
                    grid_start_y
            )

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

    def _add_label(self, label, x0, x1, y0, y1):
        self.add_rect({"fill":"white", "fill-opacity":"0.0", "width":str(x1-x0),
            "height":str(y1-y0), "stroke":"black", "x":str(x0), "y":str(y0)})

        self.add_text(label, {"x":str(x0), "y":str(y1), "textLength":str(x1-x0)})
        pass

    # TODO - Reused code from genning the innings grid
    # All based on center, the scorecard
    def _gen_player_names(self):
        grid_start_x = self.options["margin"]*self.width
        grid_end_x   = (self.options["grid_x0"] - self.options["is_player_margin"]*self.options["margin"])*self.width
        grid_start_y = self.options["grid_y0"]*self.height
        grid_end_y   = self.options["grid_y1"]*self.height
        numBatters = self.options["numBatters"]

        cell_y_size  = (grid_end_y - grid_start_y)/float(numBatters)

        number_x = grid_start_x + (grid_end_x - grid_start_x)*((1 - self.options['pname_cell_size'])/2.0)
        position_x = grid_end_x - (grid_end_x - grid_start_x)*((1 - self.options['pname_cell_size'])/2.0)

        self._add_label("#", grid_start_x,
                number_x,
                grid_start_y - self.height*self.options["label_h"],
                grid_start_y
        )

        self._add_label("PO", position_x,
                grid_end_x,
                grid_start_y - self.height*self.options["label_h"],
                grid_start_y
        )

        self._add_label("Player", number_x,
                position_x,
                grid_start_y - self.height*self.options["label_h"],
                grid_start_y
        )
        # Generate in order of use, for ease in future
        for y in range(numBatters):
            self._add_cell(
                grid_start_x,
                grid_end_x,
                grid_start_y + y*cell_y_size,
                grid_start_y + (y+1)*cell_y_size
            )

            topy = grid_start_y + y*cell_y_size
            bottomy = grid_start_y + (y+1)*cell_y_size

            # First is pnumber
            self.add_line({'x1': str(number_x), 'x2': str(number_x), 'y1':str(topy), 'y2':str(bottomy), 'stroke': 'black'})
            # Second is pposition
            self.add_line({'x1': str(position_x), 'x2': str(position_x), 'y1':str(topy), 'y2':str(bottomy), 'stroke': 'black'})


    def _add_cell(self, x0, x1, y0, y1):
        numSubs = self.options["numSubs"]
        for count in range(numSubs):
            self.add_rect({"fill":"white", "fill-opacity":"0.0", "width":str(x1-x0),
                "height":str((y1-y0)/float(numSubs)), "stroke":"black",
                "x":str(x0), "y":str(y0 + count*(y1-y0)/numSubs)})


    def _gen_counting_stats(self):
        # ODO - Reused code from genning the innings grid
        # All based on center, the scorecard
        grid_start_x = (self.options["grid_x1"] + self.options["is_sum_margin"]*self.options["margin"])*self.width
        grid_end_x   = (1 - self.options["margin"])*self.width
        grid_start_y = self.options["grid_y0"]*self.height
        grid_end_y   = self.options["grid_y1"]*self.height
        numBatters = self.options["numBatters"]

        cell_y_size  = (grid_end_y - grid_start_y)/float(numBatters)

        num_stats = len(self.options['counting_stats'])
        # Labels and counting stat cells generated dynamically unlike player
        # stuff
        lines_x = [grid_start_x + (grid_end_x - grid_start_x)*(x+1)/float(num_stats) for x in range(num_stats)]
        prev = grid_start_x
        for x in range(num_stats):
            self._add_label(self.options["counting_stats"][x], prev,
                    lines_x[x],
                    grid_start_y - self.height*self.options["label_h"],
                    grid_start_y
            )
            prev = lines_x[x]


        cell_y_size  = (grid_end_y - grid_start_y)/float(numBatters)
        # Generate in order of use, for ease in future
        for y in range(numBatters):
            self._add_cell(
                grid_start_x,
                grid_end_x,
                grid_start_y + y*cell_y_size,
                grid_start_y + (y+1)*cell_y_size
            )
            for l in lines_x:
                self.add_line({'x1': str(l), 'x2': str(l), 'y1':str(grid_start_y + y*cell_y_size), 'y2':str(grid_start_y + (y+1)*cell_y_size), 'stroke': 'black'})

    def _gen_pitching_stats(self):
        pass

    def _gen_meta_stats(self):
        pass



if __name__ == "__main__":
    test = Scorebook()
    test.save("blank_scorebook.svg")
