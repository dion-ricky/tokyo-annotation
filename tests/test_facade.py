import unittest

from tokyo_annotation import Annotation


class TestFacade(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

        self.MARQUEZ_IP = 'localhost'
        self.MARQUEZ_PORT = '5000'
        self.MARQUEZ_URL = f'http://{self.MARQUEZ_IP}:{self.MARQUEZ_PORT}'

    def test_init_from_url(self):
        annot = Annotation.from_openlineage_url(
            namespace='bigquery',
            dataset_name='source.actor',
            openlineage_url=self.MARQUEZ_URL)
        
        self.assertEqual(annot.node_id, 'dataset:bigquery:source.actor')
        self.assertEqual(annot.node.id, 'dataset:bigquery:source.actor')
        self.assertEqual(annot.node.meta['namespace'], 'bigquery')
        self.assertEqual(annot.node.meta['name'], 'source.actor')
    
    def test_annotation(self):
        annot = Annotation.from_openlineage_url(
            namespace='bigquery',
            dataset_name='source.address',
            openlineage_url=self.MARQUEZ_URL)
        
        print(annot.get())