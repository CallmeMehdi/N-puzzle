from heapq import heappop, heappush
import itertools

class PriorityQueue():
    REMOVED = '<removed-task>'
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()


    def add_task(self, task, priority=0):
        data =  [''.join(idx for idx in sub) for sub in task.data ] 
        data = ''.join(map(str, data))

        if data in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]

        self.entry_finder[data] = entry
        heappush(self.pq, entry)

    def remove_task(self, task):
        data = [''.join(idx for idx in sub) for sub in task.data ] 
        data = ''.join(map(str, data))
        entry = self.entry_finder.pop(data)
        entry[-1] = self.REMOVED

    def pop_task(self):
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is not self.REMOVED:
                data = [''.join(idx for idx in sub) for sub in task.data ] 
                data = ''.join(map(str, data))
                del self.entry_finder[data]
                return task
        return None