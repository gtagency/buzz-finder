from random import choice, randint
from collections import deque

DIM = 15

class Game:
    def __init__(self):
        self.start = (randint(0, DIM - 1), randint(0, DIM - 1))
        #should technically check that end != start...
        self.end = (randint(0, DIM - 1), randint(0, DIM - 1))
        #generate map!
        world = [[0 for _ in range(DIM)] for _ in range(DIM)]
        obstacles = []
        for i in range(65):
            r = randint(0, DIM - 1)
            c = randint(0, DIM - 1)
            if ((r, c) != self.start and (r, c) != self.end):
                world[r][c] = randint(0, 10)
                obstacles.append((r, c))
        self.world = world
        self.obstacles = obstacles

    def _neighbors(self, r, c):
        n = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        valid = [(a, b) for a, b in n if 0 <= a < DIM and 0 <= b < DIM]
        return [point for point in valid if point not in self.obstacles]

    def bfs(self):
        #
        #Code here
        #
        return {}, 0

    def _walk_backwards(self, parents):
        if len(parents) == 0:
            return []
        path = [self.end]
        current = self.end
        while current in parents:
            path.append(parents[current])
            current = parents[current]
        return path[::-1]

    def solve(self):
        parents, expanded = self.bfs()
        # path = self._walk_backwards(parents)
        #uncomment me when you've written the search, and delete the line below
        path = [self.start, self._neighbors(self.start[0], self.start[1])[0]]

        print("Path length: {} Expanded Nodes: {}".format(len(path), expanded))
        return {'obstacles' : self.obstacles, 'path' : path, 'world' : self.world,
                'start' : self.start, 'end' : self.end}

    def reset(self):
        self.__init__()
