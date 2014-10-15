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


def lesson_sort(lessons):
    """Returns a topological sort of a list of lessons.

    Ties are broken arbitrarily.

    :param lessons: a list of lessons
    """
    slug_map = {lesson.slug: lesson for lesson in lessons}
    slug_graph = {lesson.slug: [succ.slug for succ in lesson.successors()]
                  for lesson in lessons}
    sorted_slugs = topological_sort(slug_graph)
    return [slug_map[slug] for slug in sorted_slugs]
