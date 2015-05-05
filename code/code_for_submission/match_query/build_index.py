"""
Build Index using given settings and mappings, using bulk load to load documents
"""
from elasticsearch import Elasticsearch
import json
import time

class ESIndexBuilder(object):
    """Building Index"""
    def __init__(self,index_name,doc_type,schema_file,docs_file):
        """
	Build index using given settings and mappings, then
       	using bulk load to add documents

	@param index_name: index name in Elasticsearch
	@param doc_type: document type in Elasticsearch
	@param schema_file: file contains the schema for indexing
	@param docs_file: file contains documents which are in json format
	"""
        self.es = Elasticsearch()
        if  self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)

        self.index_name = index_name
        self.doc_type = doc_type
        self.schema = self.init_settings_mappings(schema_file)
        self.bulk_add_documents(docs_file)

    def init_settings_mappings(self,schema_file):
        """
	Create the index using given settings and mappings

	@param schema_file: file contains the schema for indexing
	"""
        with open(schema_file,'r') as f_schema:
            self.schema = json.loads(f_schema.read())
        self.es.indices.create(index = self.index_name, body = self.schema[self.index_name])

    def documents_gen(self,docs_file):
        """
	Be a Generator of actions for bulk loading documents

	@param docs_file: file contains documents which are in json format
	"""
        with open(docs_file,'r') as f_docs:
            counter = 0
            for line in f_docs:
                json_data = json.loads(line)
                yield {"index":{"_index":self.index_name,"_type":self.doc_type,"_id":counter}}
                yield json_data
                counter+=1

    def bulk_add_documents(self,docs_file):
        """
	Bulk load documents

	@param docs_file: file contains documents which are in json format
	"""
        self.es.bulk(index = self.index_name,body=self.documents_gen(docs_file))
        self.es.indices.refresh(index=self.index_name)

if __name__ == '__main__':
    es_builder = ESIndexBuilder('soccer','match','mapping_Zhihao.json','match_corpus_ratings.json')
