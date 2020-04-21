# -*- coding: utf-8 -*-

from astrobox.space_field import SpaceField
from tsigelnikov import TsigelnikovDrone


if __name__ == '__main__':
    scene = SpaceField(
        speed=5,
        asteroids_count=15,
    )
    drones = [TsigelnikovDrone() for _ in range(5)]
    scene.go()
