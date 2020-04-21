from astrobox.core import Drone


class TsigelnikovDrone(Drone):
    stat_empty = 0
    stat_not_fully_loaded = 0
    stat_full = 0

    def is_free_asteroid(self, asteroid):
        res = 1
        for teammate in self.teammates:
            if teammate.target == asteroid:
                if asteroid.payload < 100:
                    return False
                res -= 1
        return res > 0

    def _get_coord_closest_asteroid(self):
        self.target = self.my_mothership
        distance_to_closest_asteroid = float('inf')
        for asteroid in self.asteroids:
            if asteroid.payload > 0 and self.is_free_asteroid(asteroid):
                distance = self.distance_to(asteroid.coord)
                if distance_to_closest_asteroid > distance:
                    self.target = asteroid
                    distance_to_closest_asteroid = distance
        return self.target

    def _get_coord_farthest_asteroid(self, n=620):
        self.target = self.my_mothership
        distance_to_farthest_asteroid = 0
        for asteroid in self.asteroids:
            if asteroid.payload == 0 or self.is_free_asteroid(asteroid) is False:
                continue
            distance = self.distance_to(asteroid.coord)
            if distance_to_farthest_asteroid < distance < n:
                self.target = asteroid
                distance_to_farthest_asteroid = distance
        return self.target

    def on_born(self):
        self.target = self._get_coord_closest_asteroid()
        TsigelnikovDrone.stat_empty += self.distance_to(self.target)
        self.move_at(self.target)

    def on_stop_at_asteroid(self, asteroid):
        self.load_from(asteroid)
        if asteroid.payload + self.payload >= 100:
            self.turn_to(self.my_mothership)

    def on_stop_at_mothership(self, mothership):
        self.unload_to(mothership)
        self.turn_to(self.target)

    def on_load_complete(self):
        if self.is_full:
            TsigelnikovDrone.stat_full += self.distance_to(self.my_mothership)
            self.move_at(self.my_mothership)
        else:
            self.target = self._get_coord_closest_asteroid()
            self.move_at(self.target)
            TsigelnikovDrone.stat_not_fully_loaded += self.distance_to(self.target)

    def on_unload_complete(self):
        self.target = self._get_coord_closest_asteroid()
        self.move_at(self.target)
        TsigelnikovDrone.stat_empty += self.distance_to(self.target)
        if self.check_fullness_asteroid() and self.check_team():
            self.get_stat()

    @staticmethod
    def get_stat():
        print(
            f"\n{'emplty drone:':<30}{round(TsigelnikovDrone.stat_empty)}"
            f"\n{'full drone:':<30}{round(TsigelnikovDrone.stat_full)}"
            f"\n{'not fully loaded drone:':<30}{round(TsigelnikovDrone.stat_not_fully_loaded)}")

    def check_team(self):
        for teammate in self.teammates:
            if not teammate.is_empty:
                return False
        return True

    def check_fullness_asteroid(self):
        for asteroid in self.asteroids:
            if asteroid.payload > 0:
                return False
        return True
