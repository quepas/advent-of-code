import re
from typing import Dict, List
import networkx as nx


def parse_bags(bags: str) -> List[Dict]:
    if bags is None:
        return {}
    bag_list = []
    for bag in bags.split(","):
        g = re.match(r"^([1-9]) ([a-z ]*) bags?$", bag.strip())
        bag_list.append({
            "name": g.group(2),
            "count": int(g.group(1))
        })
    return bag_list


def parse_bag_rule(rule: str) -> Dict:
    bag_rule = {}
    g = re.match(r"^([a-z ]+) bags contain ([1-9] .* bag[s]?)*|no other bags\.$", rule)
    bag_rule["name"] = g.group(1)
    bag_rule["child"] = parse_bags(g.group(2))
    return bag_rule

def find_end_bags(G: nx.DiGraph):
    end_bags = []
    for node in G.nodes:
        if G.in_degree(node) == 0:
            end_bags.append(node)
    return end_bags


G = nx.DiGraph()
with open('input_7_test_2.txt', 'r') as f:
    mega_rule = {}

    for line in f.readlines():
        rule = parse_bag_rule(line.strip())
        for child in rule['child']:
            G.add_edge(child["name"], rule["name"], weight=child["count"])

print("Number of bags which can contain shiny gold bag = {}".format(len(nx.algorithms.descendants(G, "shiny gold"))))
end_bags = find_end_bags(G)

sum_all_paths = 0
added_edge = set()
for k in end_bags:
    for path in list(nx.algorithms.all_simple_edge_paths(G, k, "shiny gold")):
        path_weight = 1
        intermediate_edges = 0
        p = list(path)
        # p.reverse()
        print(p)
        for edge in p:
            if edge != p[0] and edge not in added_edge:
                intermediate_edges += G.get_edge_data(edge[0], edge[1])['weight']
                added_edge.add(edge)
            path_weight *= (G.get_edge_data(edge[0], edge[1])['weight'] + intermediate_edges)
        print(path_weight)
        print(intermediate_edges)
        sum_all_paths += path_weight + intermediate_edges# Add shiny gold !

# Add closest neighbours!

# 32584 too low
# 32678 too low
# 32690
# 32818
# 33594
# 33716
# 43526 too high
print(sum_all_paths)