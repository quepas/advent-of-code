from collections import deque, Counter
from time import time


def parse_instructions(lines: list[str]) -> tuple[dict, ...]:
    in_edges = {}
    out_edges = {}
    ff_states = {}
    in_pulses = {}
    module_type = {}
    for line in lines:
        in_m, out_ms = line.split(" -> ")
        name, outputs = in_m.strip(), out_ms.strip().split(", ")
        # Flip-flop
        if name.startswith("%"):
            argument = name[1:]
            ff_states[argument] = "off"
            module_type[argument] = "flip-flop"
        # Inverter
        elif name.startswith("&"):
            argument = name[1:]
            in_pulses[argument] = {}
            module_type[argument] = "inverter"
        # Broadcaster (all low!)
        elif name == "broadcaster":
            argument = name
            module_type[argument] = "broadcaster"
        else:
            print(f"Not supported instruction: {name}")
            exit(-1)

        # Put output edges
        if argument not in out_edges:
            out_edges[argument] = []
        for node in outputs:
            out_edges[argument].append(node)
            # Put input edges
            if node not in in_edges:
                in_edges[node] = []
            in_edges[node].append(argument)

    for inverter in in_pulses.keys():
        for key, values in out_edges.items():
            if inverter in values:
                in_pulses[inverter].update({key: "low"})

    # print(f"in edges={in_edges}")
    print(f"out edges={out_edges}")
    print(f"ff_states={ff_states}")
    print(f"in_pulses={in_pulses}")
    print(f"module_type={module_type}")

    return out_edges, ff_states, in_pulses, module_type


with open("input") as f:
    out_edges, ff_states, in_pulses, module_type = parse_instructions(f.readlines())
    counter = Counter()
    t0 = time()
    for k in range(1, 10000):
        to_visit = deque([("button", "low", "broadcaster")])
        while len(to_visit) > 0:
            source, in_pulse, name = to_visit.popleft()
            if name == "rx" and in_pulse == "low":
                print(f"Fewest: {k}")
                exit()
            counter.update([in_pulse])
            # print(f"Visiting: {source} -{in_pulse}-> {name}")
            if name == "output" or name not in module_type:
                continue
            typ = module_type[name]
            outs = out_edges[name]
            match typ:
                case "broadcaster":
                    for out in outs:
                        to_visit.append((name, "low", out))
                case "flip-flop":
                    to_update = {}
                    for out in outs:
                        if in_pulse == "low":
                            if ff_states[name] == "off":
                                to_update[name] = "on"
                                to_visit.append((name, "high", out))
                            elif ff_states[name] == "on":
                                to_update[name] = "off"
                                to_visit.append((name, "low", out))
                        # else:
                        #     to_visit.append((name, in_pulse, out))
                    # ff_states update must happend after further signals have been sent
                    for key, value in to_update.items():
                        ff_states[key] = value
                case "inverter":
                    in_pulses[name][source] = in_pulse
                    # print(in_pulses)
                    saved_pulses = in_pulses[name]
                    pulse = None
                    if all(map(lambda x: x == "high", saved_pulses.values())):
                        pulse = "low"
                    else:
                        pulse = "high"
                    for out in outs:
                        to_visit.append((name, pulse, out))
                case _:
                    print("Unknown!")

        # print(f"ff_states={ff_states}")
        # print(f"in_pulses={in_pulses}")
    t1 = time()
    print(counter)
    print(f"Result={counter['low'] * counter['high']}; took={t1-t0}s")
