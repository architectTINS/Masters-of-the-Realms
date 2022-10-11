# Steps to setup development environment
1. clone the repo.
2. cd Master-of-the-Realms/DynamicMarkets-VRGDA-Model
3. python3.9 -m venv .
4. ./toold/update_paths.sh
5. source bin/activate
6. pip install --upgrade pip
7. pip install cairo-nile poetry
8. nile init
9. nile compile

# How to play the game
1. Run nile node in a terminal
2. In another terminal, run ./scripts/initialise.py. This will deploy an account contract, and the game contract in the local devnet.
3. Run ./scripts/play_few_days.py to play the game for 3 days of data.
4. Run ./scripts/play_full_game.py to play/run the full game.
5. Run ./scripts/get_game_data.py to collect and produce data for further analysis as in the below screenshot.

![20221011 01 221538](https://user-images.githubusercontent.com/114365800/195200000-c6265b45-a23b-4da7-86d7-7a533ffaac50.png)
