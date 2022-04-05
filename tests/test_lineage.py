import unittest

from tokyo_annotation.utils.lineage import parse_lineage_from_marquez


class TestLineage(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        _f = open('documentation/get_lineage', 'r')
        lineage = parse_lineage_from_marquez(_f.read())
        _f.close()
        
        self.lineage = lineage
        self.graph = lineage.graph
        self.map = self.graph.nodes.map
    
    def test_get_upstream(self):
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(lineage.get_upstream(node4), [node3])
        self.assertEqual(lineage.get_upstream(node1), [node4])
        self.assertEqual(lineage.get_upstream(node6), [node1])
        self.assertEqual(lineage.get_upstream(node2), [node6])
        self.assertEqual(lineage.get_upstream(node5), [node2])
        self.assertEqual(lineage.get_upstream(node0), [node5])
    
    def test_get_upstream_recursive(self):
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(lineage.get_upstream_recursive(node0), [node5, node2, node6, node1, node4, node3])
    
    def test_get_upstream_recursive_branches(self):
        graph = """{
    "graph": [
        {
            "id": "node0",
            "type": "DATASET",
            "inEdges": [],
            "outEdges": [
                {
                    "origin": "node0",
                    "destination": "node2"
                }
            ]
        },
        {
            "id": "node1",
            "type": "JOB",
            "inEdges": [],
            "outEdges": [
                {
                    "origin": "node1",
                    "destination": "node3"
                }
            ]
        },
        {
            "id": "node2",
            "type": "DATASET",
            "inEdges": [
                {
                    "origin": "node0",
                    "destination": "node2"
                },
                {
                    "origin": "node3",
                    "destination": "node2"
                }
            ],
            "outEdges": []
        },
        {
            "id": "node3",
            "type": "DATASET",
            "inEdges": [
                {
                    "origin": "node1",
                    "destination": "node3"
                }
            ],
            "outEdges": [
                {
                    "origin": "node3",
                    "destination": "node2"
                }
            ]
        }
    ]
}
        """
        lineage = parse_lineage_from_marquez(graph)

        graph = lineage.graph

        node0 = graph.nodes.map[0]
        node1 = graph.nodes.map[1]
        node2 = graph.nodes.map[2]
        node3 = graph.nodes.map[3]

        self.assertEqual(lineage.get_upstream_recursive(node2), [node0, node3, node1])
    
    def test_get_downstream(self):
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(lineage.get_downstream(node3), [node4])
        self.assertEqual(lineage.get_downstream(node4), [node1])
        self.assertEqual(lineage.get_downstream(node1), [node6])
        self.assertEqual(lineage.get_downstream(node6), [node2])
        self.assertEqual(lineage.get_downstream(node2), [node5])
        self.assertEqual(lineage.get_downstream(node5), [node0])
    
    def test_get_downstream_recursive(self):
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(lineage.get_downstream_recursive(node3), [node4, node1, node6, node2, node5, node0])
    
    def test_get_upstream_recursive_branches(self):
        graph = """{
    "graph": [
        {
            "id": "node0",
            "type": "DATASET",
            "inEdges": [],
            "outEdges": [
                {
                    "origin": "node0",
                    "destination": "node2"
                },
                {
                    "origin": "node0",
                    "destination": "node1"
                }
            ]
        },
        {
            "id": "node1",
            "type": "JOB",
            "inEdges": [],
            "outEdges": [
                {
                    "origin": "node1",
                    "destination": "node3"
                }
            ]
        },
        {
            "id": "node2",
            "type": "DATASET",
            "inEdges": [
                {
                    "origin": "node0",
                    "destination": "node2"
                },
                {
                    "origin": "node3",
                    "destination": "node2"
                }
            ],
            "outEdges": []
        },
        {
            "id": "node3",
            "type": "DATASET",
            "inEdges": [
                {
                    "origin": "node1",
                    "destination": "node3"
                }
            ],
            "outEdges": [
                {
                    "origin": "node3",
                    "destination": "node2"
                }
            ]
        }
    ]
}
        """

        lineage = parse_lineage_from_marquez(graph)

        graph = lineage.graph

        node0 = graph.nodes.map[0]
        node1 = graph.nodes.map[1]
        node2 = graph.nodes.map[2]
        node3 = graph.nodes.map[3]

        self.assertEqual(lineage.get_downstream_recursive(node0), [node1, node2, node3, node2])