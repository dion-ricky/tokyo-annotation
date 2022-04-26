import attr
from typing import Any, Optional

from openlineage.client import OpenLineageClientOptions

from tokyo_annotation.models.node import Node
from tokyo_annotation.adapter import OpenLineageClientFacade
from tokyo_annotation.utils.lineage import (
    Lineage,
    parse_raw_lineage,
    get_genesis_datasets
)

@attr.s
class AnnotatedNode:
    node: Node = attr.ib(default=None)
    annotation: Any = attr.ib(default=None)


ENDPOINT = "lineage"


class Facade:
    def __init__(
        self,
        dataset_id: str,
        openlineage_client: OpenLineageClientFacade
    ) -> None:
        self.dataset_id = dataset_id
        self.openlineage_client = openlineage_client

        raw_lineage = Facade.get_raw_lineage(dataset_id, openlineage_client)
        self.lineage: Lineage = parse_raw_lineage(raw_lineage)
        self.node = None

        for node in self.lineage.graph.nodes.map:
            if node.id == dataset_id:
                self.node = node

    def get_annotation(self):
        pass

    def get(self):
        return self.get_annotation()

    @classmethod
    def from_openlineage_url(
        cls,
        dataset_id: str,
        openlineage_url: str,
        openlineage_client_options: Optional[OpenLineageClientOptions] = None
    ):
        openlineage_client = OpenLineageClientFacade.from_url(
                                openlineage_url, openlineage_client_options)
        
        return cls(dataset_id, openlineage_client)
    
    @staticmethod
    def get_raw_lineage(
        dataset_id,
        openlineage_client
    ):
        adapter = openlineage_client

        raw_lineage = adapter.get(
            path=ENDPOINT,
            params={
            "nodeId": dataset_id
        })

        return raw_lineage
    
    def _get_genesis_datasets(self):
        if not self.node:
            return
        
        return get_genesis_datasets(self.node, self.lineage)