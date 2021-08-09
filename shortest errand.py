import math
import heapq


class Heap_min:
    """
    This class was done with reference to FIT 1008 resources. modified heap class that support tuple
    """

    def __init__(self, n):
        self.heap_list = [math.inf] * n
        self.pos_lst = [math.inf] * n
        self.count = 1

    def swap(self, i, j):
        self.heap_list[i], self.heap_list[j] = self.heap_list[j], self.heap_list[i]
        if self.heap_list[i] != math.inf and self.heap_list[j] != math.inf:
            temp_1 = self.heap_list[i][0]
            temp_2 = self.heap_list[j][0]
            self.pos_lst[temp_1], self.pos_lst[temp_2] = self.pos_lst[temp_2], self.pos_lst[temp_1]

    def smallest_child(self, k):
        """This function is get the smallest child of the element at index k"""

        if 2 * k == self.count - 1 or self.heap_list[2 * k][1] < self.heap_list[2 * k + 1][1]:
            return 2 * k
        elif self.heap_list[2 * k][1] == self.heap_list[2 * k + 1][1]:
            if self.heap_list[2 * k][1] > self.heap_list[2 * k + 1][1]:
                return 2 * k
            else:
                return 2 * k + 1
        else:
            return 2 * k + 1

    def update_Q(self, v, weight):
        """
        This function updates the value of an entry in the heap
        Time complexity: O(log k)
        :param v: vertex and its weight
        :param weight:
        :return:
        """
        pos = self.pos_lst[v]
        if pos !=  math.inf:
            self.heap_list[pos] = (v, weight)
            self.rise(pos)

    def rise(self, k):
        """
        This function rise an element in the min heap
        Time complexity:O(logk)
        """

        k -= 1
        while k > 1:
            if self.heap_list[k // 2] == math.inf or self.heap_list[k][1] < self.heap_list[k // 2][1]:
                self.swap(k, k // 2)
                k = k // 2
            elif self.heap_list[k][1] == self.heap_list[k // 2][1]:
                if self.heap_list[k][1] > self.heap_list[k // 2][1]:
                    self.swap(k, k // 2)
                    k = k // 2
                else:
                    return k
            return k

    def push(self, item):
        """
        This function is to push an element into the min heap
        Time complexity:O(log k)
        """
        if self.count < len(self.heap_list):
            self.heap_list[self.count] = item

        self.pos_lst[item[0]] = self.count

        if self.count == 1:
            pos = 1
            self.count += 1
        else:
            self.count += 1
            pos = self.rise(self.count)

        self.pos_lst[item[0]] = pos

    def sink(self, k):
        '''
        This function is to sink an element through the heap
        Time complexity:O(logk)
        Space complexity:O(1)
        Error handling: None
        Parameters: Index of element to sink
        Return: None
        '''

        while 2 * k < self.count:
            child_ind = self.smallest_child(k)

            if self.heap_list[k][1] < self.heap_list[child_ind][1]:
                self.pos_lst[self.heap_list[k][0]] = k
                break

            elif self.heap_list[k][1] == self.heap_list[child_ind][1]:
                if self.heap_list[k][1] > self.heap_list[child_ind][1]:
                    self.pos_lst[self.heap_list[k][0]] = k

                    break
                else:
                    self.swap(child_ind, k)
            else:
                self.swap(child_ind, k)

            k = child_ind

    def pop(self):
        """
        This function pops the first element in the min heap
        Time complexity:O(logk)
        """
        self.swap(1, self.count - 1)
        element = self.heap_list[self.count - 1]
        self.count -= 1
        self.sink(1)

        if element != math.inf:
            self.pos_lst[element[0]] = math.inf

        return element


class Vertex:
    """
    represent vertex object, store edges connected and flags if this vertex is an ice or ice cream location
    """

    def __init__(self):
        self.edges = []
        self.is_ice_cream = False
        self.is_ice = False


class Edge:
    """
    represent edge object with current vertex, adjacent vertex and weight of edge
    """

    def __init__(self, u, v, w):
        self.edge_value = (u, v, w)


class Graph:
    def __init__(self, gfile):
        self.non_weight_graph = None
        self.num_vertices = 0
        self.edge_list = []
        self.vertices = None
        self.build_graph(gfile)

    def build_graph(self, gfile):
        """
        This function builds a graph for task 2 and store vertices for task 3
        :param gfile: name of text file to be processed
        :weight complexity : O(V^2) where V is the number of vertices in the graph
        :space complexity : O(V^2) where V is the number of vertices in the graph
        """
        f = open(gfile, 'r+')
        count = 0
        for line in f:
            if count == 0:
                self.num_vertices = int(line)
                self.non_weight_graph = [[False for j in range(self.num_vertices)] for i in range(self.num_vertices)]
                self.vertices = [None] * self.num_vertices
                # initialise vertex list
                for i in range(self.num_vertices):
                    self.vertices[i] = Vertex()

            else:

                line = line.strip("\n")
                line = line.split(" ")
                self.edge_list.append(line)
            count += 1

        for e in self.edge_list:
            u, v, w = int(e[0]), int(e[1]), int(e[2])
            self.add_edge(u, v, w)

    def add_edge(self, u, v, w):
        """
        add edges between two vertices
        :param u: vertex id one
        :param v: vertex id two
        :param w:  weight of edge
        :weight complexity : O(1)
        """

        # bidirectional so create two edges
        edge = Edge(u, v, w)
        edge_2 = Edge(v, u, w)

        # task 2 , no edge weight so use boolean to represent
        self.non_weight_graph[u][v] = True
        self.non_weight_graph[v][u] = True

        # task 3
        self.vertices[u].edges.append(edge)
        self.vertices[v].edges.append(edge_2)

    def shallowest_spanning_tree(self):
        """
        This function finds the shallowest spanning tree of the graph stored in your
        class Graph (a spanning tree which minimises the number of edges from the root of the spanning tree
        :complexity : O(V^2+ EV) where E is the number of edges in the graph and
                     V is the number of vertices in the graph.
        :return: vertex ID of the root which gives the shallowest spanning tree and
                 an integer to represent the height of the shallowest spanning tree
        """

        index_v = 0
        all_distances = []
        for v in range(self.num_vertices):
            dist = self.bfs(v)
            all_distances.append((v, max(dist)))

        max_depth = all_distances[0][1]
        for i in range(self.num_vertices):
            if all_distances[i][1] < max_depth:
                max_depth = all_distances[i][1]
                index_v = all_distances[i][0]
        return (index_v, max_depth)

    def bfs(self, src):
        """
        breadth first search algorithm, modified from lecture slides week 9 and notes
        :param src: starting vertex
        :complexity : O(V+E) where E is the number of edges in the graph and
                      V is the number of vertices in the graph.
        :return: distances of source vertex to the rest of the vertex
        """
        dist = [math.inf] * self.num_vertices
        dist[src] = 0
        queue = []
        heapq.heapify(queue)
        heapq.heappush(queue, src)
        while len(queue) > 0:
            u = heapq.heappop(queue)
            for v in range(self.num_vertices):
                if dist[v] == math.inf and self.non_weight_graph[u][v] is True:
                    dist[v] = dist[u] + 1
                    heapq.heappush(queue, v)
        return dist

    def dijkstra(self, src, target):
        """
        Dijkstra's Algorithm. Modified from lecture slides week 8 and notes chapter 13.
        :param src: starting vertex
        :complexity : O(E log (V)) where E is the number of edges in the graph and V is the number of vertices in the graph.
        :return: distance of source vertex to the target vertex
        """
        dist = [math.inf] * self.num_vertices
        dist[src] = 0
        pred = [0] * self.num_vertices
        Q = Heap_min(self.num_vertices)  # priority Q
        Q.push((src, 0))  # push source to priority Q

        while Q:
            temp = Q.pop()
            if temp == math.inf:
                break
            (index, weight) = temp
            edge_list = self.vertices[index].edges

            for i in range(len(edge_list)):
                u, v, w = edge_list[i].edge_value
                # relaxation
                if dist[v] > dist[u] + w:
                    if dist[v] is not math.inf:
                        # Q is updated because relaxation improves a distances estimate
                        Q.update_Q(v, w)
                        dist[v] = dist[u] + w
                        pred[v] = u
                    # discovered new vertex, so update distance and store pred vertex
                    else:
                        dist[v] = dist[u] + w
                        pred[v] = u
                        Q.push((v, w))

        target_dist = dist[target]
        path = self.reconstruct_path(src, target, pred)

        return (target_dist, path)

    def reconstruct_path(self, src, target, pred):
        """
        reconstruct vertices of the shortest path from source to target by backtracking through the pred heap_list.
        :param src: source vertex
        :param target: target vertex
        :param pred: predecessor list
        :complexity: O(n) where n is the length of path
        :return: vertices traversed
        """
        path = [target]
        while target != src:
            path.append(pred[target])
            target = pred[target]
        return list(reversed(path))

    def build_new_graph(self):
        """
        this function build new graphs for task 3. each old vertex in graph will have extra two new vertex to represent
        ice and ice cream location.
        (example, let number of vertices in old graph = 5
        vertex 1 will have new vertex 6 to represent ice location and 11 to represent ice cream location ( 1+5 and 1+5+5 respectively))
        This new vertices in new graph of ice and ice cream location are connected in the same direction and weight as old graph.

        This 3 graphs (old, ice, ice cream) can be linked with creating new edges when it is found that the vertex is
        connected to a ice or ice cream location.
        ice location will only be connected from normal location and ice cream location will only be connected from ice location.
        example, this means that we "cannot travel" from normal location to ice cream location, only from ice to ice cream location.

        this ensures :
            # 1) the order to travel ice location first then ice cream location
            # 2) traversed all possible new and old vertices to find accurate shortest path

        :return: references of new vertices list that connect the 3 graphs and original number of vertices in old graph
        """
        # Build a new graph with new two vertices for each vertices to represent ice loc, ice cream loc and non loc
        new_vertices_lst = [None] * (self.num_vertices * 3)
        num_old_vertices = self.num_vertices
        for i in range(self.num_vertices * 3):
            new_vertices_lst[i] = Vertex()

        for edge in self.edge_list:

            # constants for current loop
            source, target, weight = int(edge[0]), int(edge[1]), int(edge[2])

            # represent new vertices for ice location
            ice_source = source + num_old_vertices
            ice_target = target + num_old_vertices

            # represent new vertices for ice cream location
            ice_cream_source = source + num_old_vertices * 2
            ice_cream_target = target + num_old_vertices * 2

            # represent new edge, "bi" means bidirectional
            new_edge = Edge(source, target, weight)
            new_edge_bi = Edge(target, source, weight)

            new_vertices_lst[source].edges.append(new_edge)
            new_vertices_lst[target].edges.append(new_edge_bi)

            ice_new_edge = Edge(ice_source, ice_target, weight)
            ice_new_edge_bi = Edge(ice_target, ice_source, weight)

            new_vertices_lst[ice_source].edges.append(ice_new_edge)
            new_vertices_lst[ice_target].edges.append(ice_new_edge_bi)

            ice_cream_new_edge = Edge(ice_cream_source, ice_cream_target, weight)
            ice_cream_new_edge_bi = Edge(ice_cream_target, ice_cream_source, weight)

            new_vertices_lst[ice_cream_source].edges.append(ice_cream_new_edge)
            new_vertices_lst[ice_cream_target].edges.append(ice_cream_new_edge_bi)

            # if source or target vertex is an ice location or ice cream location, create a new edge to link and
            # connect the normal location to ice location; ice location to ice cream location

            # if self.vertices[source].is_ice :
            #     link_edge = Edge(source, ice_target, weight)
            #     new_vertices_lst[source].edges.append(link_edge)


            if self.vertices[target].is_ice:
                link_edge = Edge(source, ice_target, weight)
                new_vertices_lst[source].edges.append(link_edge)


            # if self.vertices[source].is_ice_cream:
            #     link_edge = Edge(ice_source, ice_cream_target, weight)
            #     new_vertices_lst[ice_source].edges.append(link_edge)


            if self.vertices[target].is_ice_cream:
                link_edge = Edge(ice_source, ice_cream_target, weight)
                new_vertices_lst[ice_source].edges.append(link_edge)


            if self.vertices[source].is_ice :
                link_edge = Edge(source, ice_source, 0)
                new_vertices_lst[source].edges.append(link_edge)
                #new_vertices_lst[ice_source].edges.append(link_edge_bi)

            if self.vertices[source].is_ice_cream:
                link_edge = Edge(ice_source, ice_cream_source, 0)
                new_vertices_lst[ice_source].edges.append(link_edge)



        return new_vertices_lst, num_old_vertices

    def shortest_errand(self, start, destination, ice_locs, ice_cream_locs):
        """
       This function will find the shortest walk from start to pick up some ice, and then some ice cream,
       then to destination.

       :param start: vertex id of starting vertex
       :param destination: vertex id of ending vertex
       :param ice_locs: list of vertex id that represent ice locations
       :param ice_cream_locs: list of vertex id that represent ice cream locations
       :complexity : O(Elog(V)), where E is the number of edges in the graph and V is the number of vertices in the graph.
       :return: length of the shortest walk, and list of the vertices that represent the shortest walk from home to destination
       """
        for loc in ice_locs:
            self.vertices[loc].is_ice = True
        for loc in ice_cream_locs:
            self.vertices[loc].is_ice_cream = True

        # solve single vertex graph
        if self.num_vertices == 1:
            return (0, [0])

        # solve graphs where there are overlaps between start, destination and ice location and ice cream location,
        # find shortest path straight
        if start is ice_locs[0] or destination is ice_cream_locs[0]:
            return self.dijkstra(start,destination)

        # if start is ice_cream_locs[0] and destination is ice_locs[0]:
        #     return self.dijkstra(ice_locs[0],ice_cream_locs[0])
        if (start in ice_locs and start in ice_cream_locs) or (
                destination in ice_locs and destination in ice_cream_locs):
            return self.dijkstra(start, destination)

        new_vertices_lst, num_old_vertices = self.build_new_graph()

        self.vertices = new_vertices_lst
        self.num_vertices = len(new_vertices_lst)

        destination = destination + num_old_vertices * 2
        result = self.dijkstra(start, destination)
        shortest_distance = result[0]
        path = result[1]
        print(path)
        # decrement path values to original value because new vertices were used to represent the link to ice and cream location
        for i in range(len(path)):
            if path[i] >= num_old_vertices * 2:
                path[i] -= num_old_vertices * 2
            elif path[i] >= num_old_vertices:
                path[i] -= num_old_vertices

        for i in range(len(path) - 1, 0, -1):
            if path[i] == path[i-1]:
                path.remove(path[i])

        return shortest_distance, path




