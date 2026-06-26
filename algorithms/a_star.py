import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile != 0:
                goal_index = GOAL_STATE.index(tile)
                distance += abs(index // 3 - goal_index // 3) + abs(index % 3 - goal_index % 3)
        return distance

    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        frontier = [(self.heuristic(initial), initial)]
        best_cost = {initial: 0}
        explored = set()

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            _, node = heapq.heappop(frontier)

            if node in explored:
                continue

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            explored.add(node)
            nodes_expanded += 1

            for child in node.neighbors():
                if child in explored:
                    continue
                if child not in best_cost or child.cost < best_cost[child]:
                    best_cost[child] = child.cost
                    nodes_generated += 1
                    heapq.heappush(frontier, (child.cost + self.heuristic(child), child))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
