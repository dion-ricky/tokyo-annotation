from platform import node
import unittest

from tokyo_annotation.utils import LinkedList, Node, Map, DiGraph

class TestUtils(unittest.TestCase):
    def test_node_data(self):
        node1 = Node()
        node2 = Node("String data")
        node3 = Node(100)
        node4 = Node(node3)

        self.assertEqual(node1.data, None)
        self.assertEqual(node2.data, "String data")
        self.assertEqual(node3.data, 100)
        self.assertEqual(node4.data, node3)
    
    def test_node_link(self):
        node1 = Node()
        node2 = Node("String data")
        node3 = Node(100)
        node4 = Node(node3)

        node1.next = node2
        
        node2.prev = node1
        node2.next = node3

        node3.prev = node2
        node3.next = node4

        node4.prev = node3

        self.assertEqual(node1.prev, None)
        self.assertEqual(node2.prev, node1)
        self.assertEqual(node2.next, node3)
        self.assertEqual(node3.prev, node2)
        self.assertEqual(node3.next, node4)
        self.assertEqual(node4.prev, node3)
        self.assertEqual(node4.next, None)
    
    def test_ll_init(self):
        ll1 = LinkedList()
        
        node1 = Node()
        ll2 = LinkedList(node1)

        self.assertEqual(ll1.count, 0)
        self.assertEqual(ll2.count, 1)

        node2 = Node("String data")
        node3 = Node(100)
        node4 = Node(node3)

        node1.next = node2
        node2.prev = node1
        node2.next = node3
        node3.prev = node2
        node3.next = node4
        node4.prev = node3

        ll3 = LinkedList(node1)
        self.assertEqual(ll3.count, 4)

    def test_ll_get_tail(self):
        node1 = Node()
        node2 = Node("String data")
        node3 = Node(100)
        node4 = Node(node3)

        node1.next = node2
        
        node2.prev = node1
        node2.next = node3

        node3.prev = node2
        node3.next = node4

        node4.prev = node3

        ll1 = LinkedList(node1)

        self.assertEqual(ll1.get_tail(), node4)

    def test_ll_append(self):
        ll1 = LinkedList()
        node1 = Node()

        ll1.append(node1)

        self.assertEqual(ll1.count, 1)
        self.assertEqual(ll1.head, node1)

        node2 = Node("Test data")
        ll1.append(node2)

        self.assertEqual(ll1.count, 2)
        self.assertEqual(ll1.head.next, node2)
    
    def test_ll_set_next(self):
        node1 = Node()
        node2 = Node("String data")
        node3 = Node(100)
        node4 = Node(node3)

        node1.next = node2
        
        node2.prev = node1
        node2.next = node3

        node3.prev = node2
        node3.next = node4

        node4.prev = node3

        ll1 = LinkedList(node1)

        node5 = Node()

        ll1.set_next(node2, node5)

        self.assertEqual(node2.next, node5)
        self.assertEqual(node5.prev, node2)
        self.assertEqual(node5.next, node3)
        self.assertEqual(node3.prev, node5)
        self.assertEqual(ll1.count, 5)
    
    def test_map_init(self):
        map1 = Map()

        self.assertEqual(len(map1.map), 0)
    
    def test_map_insert(self):
        map1 = Map()

        ins1 = map1.insert(None)
        ins2 = map1.insert("Test value")

        self.assertEqual(len(map1.map), 2)
        self.assertEqual(ins1, 0)
        self.assertEqual(ins2, 1)
    
    def test_map_remove(self):
        map1 = Map()

        ins1 = map1.insert(None)
        ins2 = map1.insert("Test value")

        removed = map1.remove(0)

        self.assertEqual(len(map1.map), 1)
        self.assertEqual(removed, None)
    
    def test_map_get_key(self):
        map1 = Map()

        ins1 = map1.insert(None)
        ins2 = map1.insert("Test value")

        self.assertEqual(map1.get_key("Test value"), 1)
    
    def test_map_insert_remove(self):
        map1 = Map()

        ins1 = map1.insert(None)
        ins2 = map1.insert("Test value")

        removed = map1.remove(0)
        
        ins3 = map1.insert("Test value 2")

        self.assertEqual(len(map1.map), 2)
        self.assertEqual(ins3, 2)
    
    def test_diagraph_init(self):
        map1 = Map() # empty map
        map2 = Map() # has 2 nodes

        map2.insert("Test value 1")
        map2.insert("Test value 2")

        digraph1 = DiGraph(map1)
        digraph2 = DiGraph(map2)

        self.assertEqual(digraph1.nodes, map1)
        self.assertEqual(digraph2.nodes, map2)

        self.assertEqual(digraph1.dimension, 0)
        self.assertEqual(digraph2.dimension, 2)

        self.assertEqual(digraph1.edges, [])
        self.assertEqual(digraph2.edges, [0, 0, 0, 0])
    
    def test_digraph_index(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")

        digraph1 = DiGraph(map1)

        self.assertEqual(digraph1.get_index(0, 0), 0)
        self.assertEqual(digraph1.get_index(0, 1), 1)
        self.assertEqual(digraph1.get_index(1, 0), 2)
        self.assertEqual(digraph1.get_index(1, 1), 3)
        
        self.assertEqual(digraph1.get_index(0, 0, digraph1.dimension), 0)
        self.assertEqual(digraph1.get_index(0, 1, digraph1.dimension), 1)
        self.assertEqual(digraph1.get_index(1, 0, digraph1.dimension), 2)
        self.assertEqual(digraph1.get_index(1, 1, digraph1.dimension), 3)
    
    def test_digraph_set_edge(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")

        digraph1 = DiGraph(map1)

        digraph1.set_edge(0, 1, True)

        self.assertEqual(digraph1.edges[digraph1.get_index(0, 1)], True)

        digraph1.set_edge(1, 0, True, digraph1.edges)

        self.assertEqual(digraph1.edges[digraph1.get_index(1, 0)], True)
    
    def test_digraph_edge(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")

        digraph1 = DiGraph(map1)

        digraph1.set_edge(0, 1, True)
        digraph1.set_edge(1, 0, True)

        self.assertTrue(digraph1.edge(0, 1))
        self.assertTrue(digraph1.edge(1, 0))

    def test_digraph_add_node(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")

        digraph1 = DiGraph(map1)
        digraph1.set_edge(0, 1, True)

        digraph1.add("Test value 3")

        self.assertEqual(map1.counter, 3)
        self.assertEqual(digraph1.nodes, map1)
        self.assertEqual(digraph1.dimension, 3)
        self.assertEqual(digraph1.edges, [0, 1, 0, 0, 0, 0, 0, 0, 0])
    
    def test_digraph_remove(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")
        map1.insert("Test value 3")

        digraph1 = DiGraph(map1)
        digraph1.set_edge(0, 1, True)
        digraph1.set_edge(0, 2, True)

        digraph1.remove(0)

        self.assertEqual(digraph1.dimension, 3)
        self.assertEqual(digraph1.edges, [0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    def test_digraph_downstream_index(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")
        map1.insert("Test value 3")

        digraph1 = DiGraph(map1)
        digraph1.set_edge(0, 1, True)

        self.assertEqual(digraph1.get_downstream_index(0), [1])
        self.assertEqual(digraph1.get_downstream_index(1), [])
    
    def test_digraph_downstream(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")
        map1.insert("Test value 3")

        digraph1 = DiGraph(map1)
        digraph1.set_edge(0, 1, True)

        self.assertEqual(digraph1.get_downstream(0), ["Test value 2"])
        self.assertEqual(digraph1.get_downstream(1), [])
    
    def test_digraph_upstream_index(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")
        map1.insert("Test value 3")

        digraph1 = DiGraph(map1)
        digraph1.set_edge(0, 1, True)

        self.assertEqual(digraph1.get_upstream_index(0), [])
        self.assertEqual(digraph1.get_upstream_index(1), [0])
    
    def test_digraph_upstream(self):
        map1 = Map()

        map1.insert("Test value 1")
        map1.insert("Test value 2")
        map1.insert("Test value 3")

        digraph1 = DiGraph(map1)
        digraph1.set_edge(0, 1, True)

        self.assertEqual(digraph1.get_upstream(0), [])
        self.assertEqual(digraph1.get_upstream(1), ["Test value 1"])
    
    def test_digraph_complex(self):
        map1 = Map()
        
        map1.insert("A")
        map1.insert("B")
        map1.insert("C")
        map1.insert("D")

        digraph1 = DiGraph(map1)

        digraph1.set_edge(0, 1, 1)
        digraph1.set_edge(0, 2, 1)

        digraph1.set_edge(1, 3, 1)
        digraph1.set_edge(2, 3, 1)

        self.assertEqual(digraph1.get_downstream_index(0), [1, 2])
        self.assertEqual(digraph1.get_downstream_index(1), [3])
        self.assertEqual(digraph1.get_downstream_index(2), [3])

        self.assertEqual(digraph1.get_upstream_index(1), [0])
        self.assertEqual(digraph1.get_upstream_index(2), [0])
        self.assertEqual(digraph1.get_upstream_index(3), [1, 2])

        digraph1.add("E")
        digraph1.add("F")

        self.assertEqual(digraph1.get_downstream_index(0), [1, 2])
        self.assertEqual(digraph1.get_downstream_index(1), [3])
        self.assertEqual(digraph1.get_downstream_index(2), [3])

        self.assertEqual(digraph1.get_upstream_index(1), [0])
        self.assertEqual(digraph1.get_upstream_index(2), [0])
        self.assertEqual(digraph1.get_upstream_index(3), [1, 2])

        digraph1.set_edge(3, 4, 1)
        digraph1.set_edge(4, 5, 1)

        self.assertEqual(digraph1.get_downstream_index(3), [4])
        self.assertEqual(digraph1.get_downstream_index(4), [5])

        self.assertEqual(digraph1.nodes, map1)
        self.assertEqual(digraph1.dimension, 6)

        self.assertEqual(digraph1.get_downstream(0), ["B", "C"])
        self.assertEqual(digraph1.get_downstream(1), ["D"])
        self.assertEqual(digraph1.get_downstream(2), ["D"])
        
        self.assertEqual(digraph1.get_upstream(3), ["B", "C"])
        self.assertEqual(digraph1.get_upstream(4), ["D"])
        self.assertEqual(digraph1.get_upstream(5), ["E"])