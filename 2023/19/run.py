import re


class Part:
    def __init__(self, part_repr: str):
        match = re.match(r"{x=([0-9]+),m=([0-9]+),a=([0-9]+),s=([0-9]+)}", part_repr)
        if match is not None:
            self.category = {
                "x": int(match.group(1)),
                "m": int(match.group(2)),
                "a": int(match.group(3)),
                "s": int(match.group(4))
            }

    def __repr__(self):
        return str(self.category)

    def value(self) -> int:
        return sum(self.category.values())


class Workflow:

    def __init__(self, workflow_repr: str):
        conditions_start = workflow_repr.index("{")
        self.name = workflow_repr[:conditions_start]
        # Get rid of bracelets {} around conditions
        conditions = workflow_repr[conditions_start + 1:-1].split(",")
        self.else_case = conditions.pop()
        self.conditions = list(map(self._parse_condition, conditions))

    def apply(self, part: Part) -> str:
        for condition in self.conditions:
            var, operator, value, label = condition
            part_value = part.category[var]
            if operator == "<" and part_value < value:
                return label
            if operator == ">" and part_value > value:
                return label
        return self.else_case

    def _parse_condition(self, condition: str) -> tuple[str, str, int, str]:
        category = condition[0]
        operator = condition[1]
        label_start = condition.index(":")
        value = int(condition[2:label_start])
        label = condition[label_start + 1:]
        return category, operator, value, label


def parse_info(content: str) -> tuple[dict[str, Workflow], list[Part]]:
    workflow_repr, part_repr = content.split("\n\n")
    workflows = dict(map(lambda workflow: (workflow.name, workflow), map(Workflow, workflow_repr.split("\n"))))
    parts = list(map(Part, part_repr.split("\n")))
    return workflows, parts


with open("input") as f:
    workflows, parts = parse_info(f.read())
    print(f"Found: {len(workflows)} workflows and {len(parts)} parts")

    total_value = 0
    for part in parts:
        print(f"Part: {part}")
        # 1. Apply in worklofw
        next_label = "in"
        while next_label not in ["A", "R"]:
            print(f"Next workflow: {next_label}")
            next_workflow = workflows[next_label]
            next_label = next_workflow.apply(part)
        if next_label == "A":
            print("Accepted!")
            total_value += part.value()
        else:
            print("Rejected!")
    print(f"Total value of accepted parts: {total_value}")

# Too low: 362321

# Second part
"""
 a<2006, a<1716 => 1715
 m>2090,m>1548,m>838 => 4000-838=3162
 x<2440, x>2662 => 4000 - (2662-2440) = 3738
 s>3448 => 4000-3448 = 552

"""