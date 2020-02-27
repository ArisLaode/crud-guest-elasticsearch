
import unittest
from datetime import datetime
import elasticsearch
from elasticsearch import Elasticsearch
from elasticmock import elasticmock
import json
from crud_elastic import app, ElasticData

INDEX_NAME = 'guest-book'
DOC_TYPE = 'guest'

BODY = {
    'author': 'aris',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}

UPDATED_BODY = {
    'author': 'laode',
    'text': 'Updated Text'
}

doc = {
    'nama': 'aris',
    'no handphone': '085398122436',
    'alamat': 'parigi baru',
    'timestamp': '2020, 02, 20',
}

class TestCreate(unittest.TestCase):

    @elasticmock
    def setUp(self):
        self.es = elasticsearch.Elasticsearch(hosts=[{'host': 'http://192.168.71.7', 'port': 9200}])

    def test_create_index(self):
        self.assertFalse(self.es.indices.exists(INDEX_NAME))
        self.es.indices.create(INDEX_NAME)
        self.assertTrue(self.es.indices.exists(INDEX_NAME))

    def test_insert_index(self):
        data = self.es.index(index = INDEX_NAME, doc_type=DOC_TYPE, body = doc)
        self.assertEqual(DOC_TYPE, data.get('_type'))
        self.assertTrue(data.get('created'))
        self.assertEqual(1, data.get('_version'))
        self.assertEqual(INDEX_NAME, data.get('_index'))

    def test_update_existing_doc(self):
        data = self.es.index(index=INDEX_NAME, doc_type=DOC_TYPE, body=BODY)
        document_id = data.get('_id')
        self.es.index(index=INDEX_NAME, id=document_id, doc_type=DOC_TYPE, body=UPDATED_BODY)
        target_doc = self.es.get(index=INDEX_NAME, id=document_id)

        expected = {
            '_type': DOC_TYPE,
            '_source': UPDATED_BODY,
            '_index': INDEX_NAME,
            '_version': 2,
            'found': True,
            '_id': document_id
        }

        self.assertDictEqual(expected, target_doc)

    def test_should_delete_indexed_document(self):
        doc_indexed = self.es.index(index=INDEX_NAME, doc_type=DOC_TYPE, body=BODY)
        search = self.es.search(index=INDEX_NAME)
        self.assertEqual(1, search.get('hits').get('total'))

        doc_id = doc_indexed.get('_id')
        doc_deleted = self.es.delete(index=INDEX_NAME, doc_type=DOC_TYPE, id=doc_id)
        search = self.es.search(index=INDEX_NAME)
        self.assertEqual(0, search.get('hits').get('total'))

        expected_doc_deleted = {
            'found': True,
            '_index': INDEX_NAME,
            '_type': DOC_TYPE,
            '_id': doc_id,
            '_version': 1,
        }

        self.assertDictEqual(expected_doc_deleted, doc_deleted)

    def test_should_return_hits_hits_even_when_no_result(self):
        search = self.es.search()
        self.assertEqual(0, search.get('hits').get('total'))
        self.assertListEqual([], search.get('hits').get('hits'))

    def test_should_return_all_documents(self):
        index_quantity = 10
        for i in range(0, index_quantity):
            self.es.index(index='index_{0}'.format(i), doc_type=DOC_TYPE, body={'data': 'test_{0}'.format(i)})

        search = self.es.search()
        self.assertEqual(index_quantity, search.get('hits').get('total'))

if __name__ == '__main__':
    unittest.main()