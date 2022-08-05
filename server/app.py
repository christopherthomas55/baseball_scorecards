from flask import Flask, render_template, Markup, redirect, url_for, request
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
    d = datetime.datetime.strptime(datestr, "%Y-%m-%d")
    next_day = (d + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    prev_day = (d - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    return render_template('date_page.html', games=games, datestr=datestr,
            next_day=next_day, prev_day=prev_day)

@app.route('/dateform')
def dateform():
    default = datetime.datetime.today().strftime("%Y-%m-%d")
    datestr = request.args.get('date')
    return redirect(url_for('date_page', datestr=datestr))

# TODO - Add last update
@app.route('/game/<gameid>')
def game_page(gameid):
    #try:
        isSuccess = get_game(gameid, refresh = False)
        if isSuccess:
            home_file = isSuccess.get("home")
            away_file = isSuccess.get("away")
            age = isSuccess.get("age")
            with open(home_file, "r") as f:
                home_svg = f.read()
            with open(away_file, "r") as f:
                away_svg = f.read()

            return render_template('scorebook_page.html', home_svg=Markup(home_svg),
                    away_svg=Markup(away_svg), gameid=gameid, age=age)
        else:
            raise("Not successful scorebook")
    #except:
        #return render_template('error_scorebook.html', gameid=gameid)

# TODO - add button
@app.route('/game/<gameid>/refresh')
def refresh_game(gameid):
    get_game(gameid, refresh = True)
    return redirect(url_for('game_page', gameid=gameid))

