import random
from typing import List, Tuple, Dict
from collections import Counter
import itertools
import matplotlib.pyplot as plt
from sympy.combinatorics import Permutation
from sympy.ntheory import factorint
import math

class CubiePiece:
    def __init__(self, position: int, orientation: int):
        self.position = position
        self.orientation = orientation

class RubiksCube:
    def __init__(self):
        self.corners = [CubiePiece(i, 0) for i in range(8)]
        self.edges = [CubiePiece(i, 0) for i in range(12)]

    def apply_move(self, move: str):
        corner_cycles = {
            'U': [(0, 1, 2, 3)], 'D': [(4, 7, 6, 5)],
            'F': [(0, 3, 5, 4)], 'B': [(1, 7, 6, 2)],
            'L': [(0, 4, 7, 1)], 'R': [(2, 6, 5, 3)]
        }
        edge_cycles = {
            'U': [(0, 1, 2, 3)], 'D': [(8, 11, 10, 9)],
            'F': [(0, 4, 8, 7)], 'B': [(2, 6, 10, 5)],
            'L': [(3, 7, 11, 4)], 'R': [(1, 5, 9, 6)]
        }
        corner_rotations = {
            'U': [(0, 0, 0, 0)], 'D': [(0, 0, 0, 0)],
            'F': [(1, 2, 1, 2)], 'B': [(1, 2, 1, 2)],
            'L': [(2, 1, 2, 1)], 'R': [(2, 1, 2, 1)]
        }
        edge_flips = {
            'U': [(0, 0, 0, 0)], 'D': [(0, 0, 0, 0)],
            'F': [(1, 1, 1, 1)], 'B': [(1, 1, 1, 1)],
            'L': [(1, 1, 1, 1)], 'R': [(1, 1, 1, 1)]
        }

        face = move[0]
        double_move = len(move) > 1 and move[1] == '2'
        inverse_move = len(move) > 1 and move[1] == "'"

        cycles = 2 if double_move else (3 if inverse_move else 1)
        
        for _ in range(cycles):
            for cycle in corner_cycles[face]:
                self._cycle_pieces(self.corners, cycle)
            for cycle in edge_cycles[face]:
                self._cycle_pieces(self.edges, cycle)
            for cycle, rotations in zip(corner_cycles[face], corner_rotations[face]):
                self._rotate_corners(cycle, rotations)
            for cycle, flips in zip(edge_cycles[face], edge_flips[face]):
                self._flip_edges(cycle, flips)

    def _cycle_pieces(self, pieces: List[CubiePiece], cycle: Tuple[int, ...]):
        temp = pieces[cycle[-1]].position
        for i in reversed(range(1, len(cycle))):
            pieces[cycle[i]].position = pieces[cycle[i-1]].position
        pieces[cycle[0]].position = temp

    def _rotate_corners(self, cycle: Tuple[int, ...], rotations: Tuple[int, ...]):
        for i, rot in zip(cycle, rotations):
            self.corners[i].orientation = (self.corners[i].orientation + rot) % 3

    def _flip_edges(self, cycle: Tuple[int, ...], flips: Tuple[int, ...]):
        for i, flip in zip(cycle, flips):
            self.edges[i].orientation = (self.edges[i].orientation + flip) % 2

    def scramble(self, moves: int):
        possible_moves = ['U', 'D', 'F', 'B', 'L', 'R',
                          'U2', 'D2', 'F2', 'B2', 'L2', 'R2',
                          "U'", "D'", "F'", "B'", "L'", "R'"]
        for _ in range(moves):
            self.apply_move(random.choice(possible_moves))

    def is_solved(self) -> bool:
        return all(piece.position == i and piece.orientation == 0 
                   for i, piece in enumerate(self.corners + self.edges))

    def get_state(self) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        corner_state = tuple((piece.position, piece.orientation) for piece in self.corners)
        edge_state = tuple((piece.position, piece.orientation) for piece in self.edges)
        return (corner_state, edge_state)

    def set_state(self, state: Tuple[Tuple[int, ...], Tuple[int, ...]]):
        corner_state, edge_state = state
        for i, (pos, ori) in enumerate(corner_state):
            self.corners[i].position = pos
            self.corners[i].orientation = ori
        for i, (pos, ori) in enumerate(edge_state):
            self.edges[i].position = pos
            self.edges[i].orientation = ori

    def get_permutation(self) -> Tuple[List[int], List[int]]:
        corner_perm = [piece.position for piece in self.corners]
        edge_perm = [piece.position for piece in self.edges]
        return (corner_perm, edge_perm)

def detect_cycles(perm: List[int]) -> List[List[int]]:
    cycles = []
    visited = set()
    for start in range(len(perm)):
        if start not in visited:
            cycle = []
            current = start
            while current not in visited:
                visited.add(current)
                cycle.append(current)
                current = perm[current]
            if len(cycle) > 1:
                cycles.append(cycle)
    return cycles

def calculate_order(perm: List[int]) -> int:
    cycles = detect_cycles(perm)
    if not cycles:
        return 1
    return math.lcm(*[len(cycle) for cycle in cycles])


def analyze_group_properties(trials: int, scramble_moves: int):
    cube = RubiksCube()
    permutation_orders = []
    corner_cycle_types = []
    edge_cycle_types = []
    corner_orientation_sums = []
    edge_orientation_sums = []

    for _ in range(trials):
        cube.scramble(scramble_moves)
        corner_perm, edge_perm = cube.get_permutation()

        corner_cycles = detect_cycles(corner_perm)
        edge_cycles = detect_cycles(edge_perm)

        full_perm = corner_perm + edge_perm
        permutation_orders.append(calculate_order(full_perm))
        
        corner_cycle_type = tuple(sorted([len(cycle) for cycle in corner_cycles], reverse=True))
        edge_cycle_type = tuple(sorted([len(cycle) for cycle in edge_cycles], reverse=True))
        
        corner_cycle_types.append(corner_cycle_type)
        edge_cycle_types.append(edge_cycle_type)
        
        corner_orientation_sum = sum(corner.orientation for corner in cube.corners) % 3
        edge_orientation_sum = sum(edge.orientation for edge in cube.edges) % 2
        corner_orientation_sums.append(corner_orientation_sum)
        edge_orientation_sums.append(edge_orientation_sum)

    print(f"\nAnalysis of {trials} trials with {scramble_moves} moves each:")
    
    print("\nPermutation Order Distribution:")
    order_counter = Counter(permutation_orders)
    for order, count in order_counter.most_common(10):
        print(f"Order {order}: {count} times ({count/trials:.2%})")
    
    print("\nCorner Cycle Type Distribution:")
    corner_cycle_counter = Counter(corner_cycle_types)
    for cycle_type, count in corner_cycle_counter.most_common(10):
        print(f"{cycle_type}: {count} times ({count/trials:.2%})")
    
    print("\nEdge Cycle Type Distribution:")
    edge_cycle_counter = Counter(edge_cycle_types)
    for cycle_type, count in edge_cycle_counter.most_common(10):
        print(f"{cycle_type}: {count} times ({count/trials:.2%})")
    
    print("\nCorner Orientation Sum Distribution:")
    corner_ori_counter = Counter(corner_orientation_sums)
    for sum_value, count in corner_ori_counter.most_common():
        print(f"{sum_value}: {count} times ({count/trials:.2%})")
    
    print("\nEdge Orientation Sum Distribution:")
    edge_ori_counter = Counter(edge_orientation_sums)
    for sum_value, count in edge_ori_counter.most_common():
        print(f"{sum_value}: {count} times ({count/trials:.2%})")

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.bar(order_counter.keys(), order_counter.values())
    plt.title("Distribution of Permutation Orders")
    plt.xlabel("Order")
    plt.ylabel("Frequency")
    plt.savefig("permutation_orders.png")
    plt.close()

def analyze_subgroup_structure():
    cube = RubiksCube()
    move_generators = ['U', 'D', 'F', 'B', 'L', 'R']
    subgroups = []

    for r in range(1, len(move_generators) + 1):
        for subset in itertools.combinations(move_generators, r):
            subgroup = set()
            to_process = [cube.get_state()]
            while to_process:
                state = to_process.pop()
                if state in subgroup:
                    continue
                subgroup.add(state)
                cube.set_state(state)
                for move in subset:
                    cube.apply_move(move)
                    new_state = cube.get_state()
                    if new_state not in subgroup:
                        to_process.append(new_state)
            subgroups.append((subset, len(subgroup)))

    print("\nSubgroup Analysis:")
    for generators, order in sorted(subgroups, key=lambda x: x[1]):
        print(f"Generators: {generators}, Order: {order}")
        if order > 1:
            factors = factorint(order)
            print(f"  Prime factorization: {factors}")

if __name__ == "__main__":
    analyze_group_properties(10000, 20)
    analyze_subgroup_structure()