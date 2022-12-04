# Dynamic markets based on VRGDA (Variable Rate Gradual Dutch Auction) model
## Steps to setup development environment
1. Clone sarayu repo https://github.com/architectTINS/sarayu/releases/tag/v0.1 into ~/cairo/tools/sarayu
2. clone the repo.
3. cd Master-of-the-Realms/DynamicMarkets-VRGDA-Model
4. python3.9 -m venv .
5. ./tools/update_paths.sh
6. ~/cairo/tools/sarayu/sarayuinit.sh
7. source bin/activate
6. pip install --upgrade pip
7. pip install cairo-nile==0.9.1 cairo-lang==0.10.0 starknet-devnet==0.3.3 click
8. sarayu compile

## How to play the game
1. Run nile node in a terminal
2. In another terminal, run ./scripts/initialise.py. This will deploy an account contract, and the game contract in the local devnet.
3. Run ./scripts/play_few_days.py to play the game for 3 days of data.
4. Run ./scripts/play_full_game.py to play/run the full game.
5. Run ./scripts/get_game_data.py to collect and produce data for further analysis as in the below screenshot.

![20221011 01 221538](https://user-images.githubusercontent.com/114365800/195200000-c6265b45-a23b-4da7-86d7-7a533ffaac50.png)
