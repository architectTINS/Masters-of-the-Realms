%lang starknet

namespace Game {
  const NUMBER_OF_MARKETS = 3;
  const NUMBER_OF_PLAYERS = 9;
  const INITIAL_PEARL_BALANCE = 50000;

  // The Target price
  const INITIAL_ENERGY_UNIT_PRICE = 50;

  // This much units are expected to be sold in an hour.
  const UNITS_SCHEDULE = 60;

  const NUMBER_OF_ROUNDS = 10; // This cannot be changed for this program.

  const DECAY_PERCENTAGE = 20;

  const ENERGY_UNIT_BLOCKS = 20; // Each player buys energy units in blocks of this quantity.
}
