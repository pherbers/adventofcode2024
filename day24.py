import numpy as np
import re
from tqdm import tqdm
from day05 import Graph, kahn_topological_sort

with open(__file__.replace(".py", ".txt")) as f:
    input_text: str = f.read()

text_input, _, text_gates = input_text.partition("\n\n")

re_gate = re.compile(r"(\w{3})\s+(OR|XOR|AND)\s(\w{3})\s+\->\s+(\w{3})")

wire_inputs = {}
wire_outputs = {}

for wire_input in text_input.splitlines():
    wire, _, value = wire_input.partition(":")
    wire_inputs[wire] = bool(int(value))
del wire_input
gates = {}

for gate_line in text_gates.splitlines():
    m = re_gate.match(gate_line)
    if m:
        gates[m.group(4)] = (m.group(1), m.group(2), m.group(3))
        if m.group(4).startswith("z"):
            wire_outputs[m.group(4)] = 0
n_outputs = len(wire_outputs)
print(gates)
print(wire_inputs)
all_outputs = list(sorted(gates.keys()))
all_nodes = list(sorted(set(list(wire_inputs.keys()) + list(gates.keys()) + list(wire_outputs.keys()))))
all_nodes_indices = dict((all_nodes[i],i) for i in range(len(all_nodes)))

def poll_wire(wire, wire_values, gates):
    if wire in wire_values:
        return wire_values[wire]
    
    in1, method, in2 = gates[wire]
    r1 = poll_wire(in1, wire_values, gates)
    wire_values[in1] = r1
    r2 = poll_wire(in2, wire_values, gates)
    wire_values[in2] = r2
    if method == "AND":
        return r1 and r2
    elif method == "OR":
        return r1 or r2
    elif method == "XOR":
        return r1 ^ r2
    print("Incoherent state!")
    return False

def calc_circuit(wires_in: dict, wires_out: dict, gates: dict):
    wires_in = wires_in.copy()
    wires_out = wires_out.copy()
    
    for wire_out in wires_out.keys():
        wires_out[wire_out] = poll_wire(wire_out, wires_in, gates)
    
    num = wire_to_num(wires_out)
    return num

def wire_to_num(wire_out):
    score = 0
    for i, (_, w) in enumerate(sorted(wire_out.items())):
        score += 2**i * int(w)
    return score

def num_to_wire(num, length, prefix="x"):
    wires_in = {}
    for i in range(length):
        wires_in[f"{prefix}{i:02}"] = bool(num & (1 << i))
    return wires_in

score = calc_circuit(wire_inputs, wire_outputs.copy(), gates)
print(f"{score} ({score:b})")

init_x = wire_to_num(dict((k,v) for k,v in wire_inputs.items() if k.startswith("x")))
init_y = wire_to_num(dict((k,v) for k,v in wire_inputs.items() if k.startswith("y")))

len_x = len(list((k,v) for k,v in wire_inputs.items() if k.startswith("x")))
len_y = len(list((k,v) for k,v in wire_inputs.items() if k.startswith("y")))

def is_adder_check(gates):
    x = init_x
    y = init_y
    x_in = num_to_wire(x, len_x, prefix="x")
    y_in = num_to_wire(y, len_y, prefix="y")
    c = calc_circuit(x_in | y_in, wire_outputs.copy(), gates)
    if c != x + y:
        return False
    print("Found candidate")
    for x in range(2**len_x-1):
        for y in range(2**len_y-1):
            x_in = num_to_wire(x, len_x, prefix="x")
            y_in = num_to_wire(y, len_y, prefix="y")
            c = calc_circuit(x_in | y_in, wire_outputs.copy(), gates)
            if c != x + y:
                return False
    return True

for a,b,c,d in tqdm(np.ndindex((n_outputs,n_outputs,n_outputs,n_outputs)), total=n_outputs*n_outputs*n_outputs*n_outputs):
    if a == b or c == d or a == c or b == d or a == d or b == c:
        continue
    mod_gates = gates.copy()
    gi_a = all_outputs[a]
    gi_b = all_outputs[b]
    gi_c = all_outputs[c]
    gi_d = all_outputs[d]
    # modify circuit
    g_a = mod_gates[gi_a]
    g_b = mod_gates[gi_b]
    mod_gates[gi_a] = g_b
    mod_gates[gi_b] = g_a

    g_c = mod_gates[gi_c]
    g_d = mod_gates[gi_d]
    mod_gates[gi_c] = g_d
    mod_gates[gi_d] = g_c

    # Check for cycles
    g = Graph(len(all_nodes))
    for gate_o, (gate_a, _, gate_b) in mod_gates.items():
        g.add_edge(all_nodes_indices[gate_o], all_nodes_indices[gate_a])
        g.add_edge(all_nodes_indices[gate_o], all_nodes_indices[gate_b])
    is_cyclic = kahn_topological_sort(g)
    if is_cyclic == "Graph has at least one cycle":
        continue

    is_adder = is_adder_check(mod_gates)
    if is_adder:
        break

if is_adder:
    print("Found the one")
    print(a,b,c,d)
    print(sorted([gi_a,gi_b,gi_c,gi_d]))
