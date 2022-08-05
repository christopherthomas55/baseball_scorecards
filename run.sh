echo "-----------------------------\nMust manually find game number from MLB site!\n-----------------------------"
GAME_NUMBER=633414
curl "https://statsapi.mlb.com/api/v1.1/game/$GAME_NUMBER/feed/live?language=en" > data/live_data.json
python3 lib/Scorebook.py
