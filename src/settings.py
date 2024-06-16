<<<<<<< HEAD
<<<<<<< HEAD
import os
=======
=======
import os

SCALE = 1

>>>>>>> c63ba09 (fix: state transitions)
TILE_SIZE = 32
SCREEN_WIDTH = 16 * TILE_SIZE
SCREEN_HEIGHT = 9 * TILE_SIZE
>>>>>>> c6c84f8 (wip: fixed ui unscaling for mouse events)

<<<<<<< HEAD
SCALE = 1

TILE_SIZE = 32
HALF_TILE = TILE_SIZE / 2

SCREEN_WIDTH = 16 * TILE_SIZE
SCREEN_HEIGHT = 9 * TILE_SIZE
=======
>>>>>>> c63ba09 (fix: state transitions)

ANTI_ALIASING = os.getenv("ANTI_ALIASING", "false").lower() == "true"
