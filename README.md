# The Legend of Zelda, a Pygame Training Exercise

## How to build & run project
### Exe file for Windows10 users
**FALSE POSITIVE THREAT WARNING** : 

The game.exe file is made with PyInstaller, which is apparently used a lot by malware creators, making its bootloader associated with malwares. Your antivirus will most likely identify it as a false positive threat to your system.

If you don't trust it, please feel free to inspect the source files, and run the project with the next instructions

For those who chose to trust the file : there is a game.exe file included in the main directory of the project.

If you download the whole repository, you can execute this file to play the game, even if you don't have Python installed on your machine.

### CLI File for Mac OS X users
In your terminal, change directory to the directory you find this README.md file in, and run the file : 

```./mac_os-game```

This should allow you to run this project without installing Python3 nor Pygame !

This file has been generated on a M1 machine, with OS version 14.3.1, and I have no idea if it will work on any other architecture or OS version.

Double-clicking on the file itself in the Finder will not work, as my code uses relative pathing to files, and double-clicking on the file will do the same as running it from your terminal, albeit it will do so from your HOME folder, and relative pathing to resource files will thus not work.

### Prerequisites to run it yourself
Python 3 : https://www.python.org (v3.11.5 used for the development of this project)

Pygame :  https://www.pygame.org/

Installation command : 
```python -m pip install -U pygame --user```

### Run
Command line from the `<project folder>/code/` :
```python ./main.py```

## Controls
_All controls are configurable in inputs.py_

Move with ```directional arrows``` or ```Z Q S D```

Use item A to attack with ```SPACE```

Use item B with ```LEFT SHIFT```

Open the pause/item menu with ```ESCAPE```

Reduce player health to 0 with ```BACKSPACE```

In the pause/item menu, select item B by moving the blinking selector with ```arrow left / arrow right``` or ```Q D```

Game can be closed by pressing ```ESC``` on the GAME OVER screen, or  ```ANY KEY``` on the VICTORY screen

Game can be continued by pressing ```RETURN``` on the GAME OVER screen

Game state can be saved by pressing ```F5``` when appropriate

Game state can be loaded from saved state by pressing ```F6``` when appropriate. This will reset the Player's position to where the game starts

## Gameplay hints

Please read the Survival Guide pdf, it contains lots of useful information and hints about the secrets of this world !

## Context of the project
### WHAT
Very loose recreation of The Legend of Zelda as seen on the NES, published in 1986 by Nintendo.

With tons of creative liberty.

### HOW
Developed in Python3 using the Pygame engine : https://www.pygame.org/

IDE : https://www.jetbrains.com/fr-fr/pycharm/

Graphics editing : https://www.getpaint.net/

Tile/map system management : https://www.mapeditor.org/

Graphic assets : https://www.spriters-resource.com

Sound assets : https://www.sounds-resource.com/

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

## AFTERTHOUGHT
There are still many improvements possible. That I will most likely not implement, as it doesn't really fit with my goals / the scope I decided on.
- I could do more refactoring to make further development less messy, mainly for Particles and Enemies. 
For instance : create a DivingEnemy subclass to Enemy, and have Leever & Zora inherit from it. That would allow to stop duplicating code, and make the addition of further diving monsters easier.
- I could simplify code a lot by removing all the flipping systems for the entity / particle sprites. I did it for the small useless challenge, and because I chose to think about how it would have been done when complex code was more advantageous than having all sprites in all directions and all colors, since space on a NES cartridge was VERY limited, and images are heavy.
Today, I could just create these sprites in the .png tile set images, and give less headaches to people implementing systems here.
- I could have used the palette swap system used for victory/game over animations, to also shift the colors of Entities when hurt, or the HUD in specific circumstances like in the NES game, or to represent different player equipment (such as the rings in the NES game)
- I could separate settings.py in two files, one that does all the heavy lifting of providing all the code needs, and one that only contains elements that players could easily modify to change the game's difficulty / game feel.
- Rely more on dicts in settings.py, that could clean the look a little and make file organisation slightly less confusing. But I should not do it to the point of making the code absolutely littered with ```DICT_NAME[DICT_ENTRY][LABEL_VARIATION]...```
- I could separate the big items, and lootable items from the particles, as they differ from a design point of view, but it works really well that way so far, that's a lot of work time to do for a project no one will ever use / expand upon.  

I thought about implementing some other features, and decided against. A few of them :
- Flying Enemy : no different from other Enemies, collides only with Border tiles, same kind of behaviour as Leever and Zora diving to do flying/landing,
- Map in HUD: didn't seem particularly exciting to solve (create a dict that registers which level exists/should be shown and which don't, blit them on the HUD map, blit a position sprite on the cell that corresponds to the level.current_map_screen),
- More content in general (bigger map, more dungeons, triforce fragments system, ...), but it's not where I want to go. Loads of work, for very little learning along the way. Maybe a few new mechanics to keep things interesting during gameplay, but nothing that really makes generating content worth it for a project that has no ambition of turning into a real game.

All in all, a very interesting project.

Made me really comfortable around Python, allowed me to discover many practices (good and bad), working with Pygame felt great.

Had me rethink about some design patterns, and ignore most of them.

I had to make choices about many things I didn't think about before getting confronted with it, for instance I kind of wanted to have one file per class, but felt like files acting like modules and regrouping a class with its children made sense, and kept it that way. Concepts of what belongs to a class, or another, how to keep them separated, trying to avoid them getting interdependent, ...

Developing solo was a really different experience from working in teams as I used to when I was a QA or in project management.

Huge thanks to the friends that helped me get a foot back in software development, early git practices, etc.

And thanks to the people who will stumble upon this and read it !


This project could definitely be coded in a cleaner manner, and the more projects I'll work on, the better my code will get.

This one is a first stone, and will stay the way it is, so I can come back to it and see my progress. I hope that I will see progress.
