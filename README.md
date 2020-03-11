# ymir

## How to add an Enemy:

In `sprite/tile.py`: 

1. Add to `TEXTURES`: key is the letter, value is the base texture (e.g. if the textures are called `slime_1` put `slime`).
2. Add it to `TILE_TYPE` with the next value (todo: automate this part)

In `sprite/enemy.py`:

1. Make your class
2. Put `letter: your_class` in enemies (at the bottom)

## TODO
1. Weapons
    Create a `tool` (`weapon?`) property of `Sprite`
    Provide automatic weapon-use behavior for enemies
2. Teleporters
3. AI Level Generation (!!!)
4. Pickups (tools, weapons)
5. Skill points
6. Character customization (tied to skill points)