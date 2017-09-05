from random import choice, randint
from collections import deque
from random import seed
import heapq
DIM = 20

#we want to make things deterministic, for better demonstration
seed(2)

class PriorityQueue:
    def __init__(self):
        self.backing_heap = []
        self.count = 0
        self.items = 0

    def push(self, priority, element):
        heapq.heappush(self.backing_heap, (priority, self.count, element))
        self.count += 1
        self.items += 1

    def pop(self):
        priority, _, element = heapq.heappop(self.backing_heap)
        self.items -= 1
        return priority, element

    def isEmpty(self):
        return self.items == 0

class Game:
    def __init__(self):
        self.start = (randint(0, DIM - 1), randint(0, DIM - 1))
        #should technically check that end != start...
        self.end = (randint(0, DIM - 1), randint(0, DIM - 1))
        #generate map!
        world = [[0 for _ in range(DIM)] for _ in range(DIM)]
        obstacles = []
        for i in range(150):
            r = randint(0, DIM - 1)
            c = randint(0, DIM - 1)
            if ((r, c) != self.start and (r, c) != self.end):
                world[r][c] = randint(0, 10)
                obstacles.append((r, c))
        self.world = world
        self.obstacles = obstacles
        self.frontier_points = []

    def _neighbors(self, r, c):
        n = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        valid = [(a, b) for a, b in n if 0 <= a < DIM and 0 <= b < DIM]
        return [point for point in valid if point not in self.obstacles]

    def bfs(self):
        queue = deque()
        seen = set()
        seen.add(self.start)
        queue.append(self.start)
        parents = {}
        processed = 0

        while len(queue) != 0:
            current = queue.popleft()
            #show the order we consider things in
            self.frontier_points.append(current)
            processed += 1
            if current == self.end:
                return parents, processed
            for n in self._neighbors(current[0], current[1]):
                if n not in seen:
                    seen.add(n)
                    queue.append(n)
                    parents[n] = current
        return {}, processed

    def manhattan_dist(self, r1, c1, r2, c2):
        return abs(r2 - r1) + abs(c2 - c1)

    def search(self):
        pass

    def _walk_backwards(self, parents):
        if len(parents) == 0:
            return []
        path = []
        current = self.end
        while current in parents:
            path.append(current)
            current = parents[current]
        path.append(current)
        return list(reversed(path))

    def solve(self):
        # parents, expanded = self.search()
        parents, expanded = self.bfs()
        path = self._walk_backwards(parents)

        print("Path length: {} Processed Nodes: {}".format(len(path), expanded))
        return {'obstacles' : self.obstacles, 'path' : path,
                'world' : self.world, 'frontier_points' : self.frontier_points,
                'start' : self.start, 'end' : self.end}

    def reset(self):
        self.__init__()
