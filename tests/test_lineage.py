import unittest

from tokyo_annotation.utils.lineage import (
    get_genesis_datasets,
    parse_raw_lineage,
    get_upstream,
    get_upstream_recursive,
    get_downstream,
    get_downstream_recursive
)


class TestLineage(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        _f = open('documentation/get_lineage', 'r')
        lineage = parse_raw_lineage(_f.read())
        _f.close()
        
        self.lineage = lineage
        self.graph = lineage.graph
        self.map = self.graph.nodes.map
    
    def test_get_upstream(self):
        # 3 -> 4 -> 1 -> 6 -> 2 -> 5 -> 0
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(get_upstream(node4, lineage), [node3])
        self.assertEqual(get_upstream(node1, lineage), [node4])
        self.assertEqual(get_upstream(node6, lineage), [node1])
        self.assertEqual(get_upstream(node2, lineage), [node6])
        self.assertEqual(get_upstream(node5, lineage), [node2])
        self.assertEqual(get_upstream(node0, lineage), [node5])

    def test_empty_upstream(self):
        graph = """{
    "graph": [
        {
            "id": "node0",
            "type": "DATASET",
            "inEdges": [],
            "outEdges": []
        }
    ]
}"""
        lineage = parse_raw_lineage(graph)

        graph = lineage.graph

        node0 = graph.nodes.map[0]

        self.assertEqual(get_upstream(node0, lineage), [])

    def test_get_upstream_recursive(self):
        # 3 -> 4 -> 1 -> 6 -> 2 -> 5 -> 0
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(get_upstream_recursive(node0, lineage), [node5, node2, node6, node1, node4, node3])
    
    def test_get_upstream_recursive_branches(self):
        # 0 -> 2
        # 1 -> 3 -> 2
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
        lineage = parse_raw_lineage(graph)

        graph = lineage.graph

        node0 = graph.nodes.map[0]
        node1 = graph.nodes.map[1]
        node2 = graph.nodes.map[2]
        node3 = graph.nodes.map[3]

        self.assertEqual(get_upstream_recursive(node2, lineage), [node0, node3, node1])
    
    def test_get_downstream(self):
        # 3 -> 4 -> 1 -> 6 -> 2 -> 5 -> 0
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(get_downstream(node3, lineage), [node4])
        self.assertEqual(get_downstream(node4, lineage), [node1])
        self.assertEqual(get_downstream(node1, lineage), [node6])
        self.assertEqual(get_downstream(node6, lineage), [node2])
        self.assertEqual(get_downstream(node2, lineage), [node5])
        self.assertEqual(get_downstream(node5, lineage), [node0])
    
    def test_get_downstream_recursive(self):
        # 3 -> 4 -> 1 -> 6 -> 2 -> 5 -> 0
        lineage = self.lineage

        node0 = self.map[0]
        node1 = self.map[1]
        node2 = self.map[2]
        node3 = self.map[3]
        node4 = self.map[4]
        node5 = self.map[5]
        node6 = self.map[6]

        self.assertEqual(get_downstream_recursive(node3, lineage), [node4, node1, node6, node2, node5, node0])
    
    def test_get_downstream_recursive_branches(self):
        # 0 -> 2
        # 0 -> 1 -> 3 -> 2
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
            "inEdges": [
                {
                    "origin": "node0",
                    "destination": "node1"
                }
            ],
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

        lineage = parse_raw_lineage(graph)

        graph = lineage.graph

        node0 = graph.nodes.map[0]
        node1 = graph.nodes.map[1]
        node2 = graph.nodes.map[2]
        node3 = graph.nodes.map[3]

        self.assertEqual(get_downstream_recursive(node0, lineage), [node1, node2, node3, node2])
    
    def test_genesis_ds_single(self):
        # 0 -> 1 -> 2 -> 3 -> 4
        graph = """{
    "graph": [
        {
            "id": "node0",
            "type": "DATASET",
            "inEdges": [],
            "outEdges": [
                {
                    "origin": "node0",
                    "destination": "node1"
                }
            ]
        },
        {
            "id": "node1",
            "type": "JOB",
            "inEdges": [
                {
                    "origin": "node0",
                    "destination": "node1"
                }
            ],
            "outEdges": [
                {
                    "origin": "node1",
                    "destination": "node2"
                }
            ]
        },
        {
            "id": "node2",
            "type": "DATASET",
            "inEdges": [
                {
                    "origin": "node1",
                    "destination": "node2"
                }
            ],
            "outEdges": [
                {
                    "origin": "node2",
                    "destination": "node3"
                }
            ]
        },
        {
            "id": "node3",
            "type": "JOB",
            "inEdges": [
                {
                    "origin": "node2",
                    "destination": "node3"
                }
            ],
            "outEdges": [
                {
                    "origin": "node3",
                    "destination": "node4"
                }
            ]
        },
        {
            "id": "node4",
            "type": "DATASET",
            "inEdges": [
                {
                    "origin": "node3",
                    "destination": "node4"
                }
            ],
            "outEdges": []
        }
    ]
}"""

        lineage = parse_raw_lineage(graph)

        graph = lineage.graph

        node0 = graph.nodes.map[0]
        node1 = graph.nodes.map[1]
        node2 = graph.nodes.map[2]
        node3 = graph.nodes.map[3]
        node4 = graph.nodes.map[4]

        self.assertEqual(get_genesis_datasets(node0, lineage), [])
        self.assertEqual(get_genesis_datasets(node1, lineage), [node0])
        self.assertEqual(get_genesis_datasets(node2, lineage), [node0])
        self.assertEqual(get_genesis_datasets(node3, lineage), [node0])
        self.assertEqual(get_genesis_datasets(node4, lineage), [node0])
    
    def test_genesis_ds_multiple(self):
        # 0 -> 2 -> 3
        # 1 -> 2
        # 4 -> 3
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
            "type": "DATASET",
            "inEdges": [],
            "outEdges": [
                {
                    "origin": "node1",
                    "destination": "node2"
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
                    "origin": "node1",
                    "destination": "node2"
                }
            ],
            "outEdges": [
                {
                    "origin": "node2",
                    "destination": "node3"
                }
            ]
        },
        {
            "id": "node3",
            "type": "DATASET",
            "inEdges": [
                {
                    "origin": "node2",
                    "destination": "node3"
                }
            ],
            "outEdges": []
        },
        {
            "id": "node4",
            "type": "DATASET",
            "inEdges": [],
            "outEdges": [
                {
                    "origin": "node4",
                    "destination": "node3"
                }
            ]
        }
    ]
}"""
        lineage = parse_raw_lineage(graph)

        graph = lineage.graph

        node0 = graph.nodes.map[0]
        node1 = graph.nodes.map[1]
        node2 = graph.nodes.map[2]
        node3 = graph.nodes.map[3]
        node4 = graph.nodes.map[4]

        self.assertEqual(get_genesis_datasets(node0, lineage), [])
        self.assertEqual(get_genesis_datasets(node1, lineage), [])
        self.assertEqual(get_genesis_datasets(node2, lineage), [node0, node1])
        self.assertEqual(get_genesis_datasets(node3, lineage), [node4, node0, node1])
        self.assertEqual(get_genesis_datasets(node4, lineage), [])