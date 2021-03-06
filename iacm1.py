# -*- coding: utf-8 -*-
"""

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IBQarC4sKFpDgMqscunmi7CC8UUYzRN3
"""
import cmath

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from collections import Counter

NUMBER_OF_NODES = 8192
ALPHA = -1.50

def find_neighbour(graph, prev_fitness):
  total = sum(dict(graph.degree).values())

  fitness = lambda node:  graph.degree[node] / total
  fitness_coefficient = lambda node: (fitness(node) - prev_fitness.get(node, 1))  ** ALPHA

  probabilities = {node: fitness_coefficient(node) for node in graph.nodes}
  neighbour = sorted(probabilities, key=lambda node: cmath.phase(probabilities[node]), reverse=True)[0]
    
  return neighbour, probabilities

def build_degree_frequency_plot(degree_sequence):
  degreeCount = Counter(degree_sequence)
  deg, cnt = zip(*degreeCount.items())
  fig, ax = plt.subplots()
  plt.loglog(np.log1p(deg[::-1]), cnt[::-1], 'b-', marker='o')

  plt.title("Degree Plot")
  plt.ylabel("Count")
  plt.xlabel("Degree")

  plt.show()


def build_degree_rank_plot(degree_sequence):
  plt.loglog(np.log1p(degree_sequence), 'b-', marker='o')

  plt.title("Degree rank plot")
  plt.ylabel("degree")
  plt.xlabel("rank")

  plt.show()

def main():

  # initial graph
  graph = nx.Graph([(0, 1)])
  fitness_coef = dict(graph.degree)

  for new_node in range(graph.size()+1, NUMBER_OF_NODES+1):
    node_neighbour, fitness_coef = find_neighbour(graph, fitness_coef)
  
    graph.add_node(new_node)
    graph.add_edge(new_node, node_neighbour)

  degree_sequence = sorted(dict(graph.degree()).values(), reverse=True)
  build_degree_frequency_plot(degree_sequence)
  build_degree_rank_plot(degree_sequence)

  # build graph
  plt.figure(figsize=(20,20))
  nx.draw(graph, pos=nx.kamada_kawai_layout(graph)) 
  plt.show()


if __name__ == '__main__':
  main()