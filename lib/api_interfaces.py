import requests
import datetime
import time
from pathlib import Path
import json
from Scorebook import Scorebook

# Expect this to change
API_URL='https://bdfed.stitch.mlbinfra.com/bdfed/transform-mlb-scoreboard?stitch_env=prod&sortTemplate=4&sportId=1&startDate={date}&endDate={date}'
GAME_URL="https://statsapi.mlb.com/api/v1.1/game/{gameid}/feed/live?language=en"
DATA_DIR = Path('data/')
GAME_DIR = DATA_DIR/'game'
DAY_DIR = DATA_DIR/'day'
ALL_PATHS = [DATA_DIR, GAME_DIR, DAY_DIR]
RATE_LIMIT = 5 #SECONDS

def init_dir():
    for p in ALL_PATHS:
        if not p.exists():
            print
            p.mkdir()


def cached_download_json(cache_path, url, force_download = False):
# TODO - Weird logical structure
    if not cache_path.exists() or force_download:
        if cache_path.exists() and (time.time() - cache_path.stat().st_mtime) < RATE_LIMIT:
            print(f"Rate limited for {cache_path}. Using cache")
            with cache_path.open() as f:
                djson = json.load(f)
        else:
            print(f"No cache hit for {cache_path}. Downloading")
            try:
                resp = requests.get(url)
            except Exception as e:
                print(f"Failed downloading ids for date {cache_path}")
                print(f"Exception - {str(e)}")
                raise

            djson = resp.json()
            with cache_path.open('w') as f:
                json.dump(djson, f)
    else:
        print(f"Using cache hit for {cache_path}")
        with cache_path.open() as f:
            djson = json.load(f)
    return djson


def get_date_game_ids(datestr):
    assert(isinstance(datestr, str))
    cache_f = (DAY_DIR/datestr).with_suffix('.json')
    url = API_URL.format(date=datestr)
    djson = cached_download_json(cache_f, url)

    try:
        games = djson.get('dates')[0].get('games')
        return [
                (x.get('gamePk'),
                    {"home":x.get('teams').get('home').get('team').get('name'),
                     "away":x.get('teams').get('away').get('team').get('name')
                     }
                )
                for x in games
               ]

    except Exception as e:
        print(f"Exception in parsing ids for date {datestr}")
        print(f"Exception - {str(e)}")
        raise


def get_today_game_ids():
    return get_date_game_ids(datetime.datetime.today().strftime("%Y-%m-%d"))


def get_game(gameid, refresh = False):
    cache_f = (GAME_DIR/gameid).with_suffix('.json')
    url = GAME_URL.format(gameid=gameid)

    _ = cached_download_json(cache_f, url, force_download=refresh)

    home_file = cache_f.with_name(f"{gameid}_home.svg")
    away_file = cache_f.with_name(f"{gameid}_away.svg")

    #try:
    home = Scorebook("home", str(cache_f))
    home.save(str(home_file))
    away = Scorebook("away", str(cache_f))
    away.save(str(away_file))
    #except:
        #return False
    age = time.time() - cache_f.stat().st_mtime
    return {"home": home_file, "away": away_file, "age": age}
