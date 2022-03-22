from typing import Type

from tokyo_annotation.utils import DiGraph
from tokyo_annotation.models.lineage import Node


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
        pass

    def get_upstream(
        self,
        node: Type[Node]
    ):
        pass

    def get_inputs(
        self,
        node: Type[Node]
    ):
        pass

    def get_downstream_recursive(
        self,
        node: Type[Node]
    ):
        pass

    def get_downstream(
        self,
        node: Type[Node]
    ):
        pass

    def get_outputs(
        self,
        node: Type[Node]
    ):
        pass