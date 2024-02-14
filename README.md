# The Legend of Zelda, a Pygame Training Exercise

## Controls
_All controls are configurable in inputs.py_

Move with ```directional arrows``` or ```Z Q S D```

Use item A to attack with ```SPACE```

Use item B with ```LEFT SHIFT```

Open the pause/item menu with ```ESCAPE```

In the pause/item menu, select item B by moving the blinking selector with ```arrow up / arrow down``` or ```Q D```
(Not all visible items are implemented, they will have no sprite nor effect when used)

Game can be closed by pressing ```SPACE``` on the GAME OVER screen

## How to build & run project
### Prerequisites
Python 3 : https://www.python.org

Pygame :  https://www.pygame.org/
Installation command : 
```python -m pip install -U pygame --user```

### Run
Command line from the <project folder>/code/ :
```python ./main.py```

## Context of the project
### WHAT
Recreation of The Legend of Zelda as seen on the NES, published in 1986 by Nintendo.

### HOW
Developed in Python3 using the Pygame engine.

### WHY
The goals are : 
- To get back into developing in Python
- To discover a simple game engine
- To (re)learn how to git

### SCOPE
The target result is not to redevelop the whole game, but to implement the main mechanics in a playable state :
- A playable animated character, that can move, loot items, use items, attack, get hit, and die
- A selection of animated monsters to fight against, with movement patterns inspired from the NES version (relatively basic, no real pathfinding that needs to avoid obstacles)
- A few screens of the main map, with a way to navigate between them, and the scroll animation during transition
- At least one underground map (a single screen cave, maybe one dungeon)
- A selection of items to use (basic like the hearts to regen health, or evolved like the ladder to cross bodies of water, or the flame to torch specific bushes)

### LIMITS
Graphics and sounds will be basic rips of the Nintendo owned assets, found online on sprite and sound websites.
Current sprites ripped by Mister Mike. 

Not recommended, but I'm not motivated to learn how to do pixel art and to create my own assets for now.
Not the focus of this project. Same for sound design. 

Might happen in a later project, or will use a free art pack made for this purpose.

## WIP BOARD
https://jamboard.google.com/d/17sGVfK9TGUQF2FjtBszIERMs1WPzu5huUBg2sg46HeE/edit?usp=sharing