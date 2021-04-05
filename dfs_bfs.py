
def dfs(visited,graph, node):
    if node not in visited :
        print(node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)

def dfs(graph, start):
    visited,stack = set(),[start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            stack.extend(graph[vertex]-visited)
    return visited

def bfs(graph,start):
    visited = set()
    stack = [start]

    while stack:
        vertex = stack.pop(0)
        if vertex not in visited:
            print(vertex)
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
    return visited

graph = {'A': {'B', 'C'},
         'B': {'A', 'D', 'E'},
         'C': {'A', 'F'},
         'D': {'B'},
         'E': {'B', 'F'},
         'F': {'C', 'E'}}

# bfs(graph, 'A')
dfs(graph, 'A')

# adjacency matrix representation is that it takes constant time (just one memory access) to determine whether or not there is an edge between any two given vertices.
def dfs_adj_mat(graph,start,visited):
    visited[start] = True
    for i in range(len(visited)):
        if (graph[start][i] == 1 and not visited[i]):
            dfs(graph,i,visited)
