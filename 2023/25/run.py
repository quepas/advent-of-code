class Graph:

    def __init__(self):
        self.bi_connections = {}

    def add_edge(self, start: str, end: str) -> None:
        self._create_or_insert(start, end)
        self._create_or_insert(end, start)

    def get_edges(self, node: str) -> list[str]:
        return self.bi_connections[node]

    def _create_or_insert(self, key, value):
        if key not in self.bi_connections:
            self.bi_connections[key] = []
        self.bi_connections[key].append(value)

    def vertices(self) -> list[str]:
        return list(self.bi_connections.keys())


def parse_graph(lines: list[str]):
    G = Graph()
    for line in lines:
        chunks = line.strip().split()
        start_node = chunks[0][:-1]
        for end_node in chunks[1:]:
            G.add_edge(start_node, end_node.strip())
    return G


with open("input_test_1") as f:
    graph = parse_graph(f.readlines())
    print(graph.get_edges("pzl"))
