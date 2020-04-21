# -*- coding: utf-8 -*-

# pip install -r requirements.txt

from astrobox.space_field import SpaceField
from stage_03_harvesters.reaper import ReaperDrone
from stage_03_harvesters.driller import DrillerDrone
from vader import VaderDrone
from tsigelnikov import TsigelnikovDrone

NUMBER_OF_DRONES = 5

if __name__ == '__main__':
    scene = SpaceField(
        speed=3,
        asteroids_count=20,
    )
    team_1 = [TsigelnikovDrone() for _ in range(NUMBER_OF_DRONES)]
    team_2 = [ReaperDrone() for _ in range(NUMBER_OF_DRONES)]
    team_3 = [DrillerDrone() for _ in range(NUMBER_OF_DRONES)]
    team_4 = [VaderDrone() for _ in range(NUMBER_OF_DRONES)]
    scene.go()

# Третий этап: зачёт!
