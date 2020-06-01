import pytest
import random
from storage.storage import MilvusIns


class TestStorageMilvus:
    """ test class for milvus"""
    name = "pytest_collection_name"
    dimension = 512
    index_file_size = 1024
    metric_type = "l2"

    def test_new_collection(self):
        """create new collection"""
        rv = MilvusIns.new_milvus_collection(self.name, self.dimension, self.index_file_size, self.metric_type)
        assert rv == None

    def test_insert_vectors(self):
        """test insert vectors"""
        vectors = [[random.random() for _ in range(self.dimension)] for _ in range(20)]
        rv = MilvusIns.insert_vectors(self.name, vectors)
        assert len(rv) == 20

    def test_search_vectors(self):
        """test search vectors"""
        q_records = [[random.random() for _ in range(self.dimension)]]
        rv = MilvusIns.search_vectors(self.name, q_records, 10, 16)

    def test_del_milvus_collection(self):
        """drop collection"""
        rv = MilvusIns.del_milvus_collection(self.name)
        assert rv == None
