from .CheckpointTile       import CheckpointTile
from .DeadlyTile           import DeadlyTile
from .EnemyTile            import EnemyTile, enemies
from .HorizontalMovingTile import HorizontalMovingTile
from .KeyTile              import KeyTile
from .SlicerTile           import SlicerTile
from .SpikesTile           import SpikesTile
from .SpringTile           import SpringTile
from .TeleporterTile       import TeleporterTile
from .LaserTile            import LaserTile

tile_classes = {'M': HorizontalMovingTile, 'c': CheckpointTile, 'P': SpikesTile,
                'K': KeyTile, ';': KeyTile,
                'Q': SlicerTile,
                'r': SpringTile,
                '1': TeleporterTile, '2': TeleporterTile,
                'T': LaserTile('blue')}

for k in enemies:
    tile_classes[k] = EnemyTile