# ymir
[TODO: Logo?]
An AI-generated procedural pseudo-physics-based platformer
[TODO: Image]

## How to Add an Enemy:

In `sprite/tile.py`: 

Choose a new letter to use for your enemy in the level files

1. Add to `TEXTURES`: key is the new letter, value is the base texture (e.g. if the textures are called `slime_1`, `slime_2`, etc. put `slime`).
2. Add it to `TILE_TYPE` with the next value (todo: automate this part)

In `sprite/enemy.py`:

1. Make your class `<your_class>.py`, extending `Enemy`
2. Put `<new_letter>: <your_class>` in enemies (at the bottom)

## TODO

1. Weapons
    Create a `tool` (`weapon?`) property of `Sprite`
    Provide automatic weapon-use behavior for enemies (`Enemy.py`?)
    Create user-controlled behavior for the player (`player.py`)
2. Teleporters
3. AI Level Generation (!!!)
4. Pickups (tools, weapons)
5. Skill points
6. Character customization (tied to skill points)