from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        nodes_generated = 1
        nodes_expanded = 0
        max_frontier_size = 1

        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=nodes_expanded,
                nodes_generated=nodes_generated,
                max_frontier_size=max_frontier_size,
                depth=0,
            )

        frontier = deque([initial])
        in_frontier = {initial}
        explored = set()

        while frontier:
            max_frontier_size = max(max_frontier_size, len(frontier))
            node = frontier.popleft()
            in_frontier.discard(node)
            explored.add(node)
            nodes_expanded += 1

            for child in node.neighbors():
                if child not in explored and child not in in_frontier:
                    nodes_generated += 1
                    if child.is_goal:
                        return SearchResult(
                            solution=child,
                            nodes_expanded=nodes_expanded,
                            nodes_generated=nodes_generated,
                            max_frontier_size=max_frontier_size,
                            depth=child.cost,
                        )
                    frontier.append(child)
                    in_frontier.add(child)

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
