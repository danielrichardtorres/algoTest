#depth first search
def DFS(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    for node in graph[start]:
        if node not in path:
            newpath = DFS(graph, node, end, path)
            if newpath:
                return newpath
    return None

