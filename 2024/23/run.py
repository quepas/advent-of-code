from collections import deque
Pair = tuple[str, str]


class Graph:

    def __init__(self) -> None:
        # Bi-directional connections
        self.connections = {}

    def add_connection(self, a: str, b: str) -> None:
        if a not in self.connections:
            self.connections[a] = set([b])
        else:
            self.connections[a].add(b)

    def add_edge(self, a: str, b: str) -> None:
        self.add_connection(a, b)
        self.add_connection(b, a)

    def add_all(self, pairs: list[Pair]) -> None:
        for a, b in pairs:
            self.add_edge(a, b)

    def nodes(self) -> list[str]:
        return list(self.connections.keys())

    def adjacent(self, node: str) -> list[str]:
        return self.connections.get(node, [])

    def __repr__(self) -> str:
        return str(self.connections)

count_triplets = 0

def find_triplets(G: Graph, start: str) -> list[tuple[str, ...]]:
    global count_triplets
    Q = deque([(0, start)])
    visited = []

    visited_list = []
    found = []
    
    while Q:
        level, node = Q.pop()
        print(level, node, G.adjacent(node))
        if node in visited or level > 3:
            continue
        visited.append(node)
        visited_list.append(node)
        for neighbour in G.adjacent(node):
            if neighbour == start and level == 2:
                print("Found triplet!", visited_list[-3:])
                found.append(visited_list[-3:])
                count_triplets += 1
            if neighbour in visited:
                continue
            Q.append((level + 1, neighbour))
    return found


with open("input_test1", "r") as f:
    connections = list(
        map(lambda line: tuple(sorted(line.strip().split("-"))), f.readlines())
    )
    t = Graph()
    t.add_all(connections)
    all_found = []
    for node in t.nodes():
        print("Testing node:", node)
        found = find_triplets(t, node)
        all_found.extend(found)
    print(all_found, len(all_found))
    with_t = list(filter(lambda l: any(map(lambda n: n.startswith("t"), l)), all_found))
    print(with_t)

    # print(count_triplets)
    # ds = build_disjoint_set(connections)
    # print(list(combinations(ds.sets[0], 3)))
