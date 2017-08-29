from random import choice, randint
from collections import deque


class Game:
    def __init__(self):
        self.start = (randint(0, 14), randint(0, 14))
        #should technically check that end != start...
        self.end = (randint(0, 14), randint(0, 14))
        #generate map!
        world = [[0 for _ in range(15)] for _ in range(15)]
        obstacles = []
        for i in range(75):
            r = randint(0, 14)
            c = randint(0, 14)
            if ((r, c) != self.start and (r, c) != self.end):
                world[r][c] = 1
                obstacles.append((r, c))
        self.world = world
        self.obstacles = obstacles
    
    def _neighbors(self, r, c):
        n = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        valid = [(a, b) for a, b in n if 0 <= a < 15 and 0 <= b < 15]
        return [(a, b) for a, b in valid if (a, b) not in self.obstacles] 

    def bfs(self):
        path = []
        queue = deque()
        seen = set()
        seen.add(self.start)
        queue.append(self.start)
        parents = {}
        while len(queue) != 0:
            current = queue.popleft()
            if current == self.end:
                return parents
            for n in self._neighbors(current[0], current[1]):
                if n not in seen:
                    seen.add(n)
                    queue.append(n)
                    parents[n] = current
        return {} 

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
        #get the path here
        # path = [[0, 0], [0, 1], [0, 2], [0, 3],
                # [1, 3], [2, 3], [3, 3],
                # [3, 2], [3, 1], [3, 0],
                # [2, 0], [1, 0], [0, 0]]
        path = self._walk_backwards(self.bfs())

        # path = [[0, 0], [0, 1], [0, 2], [0, 3],
                # [1, 3], [2, 3], [3, 3],
                # [3, 2], [3, 1], [3, 0],
                # [2, 0], [1, 0], [0, 0]]
        return {'obstacles' : self.obstacles, 'path' : path,
                'start' : self.start, 'end' : self.end}
    
    def reset(self):
        self.__init__()
