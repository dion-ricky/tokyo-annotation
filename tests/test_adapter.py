import unittest

from openlineage.client import OpenLineageClient, OpenLineageClientOptions
from tokyo_annotation.adapter import openlineage_client_facade

from tokyo_annotation.adapter.openlineage_client_facade import OpenLineageClientFacade


class TestAdapter(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.url = 'http://localhost:5000'

    def test_init(self):
        marquez_url = self.url
        openlineage_client_options = OpenLineageClientOptions()

        openlineage_client = OpenLineageClient(marquez_url, openlineage_client_options)

        adapter = OpenLineageClientFacade(openlineage_client)

        self.assertIsInstance(adapter, OpenLineageClientFacade)
        self.assertEqual(adapter.url, marquez_url)
        self.assertEqual(adapter.options, openlineage_client_options)
    
    def test_from_url(self):
        marquez_url = self.url
        openlineage_client_options = OpenLineageClientOptions()

        adapter = OpenLineageClientFacade.from_url(marquez_url, openlineage_client_options)

        self.assertIsInstance(adapter, OpenLineageClientFacade)
        self.assertEqual(adapter.url, marquez_url)
        self.assertEqual(adapter.options, openlineage_client_options)

        adapter = OpenLineageClientFacade.from_url(marquez_url)

        self.assertIsInstance(adapter, OpenLineageClientFacade)
        self.assertEqual(adapter.url, marquez_url)
        self.assertEqual(adapter.options, OpenLineageClientOptions())