import re
import pulp

input = [line for line in open("input.txt").read().splitlines()]

def solve_machine(targets, buttons):
    M = len(buttons)

    # Problem: minimize sum x_i
    prob = pulp.LpProblem("machine", pulp.LpMinimize)

    # Variables: x_i >= 0 integer
    x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in range(M)]

    # Objective
    prob += pulp.lpSum(x)

    # Constraints: for each counter j
    for j, t_j in enumerate(targets):
        prob += pulp.lpSum(x[i] for i in range(M) if j in buttons[i]) == t_j

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != "Optimal":
        raise RuntimeError("No optimal solution found")

    return sum(int(v.value()) for v in x)

def parse_line(line: str):
    # pattern between [] (ignored here)
    # pattern = re.search(r"\[(.*?)\]", line).group(1)

    # buttons (same as part 1)
    button_specs = re.findall(r"\((.*?)\)", line)
    buttons = []
    for spec in button_specs:
        spec = spec.strip()
        if not spec:
            buttons.append([])
        else:
            buttons.append(tuple(map(int, spec.split(","))))

    # targets between {}
    targets_str = re.search(r"\{(.*?)\}", line).group(1)
    targets = tuple(map(int, targets_str.split(",")))

    return buttons, targets

total = 0
for line in open("input.txt"):
    line = line.strip()
    if not line:
        continue
    buttons, targets = parse_line(line)
    total += solve_machine(targets, buttons)

print(total)
