'''
Created on Apr 9, 2015

Based on the input "player_query_schema.json" and "player_extraction.json" files, 
build up player's elastic search index.

Then based on player's elastic search index, search player's corresponding information.

@author: Junchao Kang
'''
from elasticsearch import Elasticsearch
from elasticsearch import helpers

import json
import pprint
import time

class playerSearch:
    
    def __init__(self):
        self.es = Elasticsearch()
        self.player_numb = 3546 # Total number of players from the corpus
    
    
    def build_elasticsearch_index(self):
        '''Build up elastic search index from the "player_query_schema.json" and "player_extraction.json" files'''
        
        # Build up schema
        with open('player_query_schema.json', 'rU') as schema_file:
            if self.es.indices.exists(index='players_index'):
                self.es.indices.delete(index='players_index')
                
            self.es.indices.create(index='players_index', body=schema_file.read())
        
        # Build up index
        with open('player_extraction.json', 'rU') as dict_file:
            root_dict = json.load(dict_file)
                
        players = []
        for player in root_dict.values():
            p = {
                '_index': 'players_index',
                '_type': 'player',
                '_source': {
                            'name': player['name'],
                            'height': player['height'],
                            'intro': player['intro'],
                            'birth_place': player['birth_place'],
                            'position': player['position'],
                            'birth_year': player['birth_year']
                            }
                }
            
            players.append(p)
            
        helpers.bulk(self.es, players)
        
        # Gives server some time to build up index
        time.sleep(3)
    
    
    def process_result_list(self, raw_rst):
        processed_rst = []
        for tmp in raw_rst:
            processed_rst.append(tmp['_source'])
        
        return processed_rst
    
    def print_out_search_result(self, rst):
        '''Print out each elastic search results list'''
        
        if len(rst) == 0:
            print 'Search miss'
            return
        
        print 'Search hits number:', len(rst), '\n'
        
        # Print out top 10 search hits
        pp = pprint.PrettyPrinter(indent=4)
        for i in range(0, 10):
            if i >= len(rst):
                break
            
            print 'Search Hit:', i + 1  # Search Hit number is in 1-based index
            pp.pprint(rst[i])
            print
            
            
    def q_birth_year(self, year1, year2):
        '''Search players born in range of [year1, year2]'''
        
        # Validate arguments
        if year1 > year2:
            year1, year2 = year2, year1
        
        query = {
                 'query': {
                            'range': {
                                      'birth_year': {
                                                    'gte' : year1,
                                                    'lte' : year2
                                                    }
                                      }
                           }
                }
        rst = self.es.search(index='players_index', body=query, size=self.player_numb)
        
        return self.process_result_list(rst['hits']['hits'])
    
    
    def q_height(self, height1, height2):
        '''Search players with height in range of [height1, height2]'''
        
        # Validate arguments
        if height1 > height2:
            height1, height2 = height2, height1
        
        query = {
                 'query': {
                            'range': {
                                      'height': {
                                                    'gte' : height1,
                                                    'lte' : height2
                                                    }
                                      }
                           }
                }
        rst = self.es.search(index='players_index', body=query, size=self.player_numb)
        
        return self.process_result_list(rst['hits']['hits'])
    
     
    def q_name(self, name_query):
        '''Search players with certain name'''
        
        query = {
                 'query': {
                           'multi_match': {
                                           'query': name_query,
                                           'fields': ['name']
                                           }
                           }
                }
        rst = self.es.search(index='players_index', body=query, size=self.player_numb)
        
        return self.process_result_list(rst['hits']['hits'])
        
        
    def q_birth_place(self, birth_place_query):
        '''Search players with certain birth place'''
        
        query = {
                 'query': {
                           'multi_match': {
                                           'query': birth_place_query,
                                           'fields': ['birth_place']
                                           }
                           }
                }
        rst = self.es.search(index='players_index', body=query, size=self.player_numb)
        
        return self.process_result_list(rst['hits']['hits'])
    
    
    def q_position(self, position_query):
        '''Search players with certain position'''
        
        query = {
                 'query': {
                           'multi_match': {
                                           'query': position_query,
                                           'fields': ['position']
                                           }
                           }
                }
        rst = self.es.search(index='players_index', body=query, size=self.player_numb)
        
        return self.process_result_list(rst['hits']['hits'])
    
    
    def q_multi_field(self, multi_field_query):
        '''
        Input "multi_field_query" should be a dictionary, which might contain below key-value pairs:
            1). key: "name"; value: string query
            2). key: "birth_place"; value: string query
            3). key: "position"; value: string query
            4). key: "height"; value: a tuple of 2 float values (e.g. (1.68, 1.80))
            5). key: "birth_year"; value: a tuple of 2 positive integers (e.g. (1960, 1990))
        '''
        
        final_rst = []
        is_initialized = False # If the "final_rst" has been initialized
        
        # Process the name query
        if 'name' in multi_field_query:
            final_rst = self.intersect(is_initialized, final_rst, self.q_name(multi_field_query['name']))
            is_initialized = True
        
        # Process the birth_place query
        if 'birth_place' in multi_field_query:
            final_rst = self.intersect(is_initialized, final_rst, self.q_birth_place(multi_field_query['birth_place']))
            is_initialized = True
        
        # Process the position query
        if 'position' in multi_field_query:
            final_rst = self.intersect(is_initialized, final_rst, self.q_position(multi_field_query['position']))
            is_initialized = True
            
        # Process the height query
        if 'height' in multi_field_query:
            height1, height2 = multi_field_query['height']
            final_rst = self.intersect(is_initialized, final_rst, self.q_height(height1, height2))
            is_initialized = True
        
        # Process the birth_year query
        if 'birth_year' in multi_field_query:
            year1, year2 = multi_field_query['birth_year']
            final_rst = self.intersect(is_initialized, final_rst, self.q_birth_year(year1, year2))
            is_initialized = True
            
        return final_rst
        
    
    def intersect(self, is_initialized, final_rst, current_rst):
        '''Intersect the 2 input results set, return the intersection results set'''
        
        if not is_initialized:
            return current_rst
        
        if len(final_rst) == 0:
            return []
        elif len(current_rst) == 0:
            return []
        
        rst = []
        for final_tmp in final_rst:
            final_tmp_name = final_tmp['name']
            
            for current_tmp in current_rst:
                if final_tmp_name == current_tmp['name']:
                    rst.append(final_tmp)
                    break
        
        return rst

    
if __name__ == '__main__':
    query_search = playerSearch()
    
#     query_search.build_elasticsearch_index()
     
#     query_search.q_birth_year(1990, 1975)
#     query_search.q_height(1.69, 1.60)
#     rst = query_search.q_name('salah')
#     rst = query_search.q_birth_place('china')
#     rst = query_search.q_position('')
    
    multi_field_query = {
                        'name': 'Li',
                        'birth_place': 'china',
                        'birth_year': (1900, 1995)
                         }
    rst = query_search.q_multi_field(multi_field_query)
    query_search.print_out_search_result(rst)