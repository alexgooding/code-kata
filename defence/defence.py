class DefenceSolver:

    def __init__(self):
        # G = grassland, F = forest, M = mountain, W = water, X = wall, B = blank
        self.MAP = [
                    ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "W", "W"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "W", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "F", "F", "F", "F"],
                    ["F", "F", "F", "F", "F", "F", "F", "F", "G", "G", "G", "F", "F", "F", "F", "F", "F", "F", "F", "M", "M", "M", "M", "M", "M", "M", "M", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "F", "W", "W", "W", "F", "F", "F", "F", "F"],
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
        self.BUDGET = 1000
        self.GRASSLAND_COST = 1
        self.FOREST_COST = 10
        self.MOUNTAIN_COST = 100

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
                print(grid[y][x])
                if grid[y][x] == "X":
                    if not self.have_two_neighbours_in_one_direction(grid, (y, x), y_limit, x_limit):
                        return False
        return True

    # A solution is valid if the wall joins together (assuming water is treated as a wall),
    # the village is inside the wall and the wall construction is within budget
    def is_valid_solution(self, grid, num_grassland, num_forest, num_mountain):
        if self.does_wall_join(grid) and self.is_village_inside_wall(grid) and self.is_within_budget(num_grassland, num_forest, num_mountain):
            return True
        else:
            return False

if __name__ == "__main__":
    solver = DefenceSolver()
    print(solver.does_wall_join(solver.MAP))
