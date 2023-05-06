import os
import unittest
import random
import editdistance

from astar import *
from utils import *

class TestFastaFunctions(unittest.TestCase):
    def setUp(self):
        self.sequence_length = 100
        self.description = "Test sequence"
        self.file_name = "test_sequence.fasta"
        self.random_sequence = generate_random_sequence(self.sequence_length)
        save_fasta_file(self.file_name, self.description, self.random_sequence)

    def tearDown(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)

    def test_read_fasta_file(self):
        read_sequence = read_fasta_file(self.file_name)
        self.assertEqual(self.random_sequence, read_sequence)

    def test_save_fasta_file(self):
        with open(self.file_name, "r") as fasta_file:
            description_line = fasta_file.readline().strip()
            self.assertEqual(f"> {self.description}", description_line)

            sequence = ""
            for line in fasta_file:
                sequence += line.strip()
            self.assertEqual(self.random_sequence, sequence)

class TestAStar(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.A = 'ACCAGTGCCATT'
        self.B = 'ACTAGTGGCACT'
        self.target = (len(self.A), len(self.B))
        
    def test_dijkstra(self):
        g = align(self.A, self.B, h_dijkstra)
        self.assertEqual(g[self.target], editdistance.eval(self.A, self.B))

    def test_astar_with_seed_heuristic_small(self):
        k = 3
        h_seed = build_seed_heuristic(self.A, self.B, k)
        g = align(self.A, self.B, h_seed)
        self.assertEqual(g[self.target], editdistance.eval(self.A, self.B))

    def test_astar_with_seed_heuristic_big(self):
        n = 10000
        A = ''.join(random.choices('ACGT', k=n))
        B = apply_errors(A, 0.01)

        target = (len(A), len(B))
        k = math.ceil(math.log(len(A), 4))
        h_seed = build_seed_heuristic(A, B, k)
        g = align(A, B, h_seed)
        print_stats(A, B, g)

        self.assertEqual(g[target], editdistance.eval(A, B))

    #path = reconstruct_path(prev, start, end)
    #self.assertEqual(path, [(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)])

    # def test_astar_draw(self):
    #     start, end = (0, 0), (2, 2)
    #     prev, cost_so_far = astar(start, end)
    #     path = reconstruct_path(prev, start, end)
    #     draw_exploration(start, end, prev)

    # def test_euclidean_distance(self):
    #     self.assertAlmostEqual(euclidean_distance((0, 0), (3, 4)), 5.0)
    #     self.assertAlmostEqual(euclidean_distance((1, 1), (1, 1)), 0.0)

if __name__ == "__main__":
    unittest.main()
