#!/usr/local/bin/python

import unicodedata
import cgi
import cgitb
cgitb.enable()

import sys
sys.path.append('/Users/apple/Documents/Eclipse_Workspace/IR_final_project') # Different for each machine

import Club

def header():  
    '''Print out HTML title, and return the received data'''
     
    print 'Content-Type: text/html\n\n'
    print '<h3>Club Search Result\n</h3>'
    
    # Receive data from web-page
    data = cgi.FieldStorage()
    
    return data


def search(data):
    '''Elastic search the player data, and print out the result'''
    cs = Club.Club()
     
    multi_field_query = {}
    if 'Club_Name' in data:
        multi_field_query['Club_Name'] = data['Club_Name'].value
     
    if ('Founded_gt' in data) and ('Founded_st' in data):
        multi_field_query['Founded'] = (int(data['Founded_gt'].value), int(data['Founded_st'].value))
         
    if 'Ground' in data:
        multi_field_query['Ground'] = data['Ground'].value
        
    if 'Chairman' in data:
        multi_field_query['Chairman'] = data['Chairman'].value
    
    if 'Manager' in data:
        multi_field_query['Manager'] = data['Manager'].value
        
    if 'Website' in data:
        multi_field_query['Website'] = data['Website'].value
        
    if 'League' in data:
        multi_field_query['League'] = data['League'].value
     
    if 'Position' in data:
        multi_field_query['Position'] = data['Position'].value
    
    if 'Nickname' in data:
        multi_field_query['Nickname'] = data['Nickname'].value
        
    if 'Season' in data:
        multi_field_query['Season'] = data['Season'].value
        
    if ('wp_gt' in data) and ('wp_st' in data):
        multi_field_query['Winning_Percentage'] = (int(data['wp_gt'].value), int(data['wp_st'].value))
        
    if 'Summary' in data:
        multi_field_query['Summary'] = data['Summary'].value
    
    rst = cs.q_mwf(multi_field_query)
    
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
        print_club_info(rst[i])
    
    print  '''
            <form>
            <input type="button" onClick="parent.location='http://localhost:8000/soccer.html'" value="Return">
            </form>
            '''


def print_club_info(dict):
    for key in dict.keys():
        print key, ':', unicodedata.normalize('NFKD', unicode(dict[key])).encode('ascii', 'ignore'), '<br>'
    
    print '<br>'
 
if __name__ == '__main__':
    search(header())