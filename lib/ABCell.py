play_map = {
    "walk": "BB",
    "single": "1B",
    "double": "2B",
    "triple": "3B",
    "home_run":"HR",
    "strikeout": "K",
}

class ABCell(object):
    def __init__(self, parent, x0, x1, y0, y1):
        self.parent = parent
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.cell_w = self.x1 - self.x0


        parent.add_rect({"fill":"white", "fill-opacity":"0.0", "width":str(x1-x0),
            "height":str(y1-y0), "stroke":"black", "x":str(x0), "y":str(y0)})


    def gen_diamond(self):
        # Diamond is always a diamond not rhombus
        max_height = self.parent.options["Bases_prop"]*(self.y1-self.y0)
        max_width  = self.parent.options["Bases_prop"]*(self.x1-self.x0)
        diamond_size = min(max_height, max_width)

        # Aligning diamond based of max height and width allowed
        # If scoresheet grids aren't very square may look weird

        # TODO - Fix this to be a config numbery have issues
        self.d_center_x = self.x1 - diamond_size/2.0 - (self.x1 - self.x0)*.15
        self.d_center_y = self.y1 - diamond_size/2.0 - (self.y1 - self.y0)*.15

        d_center_x = self.d_center_x
        d_center_y = self.d_center_y

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

        # Hack to store for later
        self.diamond = polyline_points
        self.parent.add_polyline({"fill":"none", "stroke": "black", "points": polyline_points})


    def add_run(self):
        self.parent.add_polyline({"fill": "black", "opacity": ".6", "stroke":
            "black", "points": self.diamond})

    def add_text(self, text):
        self.parent._add_text(text, self.x0, self.x1, self.y0, self.y1)

    def add_play(self, play):
        play_code = play['result']["eventType"]
        text = play_map.get(play_code, play_code)

        if play["about"]["hasOut"]:
            # Second x and y don't do anyhing
            self.parent._add_text(text, self.d_center_x - self.parent.options["center_offset"]*self.cell_w, self.d_center_x, self.d_center_y, self.d_center_y)

            out_num = (str(play['runners'][-1]['movement']['outNumber']))
            x = (self.d_center_x + self.x1 -.10*(self.x1 - self.x0))/2.0 # TODO - Fix .05 stranded
            y = (self.d_center_y + self.y0 + .02*(self.y1 - self.y0))/2.0
            self.parent._add_text(out_num, x, x, y, y)

            # center x, center y, radius x, radius y
            x = (self.d_center_x + self.x1 +  .16*(self.x1 - self.x0))/2.0 # TODO - Fix .05 stranded
            y = (self.d_center_y + self.y0 -.15*(self.y1 - self.y0))/2.0

            self.parent._add_ellipse(x, y, (self.x1 - self.x0)*.1, (self.x1 -
                self.x0)*.1, fill = "black", opacity = ".22")


        else:
            # Second x0 and y0 doesn't do anyhing
            self.parent._add_text(text, self.x0 + (self.x1-self.x0)*self.parent.options["where_text_x"], self.x0, self.y0 + (self.y1 - self.y0)*self.parent.options["where_text_y"], self.y0 )


    def add_count(self, count):
        self.balls = count["balls"]
        self.strikes = count["strikes"]

        self.balls = min(self.balls, 3)
        self.strikes = min(self.strikes, 2)

        cbox_w = (self.x1-self.x0)*self.parent.options["count_size"]
        cbox_h = (self.y1-self.y0)*self.parent.options["count_size"]

        # Balls on bottom
        for i in range(3):
            opacity = 0.0
            fill = "white"
            if i < self.balls:
                fill = "grey"
                opacity = str(1.0)
            self.parent.add_rect({"fill": fill, "fill-opacity":opacity, "width":str(cbox_w),
            "height":str(cbox_h), "stroke":"black", "x":str(self.x0 + cbox_w*i), "y":str(self.y1 - cbox_h)})

        for i in range(2):
            opacity = 0.0
            fill = "white"
            if i < self.strikes:
                fill = "grey"
                opacity = str(1.0)
            self.parent.add_rect({"fill": fill, "fill-opacity":opacity, "width":str(cbox_w),
            "height":str(cbox_h), "stroke":"black", "x":str(self.x0 + cbox_w*i), "y":str(self.y1 - 2*cbox_h)})
