from config import ANIMATED
from ABCell import ABCell

class ABCellHolder(object):
    def __init__(self, parent):
        self.all_abs = []
        self.parent = parent
        self.json = None
        # TO do - set to parent num innings
        self.inning_runs = {x: 0 for x in range(1,30)}
        self.inning_lob = {x: 0 for x in range(1, 30)}
        self.current_inning = None

        # Pointers to AB cell are stored below......batter is at 0 and bases
        # are 1-3
        self.bases = [None, None, None, None]

    def _add_ab_cell(self, *args):
        self.all_abs.append( ABCell(*args) )

    def add_json(self, json):
        self.json = json

    #TODO - Lots needed here.....fixed some ugliness but lots of artifacts
    def handle_runners(self, runners):
        # 4B when fielder's choice to end inning
        destinations = {"1B": 1, "2B": 2, "3B": 3, "score": 4, "4B": 4, "0B":0}   # This is the hackiest thing ever to add

        all_runners = runners
        runners = [x for x in runners if (x["movement"]["isOut"] is False)]

        # Sorting to start with highest bases first
        runners = sorted(runners, key= lambda x: -destinations[x["movement"]["end"]])

        # TODO - Messy
        # This draws the  lines
        # To handle plays with multiple movemens we draw lines then move runners
        for runner in all_runners:
            start = destinations.get(runner["movement"]["originBase"], 0)
            if not runner["movement"]["isOut"]:
                if not runner["movement"]["end"]:
                    continue
                end = destinations[runner["movement"]["end"]]
            else:
                end = destinations[runner["movement"]["outBase"]]
            self.bases[start].add_movement(start, end, runner["movement"]["isOut"])

        # This handles adding runs
        for runner in runners:
            start = destinations.get(runner["movement"]["originBase"], 0)
            end = destinations[runner["movement"]["end"]]
            if end == 4 and not runner["movement"]["isOut"]:
                self.bases[start].add_run()

        # TODO - I don't think this handles double steals, see above
        # This moves the runners around bases
        def null_to_0B(s):
            if s is None:
                return "0B"
            return s

        # Get runners -> loc or isout map. 99 is counted as out
        baseMap = {}
        for x in all_runners:
            basenum = destinations[null_to_0B(x["movement"]["originBase"])]
            endbase = destinations[null_to_0B(x["movement"]["end"])]
            if x["movement"]["isOut"]:
                baseMap[basenum] = 99
            baseMap[basenum] = max(endbase, baseMap.get(basenum, -1))

        new_bases = [None, None, None, None]
        for i in range(4):
            if i not in baseMap:
                new_bases[i] = self.bases[i]

        for rm, val in baseMap.items():
            if val < 4:
                new_bases[val] = self.bases[rm]

        self.bases = new_bases
        return sum([1 for x in self.bases if x]), len([x for x in runners if destinations[x["movement"]["end"]] == 4])


    def handle_inning_totals(self, inning_no, runs, outs, numRunners):
        self.inning_runs[inning_no] += runs
        if outs >= 3:
            self.inning_lob[inning_no] = numRunners - runs
            # TODO - Lots of constans here...
            x0 = self.grid_pointer.x0
            x1 = self.grid_pointer.x1
            y0 = self.all_abs[8].y0 + 100
            y1 = self.all_abs[8].y1 + 100
            text =  "Runs: " + str(self.inning_runs[inning_no]) + "  "
            self.parent._add_label(text, x0, x1, y0, y1)
            text = "LOB: " + str(self.inning_lob[inning_no]) + "\n"
            self.parent._add_label(text, x0, x1, y0+100, y1+100)


    def _add_label(self, label, x0, x1, y0, y1):
        self.add_rect({"fill":"white", "fill-opacity":"0.0", "width":str(x1-x0),
            "height":str(y1-y0), "stroke":"black", "x":str(x0), "y":str(y0)}
        )


    def gen(self):
        grid_pointer = 0
        outs = 0
        inning = 1
        looped = 0
        for count, play in enumerate(self.json['liveData']['plays']['allPlays']):
            isTop = self.parent.home_away == "away"
            if play['result']['type'] == 'atBat' and (play['about']['isTopInning'] == isTop):
                self.all_abs[grid_pointer].add_count(play['count'])
                self.all_abs[grid_pointer].gen_diamond()
                if play['result'].get('eventType'):
                    self.all_abs[grid_pointer].add_play(play)
                    # "Add" batter to start of bases
                    self.bases[0] = self.all_abs[grid_pointer]
                    (numRunners, num_runs) = self.handle_runners(play["runners"])

                    if play['about']['hasOut']:
                        all_outs_here = [x['movement']['outNumber'] for x in play['runners']]
                        outs = max([x for x in all_outs_here if x])

                    # TODO fix numRunners issues
                    self.grid_pointer = self.all_abs[grid_pointer]
                    self.handle_inning_totals(inning, num_runs, outs, numRunners)

                    # TODO - Runs when 3rd out after not counted
                    if outs != 3:
                        pass

                    if outs == 3:
                        self.bases = [None, None, None, None]
                        outs = 0
                        inning += 1
                        if (grid_pointer+1)%9 == 0:
                            grid_pointer += 1
                        else:
                            grid_pointer += 10

                    elif ((grid_pointer+1)%9 == 0) and outs < 3: # to be explicit
                        grid_pointer -= 8
                        # Not testing looped yet but good to track
                        looped += 1
                    else:
                        grid_pointer += 1

                    if ANIMATED:
                        raise Exception("Not implemented yet after directory change")
                        sleep(self.parent.options['wait_time'])
