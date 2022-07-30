from flask import Flask, render_template, Markup
import datetime
from lib.api_interfaces import get_date_game_ids, get_game, init_dir
app = Flask(__name__)


@app.before_first_request
def _init():
    init_dir()

@app.route("/")
def main():
    return date_page(datetime.datetime.today().strftime("%Y-%m-%d"))

@app.route('/date/<datestr>')
def date_page(datestr):
    games = get_date_game_ids(datestr)
    return render_template('date_page.html', games=games, datestr=datestr)

# TODO - Add last update
@app.route('/game/<gameid>')
def game_page(gameid):
    isSuccess = get_game(gameid, refresh = True)
    if isSuccess:
        home_file = isSuccess.get("home")
        away_file = isSuccess.get("away")
        with open(home_file, "r") as f:
            home_svg = f.read()
        with open(away_file, "r") as f:
            away_svg = f.read()

        return render_template('scorebook_page.html', home_svg=Markup(home_svg),
                away_svg=Markup(away_svg), gameid=gameid)
    else:
        return render_template('error_scorebook.html', gameid=gameid)

# TODO - add button
@app.route('/game/<gameid>/refresh')
def refresh_game(gameid):
    get_game(gameid, refresh = True)
    return game_page(gameid)

