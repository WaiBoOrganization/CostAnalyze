# -*- coding: utf-8 -*-
import numpy as np
import time


def adjacency_matrix(matrix):
    m = matrix.shape[0]
    n = matrix.shape[1]
    adm = np.full((m * n, m * n), float("inf"))

    for i in range(m - 1):
        for j in range(n - 1):
            adm[i * n + j, i * n + j + 1] = (matrix[i, j] + matrix[i, j + 1]) / 2
            adm[i * n + j + 1, i * n + j] = (matrix[i, j] + matrix[i, j + 1]) / 2
            adm[i * n + j, (i + 1) * n + j] = (matrix[i, j] + matrix[i + 1, j]) / 2
            adm[(i + 1) * n + j, i * n + j] = (matrix[i, j] + matrix[i + 1, j]) / 2
    for i in range(m * n):
        adm[i, i] = 0
    for i in range(m - 1):
        adm[i * n + n - 1, (i + 1) * n + n - 1] = (matrix[i, n - 1] + matrix[i + 1, n - 1]) / 2
        adm[(i + 1) * n + n - 1, i * n + n - 1] = (matrix[i, n - 1] + matrix[i + 1, n - 1]) / 2
    for j in range(n - 1):
        adm[(m - 1) * n + j, (m - 1) * n + j + 1] = (matrix[m - 1, j] + matrix[m - 1, j + 1]) / 2
        adm[(m - 1) * n + j + 1, (m - 1) * n + j] = (matrix[m - 1, j] + matrix[m - 1, j + 1]) / 2
    return adm


def get_adj(matrix):
    m = matrix.shape[0]
    n = matrix.shape[1]
    adm = np.full((m * n, m * n), 0)
    for i in range(m - 1):
        for j in range(n - 1):
            adm[i * n + j, i * n + j + 1] = 1
            adm[i * n + j + 1, i * n + j] = 1
            adm[i * n + j, (i + 1) * n + j] = 1
            adm[(i + 1) * n + j, i * n + j] = 1
    for i in range(m * n):
        adm[i, i] = 0
    for i in range(m - 1):
        adm[i * n + n - 1, (i + 1) * n + n - 1] = 1
        adm[(i + 1) * n + n - 1, i * n + n - 1] = 1
    for j in range(n - 1):
        adm[(m - 1) * n + j, (m - 1) * n + j + 1] = 1
        adm[(m - 1) * n + j + 1, (m - 1) * n + j] = 1
    rst = {}
    for i in range(len(adm)):
        rst[i] = []
        for j in range(len(adm[0])):
            if adm[i][j] == 1:
                rst[i].append(j)
    return rst


# The dijkstra algorithm is implemented,
# the source point of the directed graph and the route is used as the input of the function,
# and the shortest path is the most output.
def dijkstra(graph, s1, s2, e1, e2):
    L = len(graph[0])
    src = L * s1 + s2
    end = L * e1 + e2
    adj = (get_adj(np.mat(graph)))
    graph = adjacency_matrix(np.mat(graph))
    t = time.clock()
    nodes = [i for i in range(len(graph))]  # Get all the nodes in the graph
    visited = []  # Represents a collection of nodes that have been routed to the shortest path
    if src in nodes:
        visited.append(src)
        nodes.remove(src)
    else:
        return None
    distance = {src: 0}  # Record the distance from the source node to each node
    for i in nodes:
        distance[i] = graph[src][i]  # initialization
        path = {src: []}  # Record the path from the source node to each node
    k = pre = src
    while nodes:
        mid_distance = float('inf')
        for v in visited:
            a = adj[v]
            for d in a:
                if d in visited:
                    continue
                new_distance = graph[src][v] + graph[v][d]
                if new_distance < mid_distance:
                    mid_distance = new_distance
                    k = d
                    pre = v
        graph[src][k] = mid_distance  # Distance update
        distance[k] = mid_distance  # Shortest path
        path[k] = [i for i in path[pre]]
        path[k].append(k)
        visited.append(k)
        nodes.remove(k)
    p = []
    p.append([src // L, src % L])
    for i in path[end]:
        p.append([i // L, i % L])
    map = {'method': "Dijkstra", 'path': p, 'cost': distance[end], 'time': (time.clock() - t) * 1000}
    return map
