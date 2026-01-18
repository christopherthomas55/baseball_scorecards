Generates scorebooks as svg files
For now blank, filling in will take a bit.

Maybe can make not blank for end of 2022 season!

# Potential features
- Autofill in names/teams/weather
- In general more customizability in where things go
- Live scoring (a man can dream)

# The dream vision 
- Live scorecards of any game, in any style of scorecard

# Some more fun things if this works
- Generate historical games/season quilts
- Random game generator sent through another simulator?
- Generator game outcomes of super mega baseball LOL
- Animated svg like - https://news.ycombinator.com/item?id=44498133



########################################################
#                    Deployment Notes                  #
########################################################

Running on a digital ocean instance. 

Service name is baseball_scorecards, which runs the uwsgi stuff
I am also running nginx to serve this, esp sicne that service also holds my empty blog

I semi followed this guide, mostly changing config settings and names. Also no venv
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04
