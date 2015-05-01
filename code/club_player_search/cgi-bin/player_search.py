#!/usr/local/bin/python

import unicodedata

import sys
sys.path.append('/Users/apple/Documents/Eclipse_Workspace/IR_final_project') # Different for each machine

import meta_search
import player_query

def search(data):
    '''Elastic search the player data, and print out the result'''
    ps = player_query.playerSearch()
    
    multi_field_query = {}
    
    # Deal with string search query
    range_query_list = ['height_gt', 'height_st', 'birth_year_gt', 'birth_year_st']
    for key in data:
        if key in range_query_list:
            continue
        
        if key == data[key].value:
            continue
        
        multi_field_query[key] = data[key].value
    
    # Deal with range search query
    if ('height_gt' in data) and ('height_st' in data):
        multi_field_query['height'] = (int(data['height_gt'].value), int(data['height_st'].value))
    
    if ('birth_year_gt' in data) and ('birth_year_st' in data):
        multi_field_query['birth_year'] = (int(data['birth_year_gt'].value), int(data['birth_year_st'].value))
    
    return ps.q_multi_field(multi_field_query)


def process_player_info(dict, i):
    rst = '''
            <div class="col_1_of_b span_1_of_b">
                <a href="single.html"></a>
                <div>Search hit: {}</div><br>\n
            '''.format(i)
            
    for key in dict.keys():
        buffer = key + ':' + unicodedata.normalize('NFKD', unicode(dict[key])).encode('ascii', 'ignore') + '<br>\n'
        rst += '''
                    <div class="links">
                          <ul>
                             <li><span>{}: {}</span></li>
                          </ul>
                      </div>\n
                      '''.format(key, buffer)
    
    rst += '''
            </div>\n
            '''
    
    return rst
 
if __name__ == '__main__':
    data = meta_search.header('Player')
    rearch_rst =  meta_search.find_search_result(search(data), process_player_info)
    meta_search.write_and_jump(rearch_rst)