# Could always simulate more with fielding data
# But that isn't as elegant lol im lazy pls
from collections import defaultdict
EVENT_CACHE = {}

# n^2 maybe....ffffffffffffffffff may need c++, hope not. I can tolerate a 5 -
# 10 sec calc

# IDK actual, look it up

# ["Metadata"]["logicalEvents"] could be interesting
AVERAGE_RUNS_PER_SEASON = 7 # I think this is  useful
# Probably want to make the above based on team, but maybe not? Idk actually
# think it could be avg per season and be a counting stat low key
PREVIOUS_EVENT = None


# TO DO : Definitely still some issues. Team totals used everywhere..... just a
# measure of how many more abs you make for your team since team totals is the
# same for everyone. Need to make outs "decrease" team totals
# RIght now it's actually easuring atbats....fuuuuuuuuck gonna be a pain to # debug

def wins_happening_with_this_play(event, outs, total):
    global PREVIOUS_EVENT
    global EVENT_CACHE
    if not event:
        raise Exception("HERE")

    if event["playEndTime"] in EVENT_CACHE:
        return EVENT_CACHE[event["playEndTime"]]

    # Could do by saying
    if event["about"]["inning"] >= 9 and event["outNumber"] == 3:
    # TODO add when scores are the same.
        return event["team_total"]

    # Idk put win probability here TODO
    if event is PREVIOUS_EVENT:
        return event["team_total"] + .5

    PREVIOUS_EVENT = event
    # Maybe small time reduction here

    out_runners = [x["movement"]["outNumber"] for x in event["runners"] if x["movement"]["outNumber"]]
    if out_runners:
        max_outs = max(out_runners)
    else:
        max_outs = 0

    outs = max(outs, max_outs)
    # TODO - Make sure we don't need for loop here
    #for EVENT in EVENT_CACHE:

    if not event.get("playEndTime"):
        raise Exception("HERE2")

    if event["playEndTime"] not in EVENT_CACHE:
        if event.get("next_one_please") is None:
            return event["team_total"]


        try:
            EVENT_CACHE[event["playEndTime"]] = wins_happening_with_this_play(event["next_one_please"], outs, total)
        except Exception as e:
            #print(event)
            raise Exception

        else:
            return(total)
    # sum of both_teams
    # or only winning_team? I think both teams but not sure. If too slow, come
    # here
    # TODO

def wins_happening_without_this_play(event, outs):
    # Could go further here to make better low key, but leaving simple for now
    if outs == 2:
        return event["team_total"]

    next_one_please = event.get("next_one_please", None)
    if not next_one_please:
        return event["team_total"] + .5

    outs += 1

    if next_one_please == None:
        return event["team_total"]*.5

    print(event["team_total"])
    return wins_happening_without_this_play(next_one_please, outs)


    # NOT SURE ABOUT THIS ONE 
    #TODO
    #if event["id"] in EVENT_CACHE:
    #    return EVENT_CACHE["id"]

    #if event["ended"] == True:
    #    return event["team_total"]

    #for EVENT in EVENT_CACHE:
    #    if EVENT not in EVENT_CACHE:
    #        wins_happening_with_this_play(EVENT)
    #pass

# total is int, all_events json_dict, all_players default_dict, default 0
def war_calc(total_game_score, all_events, all_players):
    global AVERAGE_RUNS_PER_SEASON
    cache_i_guess = {}
    player_war = {x["fullName"]:0 for x in all_players}
    # Event tmust be sorted
    allEvents = all_events #calc['event']
    current_event_closeness = 1
    # Could be more complicated than scalar if you're sweaty
    scaling_factor = .5

    for count, event in enumerate(all_events):
        event["team_total"] = total_game_score
        if count < len(all_events) - 1:
            event["next_one_please"] = all_events[count + 1]

        else:
            event["next_one_please"] = None

    for event in all_events:
        outs = 0
        this_factor = scaling_factor * current_event_closeness
        # Batting only for now
        player = event["matchup"]["batter"]["fullName"]

        # This is wrong I think TODO
        out_runners = [x["movement"]["outNumber"] for x in event["runners"] if x["movement"]["outNumber"]]
        if out_runners:
            max_outs = max(out_runners)
        else:
            max_outs = 0

        outs = max(outs, max_outs)

        if max_outs is None:
            max_outs = 0
        outs = max(max_outs, 0)

        #print(wins_happening_with_this_play(event, outs, total_game_score))
        #print(wins_happening_without_this_play(event, outs))

        player_war[player] += (1.0/AVERAGE_RUNS_PER_SEASON)*(
                                (
                                player_war[player] +
                                scaling_factor*
                                    (wins_happening_with_this_play(event, outs, total_game_score) * wins_happening_without_this_play(event, outs))
                                )
                            )

    return player_war

    # idea: We calculate what would of happened with an out.
    #       Then we calculate what happened based on the play


    # You then "normalize" by subracting. You get amount of WAR. You calculate how many
    # wins happened in future because of your play. Then you calculate how many
    # wins happened in future in the else - if nothing happened on your play.
    # WAR

    # You could also do some things that are "RAR" runs against replacement


    # RAR is probably more predictive. Actually almost certainly


    # I think we could "weight" against a combo of RAR, WAR  and other things
    # for "most predictive". Idk that's too much work

    # I saw we have toal score in game to be a weight


