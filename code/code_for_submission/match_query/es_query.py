#Zhihao Zheng
#provide methods for various queries
from elasticsearch import Elasticsearch
import json

class ESQuery:
    """Class which provide methods for various queries"""
    def __init__(self,index_name='i_novels'):
        """Queries for the give index name"""
        self.index_name = index_name
        self.es = Elasticsearch()

    def q_total(self):
        """count for the total documents in the index"""
        res = self.es.search(index=self.index_name,
                             body={'query':{'match_all':{}}})
        return res['hits']['total']

    def q_range(self,year1,year2):
        """count the total documents range from year1 to year2"""
        query = {
                    'query': {
                        'range': {
                            'date': {
                                'gte': year1,
                                'lte': year2
                            }
                        }
                    }
                }

        res = self.es.search(index=self.index_name,
                             body=query)
        return res['hits']['total']

    def q_field(self,field_name):
        """count the total unique value of the give field"""
        query = {
                    'query': {
                        'match_all':{} 
                    },
                    'aggs': {
                        'q_field': {
                            'cardinality':{'field': field_name}
                        }
                    }
                }

        res = self.es.search(index=self.index_name,
                             body=query,search_type = 'count')
        return res['aggregations']['q_field']['value']

    def show_highlight_result(self,res,fields = ['title','text']):
        """show the highlighted result of given fields"""
        print "total hits:", res['hits']['total']
        counter = 1
        for hit in res['hits']['hits']:
            if (counter == 11): break
            print "Rank:",counter
            print "Title:",hit['_source']['title']
            print '---------------------------------------------'
            counter += 1
            for field in fields:
                if (field in hit['highlight']):
                    print 'Field: ', field
                    print '---------------------------------------------'
                    for content in hit['highlight'][field]:
                        print content
                        print '---------------------------------------------'

    def q_mw(self,string):
        """return results of query which matching multiple words and show it"""
        query = {
			'query': {
				'bool':{
					'should': [
							{'match':{'text':string}},
							{'match':{'text':string}}
						  ],
					'minimum_should_match':1
				}
			},
			'highlight': {
				'order': 'score',
				'fields':{'text':{},'title':{}}
			}
		}
        res = self.es.search(index=self.index_name,
                             body=query)
        self.show_highlight_result(res)
        return res

    def q_phr(self,phrase):
        """return results of query which matching the given phrase and show it"""
        query = {
			'query': {
				'bool':{
					'should': [
							{'match_phrase':{'text':phrase}},
							{'match_phrase':{'title':phrase}}
						  ],
					'minimum_should_match':1
				}
			},
			'highlight': {
				'order': 'score',
				'fields':{'text':{},'title':{}}
			}
		}
        res = self.es.search(index=self.index_name,
                             body=query)
        self.show_highlight_result(res)
        return res

    def q_mwf(self,string1,field,string2):
        """return results of query which matching the given words and
           matching certain fields, and then show it"""
        query = {
			'query': {
				'bool': {

					'should': [
							{'match':{'text':string1}},
							{'match':{'title':string1}}
						  ],
					'must': {'match':{field:string2}},
					'minimum_should_match':1
				}
			},
			'highlight': {
				'order': 'score',
				'fields':{'text':{},'title':{},field:{}}
			}
		}
        res = self.es.search(index=self.index_name,
                             body=query)
        self.show_highlight_result(res,[field,'text','title'])
        return res
