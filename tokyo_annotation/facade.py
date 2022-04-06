import attr
from typing import Any, Optional

from openlineage.client import OpenLineageClientOptions

from tokyo_annotation.lineage import Lineage
from tokyo_annotation.models.node import Node
from tokyo_annotation.adapter import OpenLineageClientFacade
from tokyo_annotation.utils.lineage import parse_raw_lineage

@attr.s
class AnnotatedNode:
    node: Node = attr.ib(default=None)
    annotation: Any = attr.ib(default=None)


ENDPOINT = "lineage"


class Facade:
    def __init__(
        self,
        dataset_id: str,
        openlineage_adapter: OpenLineageClientFacade
    ) -> None:
        self.dataset_id = dataset_id
        self.openlineage_adapter = openlineage_adapter

        raw_lineage = Facade.get_raw_lineage(dataset_id, openlineage_adapter)
        self.lineage: Lineage = parse_raw_lineage(raw_lineage)

        for node in self.lineage.graph.nodes.map:
            if node.id == dataset_id:
                self.node = AnnotatedNode(node=node)

    def get_annotation(self):
        pass

    def _get_annotation_recursive(self, node: AnnotatedNode):
        if node.annotation:
            return node.annotation
        else:
            annotations = []
            upstream = self.lineage.get_upstream(node.node)
            
            for node in upstream:
                annotations += self._get_annotation_recursive(AnnotatedNode(node))
            
            # union the annotations
            return annotations

    def get(self):
        return self.get_annotation()

    @classmethod
    def from_openlineage_url(
        cls,
        dataset_id: str,
        openlineage_url: str,
        openlineage_client_options: Optional[OpenLineageClientOptions] = None
    ):
        openlineage_adapter = OpenLineageClientFacade.from_url(
                                openlineage_url, openlineage_client_options)
        
        return cls(openlineage_adapter, dataset_id)
    
    @staticmethod
    def get_raw_lineage(
        dataset_id,
        openlineage_adapter
    ):
        adapter = openlineage_adapter

        raw_lineage = adapter.get(
            path=ENDPOINT,
            params={
            "nodeId": dataset_id
        })

        return raw_lineage