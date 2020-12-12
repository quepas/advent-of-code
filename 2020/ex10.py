from typing import List
import networkx as nx
import matplotlib.pyplot as plt


def count_adapter_min_jolts_diffs(in_jolts: List[int]):
    jolts = in_jolts.copy()
    diffs = {
        "1": 0,
        "2": 0,
        "3": 0
    }
    jolts.sort()
    # Insert the jolts of the charging outlet to the beginning
    jolts.insert(0, 0)
    # Append the jolts of the built-in adapter
    jolts.append(max(jolts) + 3)
    # Compute difference
    jolts_diff = diff(jolts)
    for k in jolts_diff:
        diffs[str(k)] += 1
    return diffs


def count_adapter_arrangment_jolts_diffs(jolts: List[int]):
    jolts.sort()
    dp = generate_adapter_path(jolts)
    return dp[0]


def generate_adapter_path(in_adapters: List[int]):
    adapters = in_adapters.copy()
    adapters.sort()
    adapters.insert(0, 0)
    adapters.append(max(adapters)+3)
    G = nx.DiGraph()
    for adapter in adapters:
        for k in range(1, 4):
            if adapter+k in adapters:
                G.add_edge(adapter, adapter+k)
    # If you need to see it ;)
    # nx.draw_kamada_kawai(G, with_labels=True)
    # plt.show()
    dp = {}
    for node in G.nodes:
        dp[node] = 0
    dp[max(adapters)] = 1
    for node in reversed(list(nx.algorithms.topological_sort(G))):
        # For each vertex v from node
        for in_neigh in G.successors(node):
            dp[node] += dp[in_neigh]
    return dp


def diff(jolts: List[int]):
    copied_jolts = jolts.copy()
    diff_jolts = []
    for k in range(1, len(copied_jolts)):
        diff_jolts.append(copied_jolts[k] - copied_jolts[k - 1])
    return diff_jolts


with open("input_10.txt", "r") as f:
    jolts = list(map(lambda x: int(x.strip()), f.readlines()))
    print("Jolts minimal diffs are = {}".format(count_adapter_min_jolts_diffs(jolts)))
    print("Jolts arrangments are = {}".format(count_adapter_arrangment_jolts_diffs(jolts)))
