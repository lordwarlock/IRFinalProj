#!/usr/local/bin/python

import unicodedata
import cgi
import cgitb
cgitb.enable()

import sys
sys.path.append('/Users/apple/Documents/Eclipse_Workspace/IR_final_project') # Different for each machine

import player_query

def header():  
    '''Print out HTML title, and return the received data'''
     
    print 'Content-Type: text/html\n\n'
    print '<h3>Player Search Result\n</h3>'
    
    # Receive data from web-page
    data = cgi.FieldStorage()
    
    return data


def search(data):
    '''Elastic search the player data, and print out the result'''
    ps = player_query.playerSearch()
    
    multi_field_query = {}
    if 'name' in data:
        multi_field_query['name'] = data['name'].value
    
    if 'birth_place' in data:
        multi_field_query['birth_place'] = data['birth_place'].value
        
    if 'position' in data:
        multi_field_query['position'] = data['position'].value
    
    if ('height_st' in data) and ('height_gt' in data):
        multi_field_query['height'] = (int(data['height_st'].value), int(data['height_st'].value))
    
    if ('birth_year_st' in data) and ('birth_year_gt' in data):
        multi_field_query['birth_year'] = (int(data['birth_year_st'].value), int(data['birth_year_gt'].value))
    
    rst = ps.q_multi_field(multi_field_query)
    
    # Process search result
    if len(rst) == 0:
        print 'Search miss<br>'
        return
    
    print 'Total search hits number: ', len(rst), '<br><br>'
    
    # Print out top 10 search hits
    for i in range(0, 10):
        if i >= len(rst):
            break
        
        print 'Search hit ', i + 1, '<br>'    
        print_player_info(rst[i])
    
    print  '''
            <form>
            <input type="button" onClick="parent.location='http://localhost:8000/soccer.html'" value="Return">
            </form>
            '''


def print_player_info(dict):
    for key in dict.keys():
        print key, ':', unicodedata.normalize('NFKD', unicode(dict[key])).encode('ascii', 'ignore'), '<br>'
    
    print '<br>'
 
if __name__ == '__main__':
    search(header())