%lang starknet

namespace Game {
  const NUMBER_OF_FOOD_OPTIONS = 3;
  const NUMBER_OF_PLAYERS = 9;
  const INITIAL_PEARL_BALANCE = 1000;

  // The Target price - for each of the food option.
  const INITIAL_FOOD_PRICE = 50;

  // This much units are expected to be sold in an hour.
  const UNITS_SCHEDULE = 3;

  // This cannot be changed for this program.
  // Number of time a traveller/player makes food choices.
  const NUMBER_OF_ROUNDS = 10; 

  const DECAY_PERCENTAGE = 20;
}
