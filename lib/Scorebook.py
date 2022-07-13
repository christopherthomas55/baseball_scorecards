import json
import sys
from time import sleep
import config
from SVG_base import SVGBase
from ABCellHolder import ABCellHolder
from war_calc import war_calc


class Scorebook(SVGBase):
    # Inherits add_SHAPE and save
    def __init__(self, home_away, *args, **kwargs):
        super().__init__()
        self.options = kwargs
        self.ABs = ABCellHolder(parent=self)
        self.home_away = home_away

        #TODO - Fill with default, not replace
        if not self.options:
            self.options = config.DEFAULT_SCOREBOOK

        with open('data/live_data.json', 'r') as f:
            self.json = json.load(f)

        self.ABs.add_json(self.json)

        self._gen_grid()
        self._gen_player_names()
        self._gen_counting_stats()

        self._gen_pitching_stats()
        self._gen_meta_stats()
        self.ABs.gen()

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
            self._add_label(str(x+1), grid_start_x + x*cell_x_size,
                    grid_start_x + (x+1)*cell_x_size,
                    grid_start_y - self.height*self.options["label_h"],
                    grid_start_y
            )

            for y in range(numBatters):
                self.ABs._add_ab_cell(
                        self,
                        grid_start_x + x*cell_x_size,
                        grid_start_x + (x+1)*cell_x_size,
                        grid_start_y + y*cell_y_size,
                        grid_start_y + (y+1)*cell_y_size
                )

            # TODO move this elsewhere prob
            # TODO parameterize
            # This adds the summary a bottom
            height_prop = .8
            self.add_rect({"fill":"white", "fill-opacity":"0.0",
                "width":str(cell_x_size),
                "height":str(height_prop*cell_y_size),
                "x":str(grid_start_x + x*cell_x_size),
                "y":str(grid_start_y + (y+1)*cell_y_size),
                "stroke":"black"})
        self.ABs.summary_y = grid_start_y + (y+1)*cell_y_size
        self.ABs.summary_height = cell_y_size*height_prop


    def _add_label(self, label, x0, x1, y0, y1):
        self.add_rect({"fill":"white", "fill-opacity":"0.0", "width":str(x1-x0),
            "height":str(y1-y0), "stroke":"black", "x":str(x0), "y":str(y0)}
        )

        self.add_text(label, {"x":str(x0 + 10), "y":str((y1 + y0)/2.0),
            "dominant-baseline": "middle",
            "font-size": "x-large"
            #"textLength":str(x1-x0), "lengthAdjust": "spacingAndGlyphs",
            #"length-percentage":str(100)
            }
        )

        pass

    def _add_text(self, label, x0, x1, y0, y1):
        #import pdb; pdb.set_trace()
        self.add_text(label, {"x":str(x0 + 10), "y":str((y1 + y0)/2.0),
            "dominant-baseline": "middle",
            "font-size": "x-large"
            #"textLength":str(x1-x0), "lengthAdjust": "spacingAndGlyphs",
            #"length-percentage":str(100)
            }
        )


    def _add_ellipse(self, cx, cy, rx, ry, fill = "white", opacity = "0.05"):
        self.add_ellipse({'cx': cx, 'cy': cy, 'rx': rx, 'ry': ry, 'fill': fill, 'opacity': opacity})

    # TODO - Reused code from genning the innings grid
    # All based on center, the scorecard
    def _gen_player_names(self):

        # Location stuff
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

        batting_order = self.json['liveData']['boxscore']['teams'][self.home_away]['battingOrder']
        batting_names = [self.json['gameData']['players']['ID' + str(i)]['lastFirstName'] for i in batting_order]

        # JSON player name stuff

        # Generate in order of use, for ease in future
        for count, y in enumerate(range(numBatters)):
            self._add_cell(
                grid_start_x,
                grid_end_x,
                grid_start_y + y*cell_y_size,
                grid_start_y + (y+1)*cell_y_size
            )

            self._add_text(batting_names[count],
                grid_start_x + (grid_end_x - grid_start_x)*(1 - self.options['pname_cell_size'])/2.0,
                grid_start_x + (grid_end_x - grid_start_x)*(1 - self.options['pname_cell_size'])/2.0,
                grid_start_y + y*cell_y_size - self.height*self.options["label_h"],
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


    if config.ANIMATED:
        while True:
            away = Scorebook("away")
            away.save("img/away_scorebook.svg")
            json = away.json
            away_war_people = war_calc(json["home"]["runTotal"], json, json["lineup"])
            print(away_war_people)

    # Need to find every json call here f. Here I go
    # Done so far :  ---
    # Not done:      All

    # I gotta get them from the json at least. json["home']] might be list
    # comprehension though
    home = Scorebook("home")
    home.save("img/home_scorebook.svg")
    away = Scorebook("away")
    away.save("img/away_scorebook.svg")
    sys.exit()

    j = home.json
    runTotal  = j["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["batting"]["runs"]
    home_json = [x for x in j["liveData"]["plays"]["allPlays"] if not x["about"]["isTopInning"]]

    batting_order_ids = j["liveData"]["boxscore"]["teams"]["home"]["battingOrder"]
    player_metadata   =  0 # Needs something json["home"]["lineup"]

    player_metadata = j["gameData"]["players"]
    lineup = [player_metadata[x] for x in player_metadata]
    #print(lineup)

    home_war_people = war_calc(runTotal, home_json, lineup)
    out = [(x, home_war_people[x]) for x in home_war_people.keys()]
    out = sorted(out, key = lambda x: x[-1])
    for i in out:
        if i[1] >= 0:
            print("%s: %s \n"%(i[0], str(i[1])))

    j = away.json
    runTotal  = j["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["batting"]["runs"]
    away_json = [x for x in j["liveData"]["plays"]["allPlays"] if x["about"]["isTopInning"]]

    batting_order_ids = j["liveData"]["boxscore"]["teams"]["away"]["battingOrder"]
    lineup = [player_metadata[x] for x in player_metadata]

    away_war_people = war_calc(runTotal, away_json, lineup)
    out = [(x, away_war_people[x]) for x in home_war_people.keys()]
    out = sorted(out, key = lambda x: x[-1])
    for i in out:
        if i[1] >= 0:
            print("%s: %s \n"%(i[0], str(i[1])))
