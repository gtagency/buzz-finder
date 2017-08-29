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
                world[r][c] = 1
                obstacles.append((r, c))
        self.world = world
        self.obstacles = obstacles

    def _neighbors(self, r, c):
        n = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        valid = [(a, b) for a, b in n if 0 <= a < DIM and 0 <= b < DIM]
        return [point for point in valid if point not in self.obstacles]

    def bfs(self):
        path = []
        queue = deque()
        seen = set()
        seen.add(self.start)
        queue.append(self.start)
        parents = {}
        expanded = 0

        while len(queue) != 0:
            current = queue.popleft()
            if current == self.end:
                return parents, expanded
            for n in self._neighbors(current[0], current[1]):
                expanded += 1
                if n not in seen:
                    seen.add(n)
                    queue.append(n)
                    parents[n] = current
        return {}, expanded

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
        path = self._walk_backwards(parents)
        print("Path length: {} Expanded Nodes: {}".format(len(path), expanded))
        return {'obstacles' : self.obstacles, 'path' : path,
                'start' : self.start, 'end' : self.end}

    def reset(self):
        self.__init__()
