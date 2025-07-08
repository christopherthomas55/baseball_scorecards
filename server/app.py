from flask import Flask, render_template, Markup, redirect, url_for, request
import datetime
import pytz
from lib.api_interfaces import get_date_game_ids, get_game, init_dir, game_to_svg
app = Flask(__name__)


@app.before_first_request
def _init():
    init_dir()

@app.route("/")
def main():
    return date_page(datetime.datetime.now(pytz.timezone('US/Central')).strftime("%Y-%m-%d"))

@app.route('/date/<datestr>')
def date_page(datestr):
    games = get_date_game_ids(datestr)
    d = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    next_day = (d + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    prev_day = (d - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    games_data = [get_game(gameid, refresh = False) for gameid in games]
    for g in games_data:
        g['home_svg'] = Markup(g['home_svg'])
        g['away_svg'] = Markup(g['away_svg'])

    # TODO 1 - Create a Game data object and send that over. get_game() should
    # use it. Should interact with scorebook object.

    # TODO 2 - Create a div/template for these. Maybe look into tailwind css

    return render_template('date_page.html', games=games, datestr=datestr,
                           gamedatas=games_data, next_day=next_day, prev_day=prev_day)

@app.route('/dateform')
def dateform():
    default = datetime.datetime.today().strftime("%Y-%m-%d")
    datestr = request.args.get('date')
    return redirect(url_for('date_page', datestr=datestr))


def game_to_svg(game):
    # If not successful
    if not game:
        print(str(e))
        return None
        # return render_template('error_scorebook.html', gameid=gameid)

    home_file = game.get("home")
    away_file = game.get("away")
    age = game.get("age")
    with open(home_file, "r") as f:
        home_svg = f.read()
    with open(away_file, "r") as f:
        away_svg = f.read()
    return home_svg, away_svg


# TODO - Need to handle "no lineup" exceptions better. Probably in scorecard.py
# not here
@app.route('/game/<gameid>')
def game_page(gameid):
    try:
        game = get_game(gameid, refresh = False)
        if game:
            home_svg, away_svg = game_to_svg(game)
            return render_template('scorebook_page.html',
                                   home_svg=Markup(game["home_svg"]),
                                   away_svg=Markup(game["away_svg"]),
                                   gameid=gameid, age=age)
        else:
            raise("Not successful scorebook")
    except Exception as e:
        print(str(e))
        return render_template('error_scorebook.html', gameid=gameid)

# TODO - add button
@app.route('/game/<gameid>/refresh')
def refresh_game(gameid):
    get_game(gameid, refresh = True)
    return redirect(url_for('game_page', gameid=gameid))

