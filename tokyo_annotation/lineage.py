from typing import Type, List

from tokyo_annotation.utils import DiGraph
from tokyo_annotation.models.node import Node


class Lineage:
    def __init__(
        self,
        graph: DiGraph):
        self._graph = graph

    @property
    def graph(self):
        return self._graph

    def get_upstream_recursive(
        self,
        node: Type[Node]
    ):
        upstreams = self.get_upstream(node)

        all_upstreams = []
        all_upstreams += upstreams

        for i in upstreams:
            all_upstreams += self.get_upstream_recursive(i)
        
        return all_upstreams

    def get_upstream(
        self,
        node: Type[Node]
    ) -> List[Type[Node]]:
        index = self.graph.nodes.get_key(node)
        upstreams = self.graph.get_upstream(index)

        return upstreams

    def get_inputs(
        self,
        node: Type[Node]
    ):
        return self.get_upstream(node)

    def get_downstream_recursive(
        self,
        node: Type[Node]
    ):
        downstreams = self.get_downstream(node)

        all_downstreams = []
        all_downstreams += downstreams

        for i in downstreams:
            all_downstreams += self.get_downstream_recursive(i)
        
        return all_downstreams

    def get_downstream(
        self,
        node: Type[Node]
    ):
        index = self.graph.nodes.get_key(node)
        downstreams = self.graph.get_downstream(index)

        return downstreams

    def get_outputs(
        self,
        node: Type[Node]
    ):
        return self.get_downstream(node)