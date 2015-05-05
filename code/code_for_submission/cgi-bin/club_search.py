#!/usr/bin/python

import unicodedata

import meta_search

import sys
sys.path.append('./club_query')
import Club


def main():
    '''Club search's main functionality. Receive cgi data from club web-page, do elastic search, and jump into the result page.'''
    
    data = meta_search.receive_data()
    rearch_rst =  meta_search.find_search_result(search(data), process_club_info)
    meta_search.write_and_jump(rearch_rst)


def search(data):
    '''
    Elastic search the club, and return the search result list.
    
    @param data: the cgi data from the club search web-page
    
    @return: the elastic search result list
    '''
    
    cs = Club.Club()
    
    multi_field_query = {}
    
    # Deal with match search query
    range_query_list = ['Capacity_gt', 'Capacity_st', 'Founded_gt', 'Founded_st', 'wp_gt', 'wp_st']
    for key in data:
        if key in range_query_list:
            continue
        
        if key == data[key].value:
            continue
        
        multi_field_query[key] = data[key].value
    
    # Deal with range search query
    if ('Capacity_gt' in data) and ('Capacity_st' in data):
        multi_field_query['Capacity'] = (int(data['Capacity_gt'].value), int(data['Capacity_st'].value))
    
    if ('Founded_gt' in data) and ('Founded_st' in data):
        multi_field_query['Founded'] = (int(data['Founded_gt'].value), int(data['Founded_st'].value))
        
    if ('wp_gt' in data) and ('wp_st' in data):
        multi_field_query['Winning_Percentage'] = (int(data['wp_gt'].value), int(data['wp_st'].value))
    
    return cs.q_mwf(multi_field_query)


def process_club_info(dict, i):
    '''
    Process a searched club information into html string.
    
    @param dict: the searched club information
    @param i: current search hit number
    
    @return: the html string that corresponds to current club information
    '''
    
    rst = '''
            <div class="col_1_of_b span_1_of_b">
                <h3>Search Hit {}</h3>\n
            '''.format(i)
            
    for key in dict.keys():
        if key == 'Website':
            web_url = unicodedata.normalize('NFKD', unicode(dict[key])).encode('ascii', 'ignore')
            buffer = key + ': <a href="' + web_url + '">' + web_url + '</a><br>\n'
            rst += '''
                <div class="links">
                    <ul>
                        <li><span>{}</span></li>
                    </ul>
                </div>\n
                '''.format(buffer)
            continue
        
        if key == 'Summary':
            continue
         
        buffer = key + ': ' + unicodedata.normalize('NFKD', unicode(dict[key])).encode('ascii', 'ignore') + '<br>\n'
        rst += '''
                <div class="links">
                    <ul>
                        <li><span>{}</span></li>
                    </ul>
                </div>\n
                '''.format(buffer)
    
    buffer = 'Summary: ' + unicodedata.normalize('NFKD', unicode(dict['Summary'])).encode('ascii', 'ignore') + '<br>\n'
    rst += '''
            <div class="links">
                <ul>
                    <li><span>{}</span></li>
                </ul>
            </div>\n
            '''.format(buffer)
              
    rst += '''
            </div>\n
            '''
    
    return rst


if __name__ == '__main__':
    main()