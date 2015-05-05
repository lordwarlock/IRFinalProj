#!/usr/bin/python

import unicodedata

import sys
sys.path.append('/Users/apple/Documents/Eclipse_Workspace/IR_final_project') # Different for each machine

import match_query
import meta_search


def search(data):
    '''Elastic search the match data, and return the search result'''
    mq = match_query.MatchQuery()
    
    multi_field_query = {}
    
    # Deal with player information search
    player_dict = {}
    
    player_dict['Start_11'] = None
    
    if 'player_name' == data['player_name'].value:
        player_dict['Name'] = None
    else:
        player_dict['Name'] = data['player_name'].value
    
    if ('score_gt' in data) and ('score_st' in data):
        player_dict['Scores'] = {0:int(data['score_gt'].value), 1:int(data['score_st'].value)}
    else:
        player_dict['Scores'] = {0:None,1:None}
    
    if ('rating_gt' in data) and ('rating_st' in data):
        player_dict['Rate'] = {0:int(data['rating_gt'].value), 1:int(data['rating_st'].value)}
    else:
        player_dict['Rate'] = {0:None,1:None}
        
    if ('goal_time_gt' in data) and ('goal_time_st' in data):
        player_dict['Scores_Time'] = {0:int(data['goal_time_gt'].value), 1:int(data['goal_time_st'].value)}
    else:
        player_dict['Scores_Time'] = {0:None,1:None}
    
    # Deal with match search
    match_query_dict = {}
    match_query_dict['Player'] = [player_dict]
    
    if 'home_team' == data['home_team'].value:
        match_query_dict['home_team'] = None
    else:
        match_query_dict['home_team'] = data['home_team'].value
    
    if 'away_team' == data['away_team'].value:
        match_query_dict['away_team'] = None
    else:
        match_query_dict['away_team'] = data['away_team'].value
    
    if ('home_goal_gt' in data) and ('home_goal_st' in data):
        match_query_dict['home_goals'] = {0:int(data['home_goal_gt'].value), 1:int(data['home_goal_st'].value)}
    else:
        match_query_dict['home_goals'] = {0:None,1:None}
        
    if ('away_goal_gt' in data) and ('away_goal_st' in data):
        match_query_dict['away_goals'] = {0:int(data['away_goal_gt'].value), 1:int(data['away_goal_st'].value)}
    else:
        match_query_dict['away_goals'] = {0:None,1:None}
        
    if ('match_date_gt' in data) and ('match_date_st' in data):
        match_query_dict['match_date'] = {0:data['match_date_gt'].value, 1:data['match_date_st'].value}
    else:
        match_query_dict['match_date'] = {0:None,1:None}
        
    return mq.q_match(match_query_dict)


def process_match_info(dict, i): # To be modified
    rst = '''
            <div class="col_1_of_b span_1_of_b">
                <h3>Search Hit {}</h3>\n
            '''.format(i)
    
    # 'home_scorer', 'away_scorer', 
    jump_list = ['ratings', 'away_sub', 'home_start_11', 'away_start_11', 'home_sub', 'key_name', 'league']
    
    for key in dict.keys():
        if key in jump_list:
            continue
        
        buffer = key + ': ' + unicodedata.normalize('NFKD', unicode(dict[key])).encode('ascii', 'ignore') + '<br>\n'
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
    data = meta_search.receive_data()
#     print search(data)
    rearch_rst =  meta_search.find_search_result(search(data), process_match_info)
    meta_search.write_and_jump(rearch_rst)