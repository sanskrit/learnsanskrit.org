def topological_sort(graph):
    """Topological sort of a graph. Ties are broken arbitrarily.

    From http://www.logarithmic.net

    :param graph: an adjacency list. `graph[key] = successors`
    """
    count = {node: 0 for node in graph}
    for node in graph:
        for successor in graph[node]:
            count[successor] += 1

    candidates = [node for node in graph if not count[node]]
    result = []
    while candidates:
        node = candidates.pop()
        result.append(node)
        for successor in graph[node]:
            count[successor] -= 1
            if not count[successor]:
                candidates.append(successor)

    return result
