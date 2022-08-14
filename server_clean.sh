# Removes all but last 20
find /home/chris/baseball_scorecards/data/game/ -maxdepth 1 -type f | head -n -20 | xargs --no-run-if-empty rm
find /home/chris/baseball_scorecards/data/day/ -maxdepth 1 -type f | head -n -20 | xargs --no-run-if-empty rm
