#curl 'https://statsapi.mlb.com/api/v1.1/game/662751/feed/live?language=en' > example_data.json

echo "-----------------------------\nMust manually find game number from MLB site!\n-----------------------------"
GAME_NUMBER=661271
curl "https://statsapi.mlb.com/api/v1.1/game/$GAME_NUMBER/feed/live?language=en" > live_data.json

