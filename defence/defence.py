from shapely.geometry import Polygon
from operator import itemgetter
from matplotlib.path import Path
import numpy as np
from copy import deepcopy

class DefenceSolver:

    def __init__(self):
        # G = grassland, F = forest, M = mountain, W = water, X = wall, B = blank
        self.MAP = [
                    ["F", "X", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W"],
                    ["X", "F", "X", "X", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "F", "F", "F"],
                    ["X", "F", "F", "X", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "F", "F", "F", "F"],
                    ["F", "X", "X", "F", "F", "F", "F", "F", "G", "G", "G", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "F", "F", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G", "F", "F", "F", "G", "G", "G", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "F", "F", "W", "W", "W", "W", "W", "F", "W", "W", "W", "F", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "W"],
                    ["F", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "W", "W"],
                    ["F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "W", "F"],
                    ["F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "W", "W", "F"],
                    ["F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "G", "G", "G", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "G", "G", "G", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "W", "F", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "G", "M", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "G", "G", "G", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "G", "G", "G", "G", "G", "G"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "W", "G", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "G", "G", "G", "G", "F"],
                    ["G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "G", "G", "G", "G", "F"],
                    ["F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "G", "G", "G", "F", "F"],
                    ["F", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "V", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G", "F", "F", "F", "W", "W", "W", "W", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "G", "F", "F", "F", "F", "F", "W", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "G", "G", "G", "G", "G", "F", "F", "F", "F", "F", "W", "W", "F", "F", "F", "G", "G", "G", "G", "G", "G", "G", "G", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "G", "G", "G", "F", "F", "F", "F", "F", "W", "W", "F", "F", "F", "F", "F", "F", "G", "G", "G", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "F", "F", "W", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W", "M", "M", "M", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "F", "F", "F", "W", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "W", "W", "W", "W", "W", "W", "F", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "W", "F", "F", "F", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "F", "F", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "W", "W", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "G", "G", "G", "G", "G", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "W", "F", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "W", "W", "W", "F", "F", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "F", "F", "W", "F", "F", "F", "W", "W", "F", "F", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "F", "F", "F", "W", "F", "F", "F", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "F", "W", "W", "W", "F", "F", "W", "F", "F", "F", "F", "F", "W", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "W", "W", "W", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "W", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "F", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
                    ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"]
                    ]
        self.Y_LIMIT = len(self.MAP)
        self.X_LIMIT = len(self.MAP[0])
        self.BUDGET = 1000
        self.GRASSLAND_COST = 1
        self.FOREST_COST = 10
        self.MOUNTAIN_COST = 100
        self.best_wall_path = []
        self.best_wall_score = 0

    def calculate_cost(self, num_grassland, num_forest, num_mountain):
        return num_grassland * self.GRASSLAND_COST + num_forest * self.FOREST_COST + num_mountain * self.MOUNTAIN_COST

    def is_within_budget(self, num_grassland, num_forest, num_mountain):
        if self.calculate_cost(num_grassland, num_forest, num_mountain) <= self.BUDGET:
            return True
        else:
            return False

    def have_two_neighbours_in_one_direction(self, grid, coordinate, y_limit, x_limit):

        if coordinate[0] - 1 < 0:
            top_border = ["B", "B", "B"]
        else:
            top_border = ["B" if coordinate[1] - 1 < 0 else grid[coordinate[0] - 1][coordinate[1] - 1],
                          grid[coordinate[0] - 1][coordinate[1]],
                          "B" if coordinate[1] + 1 >= x_limit else grid[coordinate[0] - 1][coordinate[1] + 1]]

        if coordinate[0] + 1 >= y_limit:
            bottom_border = ["B", "B", "B"]
        else:
            bottom_border = ["B" if coordinate[1] - 1 < 0 else grid[coordinate[0] + 1][coordinate[1] - 1],
                             grid[coordinate[0] + 1][coordinate[1]],
                             "B" if coordinate[1] + 1 >= x_limit else grid[coordinate[0] + 1][coordinate[1] + 1]]

        if coordinate[1] -1 < 0:
            left_border = ["B", "B", "B"]
        else:
            left_border = ["B" if coordinate[0] - 1 < 0 else grid[coordinate[0] - 1][coordinate[1] - 1],
                          grid[coordinate[0]][coordinate[1] - 1],
                          "B" if coordinate[0] + 1 >= y_limit else grid[coordinate[0] + 1][coordinate[1] - 1]]

        if coordinate[1] + 1 >= x_limit:
            right_border = ["B", "B", "B"]
        else:
            right_border = ["B" if coordinate[0] - 1 < 0 else grid[coordinate[0] - 1][coordinate[1] + 1],
                             grid[coordinate[0]][coordinate[1] + 1],
                             "B" if coordinate[0] + 1 >= y_limit else grid[coordinate[0] + 1][coordinate[1] + 1]]

        if ("X" in top_border and "X" in bottom_border) or ("X" in left_border and "X" in right_border):
            return True
        else:
            return False

    def does_wall_join(self, grid):
        y_limit = len(grid)
        x_limit = len(grid[0])
        for y in range(0, y_limit):
            for x in range(0, x_limit):
                if grid[y][x] == "X":
                    if not self.have_two_neighbours_in_one_direction(grid, (y, x), y_limit, x_limit):
                        return False
        return True

    def is_village_inside_wall(self, grid):
        return True

    # A solution is valid if the wall joins together (assuming water is treated as a wall),
    # the village is inside the wall and the wall construction is within budget
    def is_valid_solution(self, grid, num_grassland, num_forest, num_mountain):
        if self.does_wall_join(grid) and self.is_village_inside_wall(grid) and self.is_within_budget(num_grassland, num_forest, num_mountain):
            return True
        else:
            return False

    # Should be deprecated with solution
    def find_wall_coordinates(self, grid):
        wall_coordinates = []
        for y in range(0, self.Y_LIMIT):
            for x in range(0, self.X_LIMIT):
                if grid[y][x] == "X":
                    new_wall_coordinate = (x, y)
                    wall_coordinates += (new_wall_coordinate,)

        return wall_coordinates

    def calculate_living_space(self, wall_coordinates):
        # wall_coordinates = self.find_wall_coordinates(grid)
        num_wall_coordinates = len(wall_coordinates)
        wall_boundary = Polygon(wall_coordinates)
        # Calculate the number of interior point which is equal to the living space score.
        living_space = wall_boundary.area + 1 - num_wall_coordinates/2

        return living_space

    # Recursive branching until solution is found or money runs out. Start from every point in the grasslands. Ignoring water as walls for now
    def solve(self, grid):
        for y in range(0, self.Y_LIMIT):
            for x in range(0, self.X_LIMIT):
                if grid[y][x] == "G":
                    self.next_wall(deepcopy(grid), [x, y], [], 0, 0, 0)

        print(self.best_wall_path)
        print(self.best_wall_score)

    def next_wall(self, grid, current_wall_coordinate, current_path, num_grassland_wall, num_forest_wall, num_mountain_wall):
        if current_wall_coordinate[0] < 0 or current_wall_coordinate[0] >= self.Y_LIMIT or current_wall_coordinate[1] < 0 or current_wall_coordinate[1] >= self.X_LIMIT:
            return
        if grid[current_wall_coordinate[1]][current_wall_coordinate[0]] == "W":
            return
        if grid[current_wall_coordinate[1]][current_wall_coordinate[0]] == "G":
            num_grassland_wall += 1
            grid[current_wall_coordinate[1]][current_wall_coordinate[0]] = "X"
        if grid[current_wall_coordinate[1]][current_wall_coordinate[0]] == "F":
            num_forest_wall += 1
            grid[current_wall_coordinate[1]][current_wall_coordinate[0]] = "X"
        if grid[current_wall_coordinate[1]][current_wall_coordinate[0]] == "M":
            num_mountain_wall += 1
            grid[current_wall_coordinate[1]][current_wall_coordinate[0]] = "X"

        if not self.is_within_budget(num_grassland_wall, num_forest_wall, num_mountain_wall):
            if self.is_valid_solution(grid, num_grassland_wall, num_forest_wall, num_mountain_wall):
                current_path_score = self.calculate_living_space(current_path)
                if current_path_score > self.best_wall_score:
                    self.best_wall_score = current_path_score
                    self.best_wall_path = current_path
            return
        else:
            current_path.append(current_wall_coordinate)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0] - 1, current_wall_coordinate[1] - 1],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0] - 1, current_wall_coordinate[1]],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0], current_wall_coordinate[1] - 1],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0] + 1, current_wall_coordinate[1] - 1],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0] - 1, current_wall_coordinate[1] + 1],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0] + 1, current_wall_coordinate[1] + 1],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0] + 1, current_wall_coordinate[1]],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)
            self.next_wall(deepcopy(grid), [current_wall_coordinate[0], current_wall_coordinate[1] + 1],
                           current_path, num_grassland_wall, num_forest_wall, num_mountain_wall)

if __name__ == "__main__":
    solver = DefenceSolver()
    print(solver.solve(solver.MAP))
