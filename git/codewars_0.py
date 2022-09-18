from collections import deque
import time
import numpy as np


class Node:
    def __init__(self):
        self.next = None
        self.previous = None


def slow_loop_size(node):
    list = []
    while node not in list:
        list.append(node)
        print(list)
        node = node.next
    print(len(list) - list.index(node))


def fast_loop_size(node):
    np_list = np.array([])
    while node not in np_list:
        np_list = np.append(np_list, node)
        node = node.next
    print(len(np_list) - int(np.where(np_list == node)[0]))


def faster_loop_size(node):
    list = []
    while node.__hash__() not in list:
        list.append(node.__hash__())
        node = node.next
    return len(list) - list.index(node.__hash__())


nodes = [Node() for _ in range(3904)]
for node, next_node in zip(nodes, nodes[1:]):
    node.next = next_node
nodes[3903].next = nodes[1087]
node1 = Node()
node2 = Node()
node3 = Node()
node4 = Node()
node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node2
print(faster_loop_size(node1))
