from config import ANIMATED
from ABCell import ABCell
RUNNER_VERBOSE = True
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
        safe_runners = [x for x in runners if (x["movement"]["isOut"] is False)]

        def null_to_0B(s):
            if s is None:
                return "0B"
            return s

        # Find where each runnerid goes. Gets start, end and out
        runner_map = {}
        for x in all_runners:
            r_id = x['details']['runner']['id']
            if r_id not in runner_map:
                runner_map[r_id] = {'start': destinations[null_to_0B(x['movement']['originBase'])],
                                    'end': destinations[null_to_0B(x['movement']['end'])],
                                    'out': x['movement']['isOut']
                                   }
            else:
                runner_map[r_id]['start'] = min(runner_map[r_id]['start'], destinations[null_to_0B(x['movement']['originBase'])])
                runner_map[r_id]['end'] = max(runner_map[r_id]['end'], destinations[null_to_0B(x['movement']['end'])])
                runner_map[r_id]['out'] = runner_map[r_id]['out'] or x['movement']['isOut']


        new_bases = [None, None, None, None]
        # If not in above runner_map this is a no movement andpass through
        for i in range(4):
            if i not in {runner_map[x]['start'] for x in runner_map.keys()}:
                new_bases[i] = self.bases[i]

        if RUNNER_VERBOSE:
            print("------------------- \n")
            print(all_runners)
            print(self.bases)
            print(runner_map)

        # Move runners. Some strikeouts show up here so we check end vs start
        # Also add runs
        for mvmt in runner_map.keys():
            start = runner_map[mvmt]['start']
            end = runner_map[mvmt]['end']
            out = runner_map[mvmt]['out']
            if end != start:
                self.bases[start].add_movement(start, end, out)

            if end == 4 and not out:
                self.bases[start].add_run()

        # Filter runners still on bases
        runner_map = {x:runner_map[x] for x in runner_map.keys() if not
                runner_map[x]['out'] and runner_map[x]['end'] <= 3}

        for mvmt in runner_map.keys():
            basenum = runner_map[mvmt]['start']
            endbase = runner_map[mvmt]['end']
            new_bases[endbase] = self.bases[basenum]

        self.bases = new_bases
        return sum([1 for x in self.bases if x]), len([x for x in safe_runners if destinations[x["movement"].get("end", 0)] == 4])


    def handle_inning_totals(self, inning_no, runs, outs, numRunners):
        self.inning_runs[inning_no] += runs
        if outs >= 3:
            self.inning_lob[inning_no] = numRunners - runs
            # TODO - Lots of constans here...
            x0 = self.grid_pointer.x0
            x1 = self.grid_pointer.x1
            y0 = self.summary_y
            y1 = self.summary_y + self.summary_height*.8
            text =  "Runs: " + str(self.inning_runs[inning_no]) + "  "
            self.parent._add_text(text, x0, x1, y0, y1)
            text = "LOB : " + str(self.inning_lob[inning_no]) + "\n"
            self.parent._add_text(text, x0, x1, y1, y1)


    def _add_label(self, label, x0, x1, y0, y1):
        self.add_rect({"fill":"white", "fill-opacity":"0.0", "width":str(x1-x0),
            "height":str(y1-y0), "stroke":"black", "x":str(x0), "y":str(y0)}
        )


    def gen(self):
        grid_pointer = 0
        outs = 0
        inning = 1
        looped = 0
        manfred_extra_runner = -1
        for count, play in enumerate(self.json['liveData']['plays']['allPlays']):
            isTop = self.parent.home_away == "away"
            if play['result']['type'] == 'atBat' and (play['about']['isTopInning'] == isTop):
                if manfred_extra_runner > 0:
                    self.bases = [None, None, None, None]
                    self.bases[2] = self.all_abs[manfred_extra_runner]
                    self.bases[2].gen_diamond()
                    manfred_extra_runner = -1

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

                        # Extras in 2020
                        # TODO - get year
                        year = 2022
                        playoffs = False
                        if inning >= 10 and year in [2020, 2021, 2022] and not playoffs:
                            manfred_extra_runner = grid_pointer + 9

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
