import unittest

from src.christofides import christofides
from src.core import load_cities
from src.genetic import GAConfig, genetic_tsp


class TravellingMerchantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = load_cities("data/villes_france_lat_long.csv")

    def _assert_valid_cycle(self, route):
        self.assertEqual(route[0], route[-1])
        self.assertEqual(len(route), len(self.cities) + 1)
        self.assertEqual(set(route[:-1]), set(range(len(self.cities))))
        self.assertEqual(len(set(route[:-1])), len(self.cities))

    def test_christofides_returns_valid_cycle(self):
        result = christofides(self.cities)
        self._assert_valid_cycle(result.route)
        self.assertGreater(result.distance_km, 0)

    def test_genetic_returns_valid_cycle(self):
        cfg = GAConfig(population_size=60, generations=80, elite_size=4, seed=7)
        result = genetic_tsp(self.cities, cfg)
        self._assert_valid_cycle(result.route)
        self.assertGreater(result.distance_km, 0)


if __name__ == "__main__":
    unittest.main()
