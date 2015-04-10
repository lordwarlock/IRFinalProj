'''
Created on Apr 9, 2015

@author: Junchao Kang
'''
from elasticsearch import Elasticsearch
from elasticsearch import helpers

import json
import pprint
import time

es = Elasticsearch()
player_numb = 3546 # Total number of players from the corpus

def build_elasticsearch_index():
    '''Build up elastic search index from the "player_query_schema.json" and "player_extraction.json" files'''
    
    # Build up schema
    with open('player_query_schema.json', 'rU') as schema_file:
        if es.indices.exists(index='players_index'):
            es.indices.delete(index='players_index')
            
        es.indices.create(index='players_index', body=schema_file.read())
    
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
        
    helpers.bulk(es, players)
    
    # Gives server some time to build up index
    time.sleep(3)
    

def print_out_search_result(rst):
    '''Print out each elastic search result'''
    
    if rst['hits']['total'] == 0:
        print 'Search miss'
        return
    
    print 'Search hits number:', rst['hits']['total'], '\n'
    
    # Print out top 10 search hits
    pp = pprint.PrettyPrinter(indent=4)
    for i in range(0, 10):
        if i >= len(rst['hits']['hits']):
            break
        
        print 'Search Hit:', i + 1  # Search Hit number is in 1-based index
        pp.pprint(rst['hits']['hits'][i]['_source'])
        print
        
        
def q_birth_year(year1, year2):
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
    rst = es.search(index='players_index', body=query, size=player_numb)
    
    return rst


def q_height(height1, height2):
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
    rst = es.search(index='players_index', body=query, size=player_numb)
    
    return rst

 
def q_name(name_query):
    '''Search players with certain name'''
    
    query = {
             'query': {
                       'multi_match': {
                                       'query': name_query,
                                       'fields': ['name']
                                       }
                       }
            }
    rst = es.search(index='players_index', body=query, size=player_numb)
    
    return rst
    
    
def q_birth_place(birth_place_query):
    '''Search players with certain birth place'''
    
    query = {
             'query': {
                       'multi_match': {
                                       'query': birth_place_query,
                                       'fields': ['birth_place']
                                       }
                       }
            }
    rst = es.search(index='players_index', body=query, size=player_numb)
    
    return rst


def q_position(position_query):
    '''Search players with certain position'''
    
    query = {
             'query': {
                       'multi_match': {
                                       'query': position_query,
                                       'fields': ['position']
                                       }
                       }
            }
    rst = es.search(index='players_index', body=query, size=player_numb)
    
    return rst


if __name__ == '__main__':
#     build_elasticsearch_index()
     
#     q_birth_year(1990, 1975)
#     q_height(1.69, 1.60)
#     rst = q_name('salah')
#     rst = q_birth_place('china')
    rst = q_position('blah xxxx')
    
    print_out_search_result(rst)