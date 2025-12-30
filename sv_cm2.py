import pyperclip
import time
import re

start_time = time.perf_counter()
scene_blocks = {}
scene_connections = []
d_ff_count = 0
class block:
    def __init__(self, index: int, x: int, y: int, z: int, params: list[int], name: str):
        self.index = str(index)
        self.x = str(x)
        self.y = str(y)
        self.z = str(z)
        self.params = [str(i) for i in params]
        self.world_name = name
        if not self.params:
            self.final_look = ",".join([self.index, "0", self.x, self.y, self.z])+",;"
        else:
            self.final_look = ",".join([self.index, "0", self.x, self.y, self.z, "+".join(self.params)])+";"
    
    def add_to_blocks(self):
        global scene_blocks
        scene_blocks[len(scene_blocks)] = self



class PD_ff:
    """
    Orientation counter-clockwise
    start_pos - x, y, z
    """
    def __init__(self, orientation: int, start_pos: list[int], input_block: block):
        global d_ff_count
        self.blocks = {}
        self.connections = []
        self.type = "posedge"
        self.index = d_ff_count
        if orientation == 0:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]+1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]+2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]+3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]+4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
        elif orientation == 90:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]-1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]-2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]-3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]-4, [], f"d_ff_2node{d_ff_count}")
        elif orientation == 180:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]-1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]-2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]-3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]-4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
        elif orientation == 270:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]+1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]+2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]+3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]+4, [], f"d_ff_2node{d_ff_count}")

        self.connections.append(scene_connection(f"d_ff_node{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_xor{d_ff_count}", f"d_ff_and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_and{d_ff_count}", f"d_ff_t_ff{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_2node{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(input_block.world_name, f"d_ff_node{d_ff_count}"))
        d_ff_count += 1

    def point_to_scene(self):
        global scene_blocks, d_ff_count, connections
        next_free_index = len(scene_blocks)
        for index, block in self.blocks.items():
            scene_blocks[next_free_index+index] = block
        for connection in self.connections:
            scene_connections.append(connection)

class ND_ff:
    """
    Orientation counter-clockwise
    start_pos - x, y, z
    """
    def __init__(self, orientation: int, start_pos: list[int], input_block: block):
        global d_ff_count
        self.blocks = {}
        self.connections = []
        self.type = "negedge"
        self.index = d_ff_count
        if orientation == 0:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]+1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]+2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]+3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]+4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0]+5, start_pos[1], start_pos[2], [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0]+6, start_pos[1], start_pos[2], [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0]+7, start_pos[1], start_pos[2], [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0]+8, start_pos[1], start_pos[2], [], f"d_ff_2and{d_ff_count}")
        elif orientation == 90:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]-1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]-2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]-3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]-4, [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0], start_pos[1], start_pos[2]-5, [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0], start_pos[1], start_pos[2]-6, [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0], start_pos[1], start_pos[2]-7, [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0], start_pos[1], start_pos[2]-8, [], f"d_ff_2and{d_ff_count}")
        elif orientation == 180:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0]-1, start_pos[1], start_pos[2], [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0]-2, start_pos[1], start_pos[2], [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0]-3, start_pos[1], start_pos[2], [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0]-4, start_pos[1], start_pos[2], [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0]-5, start_pos[1], start_pos[2], [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0]-6, start_pos[1], start_pos[2], [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0]-7, start_pos[1], start_pos[2], [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0]-8, start_pos[1], start_pos[2], [], f"d_ff_2and{d_ff_count}")
        elif orientation == 270:
            self.blocks[0] = block(15, start_pos[0], start_pos[1], start_pos[2], [], f"d_ff_node{d_ff_count}")
            self.blocks[1] = block(3, start_pos[0], start_pos[1], start_pos[2]+1, [], f"d_ff_xor{d_ff_count}")
            self.blocks[2] = block(1, start_pos[0], start_pos[1], start_pos[2]+2, [], f"d_ff_and{d_ff_count}")
            self.blocks[3] = block(5, start_pos[0], start_pos[1], start_pos[2]+3, [0, 0], f"d_ff_t_ff{d_ff_count}")
            self.blocks[4] = block(15, start_pos[0], start_pos[1], start_pos[2]+4, [], f"d_ff_2node{d_ff_count}")
            self.blocks[5] = block(15, start_pos[0], start_pos[1], start_pos[2]+5, [], f"d_ff_inode{d_ff_count}")
            self.blocks[6] = block(5, start_pos[0], start_pos[1], start_pos[2]+6, [0, 0], f"d_ff_2t_ff{d_ff_count}")
            self.blocks[7] = block(0, start_pos[0], start_pos[1], start_pos[2]+7, [], f"d_ff_not{d_ff_count}")
            self.blocks[8] = block(1, start_pos[0], start_pos[1], start_pos[2]+8, [], f"d_ff_2and{d_ff_count}")

        self.connections.append(scene_connection(f"d_ff_node{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_xor{d_ff_count}", f"d_ff_and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_and{d_ff_count}", f"d_ff_t_ff{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_2node{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_t_ff{d_ff_count}", f"d_ff_xor{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_inode{d_ff_count}", f"d_ff_2t_ff{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_inode{d_ff_count}", f"d_ff_not{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_not{d_ff_count}", f"d_ff_2and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_2t_ff{d_ff_count}", f"d_ff_2and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_2and{d_ff_count}", f"d_ff_and{d_ff_count}"))
        self.connections.append(scene_connection(f"d_ff_2and{d_ff_count}", f"d_ff_2t_ff{d_ff_count}"))
        self.connections.append(scene_connection(input_block.world_name, f"d_ff_node{d_ff_count}"))
        d_ff_count += 1

    def point_to_scene(self):
        global scene_blocks, d_ff_count, connections
        next_free_index = len(scene_blocks)
        for index, block in self.blocks.items():
            scene_blocks[next_free_index+index] = block
        for connection in self.connections:
            scene_connections.append(connection)

class scene_connection:
    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst


output_code_blocks = ""
output_code_connections = ""

def build_scene():
    global scene_blocks, scene_connections, output_code_connections, output_code_blocks, end_time

    for connection in scene_connections:
        output_code_connections += [str(index+1) for index, block in scene_blocks.items() if block.world_name == connection.src][0]
        output_code_connections += ","
        output_code_connections += [str(index+1) for index, block in scene_blocks.items() if block.world_name == connection.dst][0]
        output_code_connections += ";"

    for index, block in scene_blocks.items():
        output_code_blocks += block.final_look

    copy_or_print = input("Copy or print: ").lower()
    end_time = time.perf_counter()
    if copy_or_print == "print":
        print(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??")
    else:
        pyperclip.copy(output_code_blocks[:-1]+"?"+output_code_connections[:-1]+"??")

class always_relay_on:
    def __init__(self, block_to_relay_on, d_ff, output_block):
        if d_ff.type == "posedge":
            scene_connections.append(scene_connection(block_to_relay_on.world_name, f"d_ff_and{d_ff.index}"))
            scene_connections.append(scene_connection(f"d_ff_t_ff{d_ff.index}", output_block.world_name))
        elif d_ff.type == "negedge":
            scene_connections.append(scene_connection(block_to_relay_on.world_name, f"d_ff_inode{d_ff.index}"))
            scene_connections.append(scene_connection(f"d_ff_2node{d_ff.index}", output_block.world_name))

and_gate_count = 0
def and_gate(input1, input2, output, position: list[int]) -> None:
    global scene_connections, scene_blocks, and_gate_count

    gate = block(1, position[0], position[1], position[2], [], f"and_gate{and_gate_count}")
    gate.add_to_blocks()
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    scene_connections.append(scene_connection(gate.world_name, output))
    and_gate_count += 1

not_gate_count = 0
def not_gate(input, output, position: list[int]) -> None:
    global scene_connections, scene_blocks, not_gate_count

    gate = block(0, position[0], position[1], position[2], [], f"not_gate{not_gate_count}")
    gate.add_to_blocks()
    scene_connections.append(scene_connection(input, gate.world_name))
    scene_connections.append(scene_connection(gate.world_name, output))
    not_gate_count += 1

or_gate_count = 0
def or_gate(input1, input2, output, position: list[int]) -> None:
    global scene_connections, scene_blocks, or_gate_count

    gate = block(2, position[0], position[1], position[2], [], f"or_gate{or_gate_count}")
    gate.add_to_blocks()
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    scene_connections.append(scene_connection(gate.world_name, output))
    or_gate_count += 1

xor_gate_count = 0
def xor_gate(input1, input2, output, position: list[int]) -> None:
    global scene_connections, scene_blocks, xor_gate_count

    gate = block(3, position[0], position[1], position[2], [], f"xor_gate{xor_gate_count}")
    gate.add_to_blocks()
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    scene_connections.append(scene_connection(gate.world_name, output))
    xor_gate_count += 1

nor_gate_count = 0
def nor_gate(input1, input2, output, position: list[int]) -> None:
    global scene_connections, scene_blocks, nor_gate_count

    gate = block(0, position[0], position[1], position[2], [], f"nor_gate{nor_gate_count}")
    gate.add_to_blocks()
    scene_connections.append(scene_connection(input1, gate.world_name))
    scene_connections.append(scene_connection(input2, gate.world_name))
    scene_connections.append(scene_connection(gate.world_name, output))
    nor_gate_count += 1



build_scene()
print(f"Took {(end_time - start_time):.2f}s")
