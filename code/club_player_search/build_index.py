#Zhihao Zheng
#Building Index using given settings and mappings, using bulk load to load documents

from elasticsearch import Elasticsearch
import json
import time

class ESIndexBuilder(object):
    """Building Index"""
    def __init__(self,index_name,doc_type,schema_file,docs_file):
        """Building index using given settings and mappings, then
           using bulk load to add documents
           if del_flag, it will delete the existed index(make sure it
           exists)"""
        self.es = Elasticsearch()
        if  self.es.indices.exists(index=index_name):
            self.es.indices.delete(index=index_name)

        self.index_name = index_name
        self.doc_type = doc_type
        self.schema = self.init_settings_mappings(schema_file)
        self.bulk_add_documents(docs_file)

    def init_settings_mappings(self,schema_file):
        """create the index using given settings and mappings"""
        with open(schema_file,'r') as f_schema:
            self.schema = json.loads(f_schema.read())
        self.es.indices.create(index = self.index_name, body = self.schema[self.index_name])

    def documents_gen(self,docs_file):
        """generator of actions for bulk loading documents"""
        with open(docs_file,'r') as f_docs:
            counter = 0
            for line in f_docs:
                json_data = json.loads(line)
                yield {"index":{"_index":self.index_name,"_type":self.doc_type,"_id":counter}}
                yield json_data
                counter+=1

    def bulk_add_documents(self,docs_file):
        """bulk load documents"""
        self.es.bulk(index = self.index_name,body=self.documents_gen(docs_file))
        self.es.indices.refresh(index=self.index_name)

if __name__ == '__main__':
    es_builder = ESIndexBuilder('soccer','match','mapping_Zhihao.json','match_corpus_ratings.json')
