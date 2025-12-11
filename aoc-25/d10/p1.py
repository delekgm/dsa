import re
from collections import deque

input = [line for line in open("input.txt").read().splitlines()]

def fewest_presses(pattern, buttons):
    N = len(pattern)
    
    # build target bitmask
    target = 0
    for i in range(N):
        if pattern[i] == "#":
            target |= (1 << i)
    
    button_masks = []
    for button in buttons:
        mask = 0
        for idx in button:
            mask |= (1 << idx)
        button_masks.append(mask)

    MAX_STATE = 1 << N
    dist = [float("inf")] * MAX_STATE
    dist[0] = 0
    q = deque()
    q.append(0)

    while q:
        cur = q.popleft()

        if cur == target:
            return dist[cur]
        
        for bm in button_masks:
            nxt = cur ^ bm
            if dist[nxt] > dist[cur] + 1:
                dist[nxt] = dist[cur] + 1
                q.append(nxt)

machines = []
for line in input:
    pattern = re.search(r"\[(.*?)\]", line).group(1)
    button_specs = re.findall(r"\((.*?)\)", line)
    buttons = []
    for spec in button_specs:
        if spec.strip() == "":
            buttons.append([])
        else:
            idxs = tuple(map(int, spec.split(",")))
            buttons.append(idxs)
    machines.append((pattern, buttons))

total = 0
for machine in machines:
    pattern, buttons = machine
    total += fewest_presses(pattern, buttons)

print(total)
