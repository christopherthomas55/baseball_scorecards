from config import ANIMATED
from ABCell import ABCell

class ABCellHolder(object):
    def __init__(self, parent):
        self.all_abs = []
        self.parent = parent
        self.json = None

        # Pointers to AB cell are stored below......batter is at 0 and bases
        # are 1-3
        self.bases = [None, None, None, None]
        pass

    def _add_ab_cell(self, *args):
        self.all_abs.append( ABCell(*args) )

    def add_json(self, json):
        self.json = json

    #TODO - Lots needed here.....
    def handle_runners(self, runners):
        # 4B when fielder's choice
        destinations = {"1B": 1, "2B": 2, "3B": 3, "score": 4, "4B": 4}

        all_runners = runners
        runners = [x for x in runners if (x["movement"]["isOut"] is False)]
        maxOrigin = {}
        for x in runners:
            originBase = x["movement"]["originBase"]
            endBase = x["movement"]["end"]
            if originBase in maxOrigin:
                if destinations[endBase] > maxOrigin[originBase]:
                    maxOrigin[originBase] = destinations[endBase]
            else:
                maxOrigin[originBase] = destinations[endBase]
        # TODO - disgusting
        runners = [x for x in runners if maxOrigin.get(x["movement"]["originBase"], -1) == destinations[x["movement"]["end"]]]

        # Sorting to start with highest bases first

        runners = sorted(runners, key= lambda x: -destinations[x["movement"]["end"]])

        # TODO - Messy
        # To handle plays with multiple movemens we draw lines then move runners
        for runner in all_runners:
            start = destinations.get(runner["movement"]["originBase"], 0)
            if not runner["movement"]["isOut"]:
                end = destinations[runner["movement"]["end"]]
            else:
                end = destinations[runner["movement"]["outBase"]]
            self.bases[start].add_movement(start, end, runner["movement"]["isOut"])

        # TODO - I don't think this handles double steals, see above
        for runner in runners:
            start = destinations.get(runner["movement"]["originBase"], 0)
            end = destinations[runner["movement"]["end"]]

            if end == 4 and not runner["movement"]["isOut"]:
                self.bases[start].add_run()
            else:
                self.bases[end] = self.bases[start]

            self.bases[start] = None



    def gen(self):
        grid_pointer = 0
        outs = 0
        inning = 1
        looped = 0
        for play in self.json['liveData']['plays']['allPlays']:
            isTop = self.parent.home_away == "away"
            if play['result']['type'] == 'atBat' and (play['about']['isTopInning'] == isTop):
                self.all_abs[grid_pointer].add_count(play['count'])
                self.all_abs[grid_pointer].gen_diamond()
                if play['result'].get('eventType'):
                    self.all_abs[grid_pointer].add_play(play)
                    # "Add" batter to start of bases
                    self.bases[0] = self.all_abs[grid_pointer]
                    self.handle_runners(play["runners"])

                    if play['about']['hasOut']:
                        outs += 1

                    if "double_play" in play['result'].get('eventType').lower():
                        outs += 1

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
