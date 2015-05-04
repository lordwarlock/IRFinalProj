from elasticsearch import Elasticsearch
import json
"""
half_time_home_team_goals
away_team_corners
report
away_sub
full_time_result
home_start_11
half_time_away_team_goals
away_team
away_team_hit_woodwork
away_team_red_cards
home_team_hit_woodwork
home_team_shots_on_target
key_name
referee
away_start_11
home_team_corners
home_team_yellow_cards
home_scorer
date
home_team_shots
league
home_team
away_team_yellow_cards
away_scorer
half_time_result
away_team_shots_on_target
home_sub
full_time_home_team_goals
home_team_red_cards
full_time_away_team_goals
away_team_shots
ratings
"""
class MatchQuery:
    def __init__(self,index_name = 'soccer',doc_type = 'match'):
        """Queries for the give index name"""
        self.index_name = index_name
        self.doc_type = doc_type
        self.es = Elasticsearch()

    def make_nested_range_query_clause(self,path,field,value1,value2):
        query_clause = dict()
        query_clause['nested'] = dict()
        query_clause['nested']['path'] = path
        query_clause['nested']['query'] = dict()
        query_clause['nested']['query']['range'] = dict()
        query_clause['nested']['query']['range'][path+'.'+field] = dict()
        query_clause['nested']['query']['range'][path+'.'+field]['gte'] = value1
        query_clause['nested']['query']['range'][path+'.'+field]['lte'] = value2
        return query_clause

    def make_nested_match_query_clause(self,path,field,value):
        query_clause = dict()
        query_clause['nested'] = dict()
        query_clause['nested']['path'] = path
        query_clause['nested']['query'] = dict()
        query_clause['nested']['query']['match'] = dict()
        query_clause['nested']['query']['match'][path+'.'+field] = dict()
        query_clause['nested']['query']['match'][path+'.'+field] = value
        return query_clause

    def make_range_query_clause(self,field,value1,value2):
        query_clause = dict()
        query_clause['range'] = dict()
        query_clause['range'][field] = dict()
        query_clause['range'][field]['gte'] = value1
        query_clause['range'][field]['lte'] = value2
        return query_clause

    def make_match_query_clause(self,field,value):
        query_clause = dict()
        query_clause['match'] = dict()
        query_clause['match'][field] = value
        return query_clause

    def make_and_query(self,query_clauses):
        query = dict()
        query['query'] = dict()
        query['query']['bool'] = dict()
        query['query']['bool']['must'] = query_clauses
        return query

    def q_query(self,query):
        res = self.es.search(index=self.index_name,
                             doc_type = self.doc_type,
                             body=query)

        return res

    def preprocess_query_template(self,query_dict):
        preprocessed = dict()
        for key,value in query_dict.iteritems():
            if key == 'Player':
                preprocessed[key] = self.preprocess_player(value)

            elif type(value) == type(preprocessed):
                preprocessed[key] = dict()
                if value[0] != None:
                    preprocessed[key][0] = value[0]
                else:
                    preprocessed[key][0] = -1
                if value[1] != None:
                    preprocessed[key][1] = value[1]
                else:
                    preprocessed[key][1] = 999
            elif value == None:
                preprocessed[key] = '""'
            else:
                if type(value) == type('string'):
                    preprocessed[key] = '"'+value+'"'
                else:
                    preprocessed[key] = value
        print preprocessed
        return preprocessed

    def preprocess_player(self,player_list):
        preprocessed_list = []
        for player in player_list:
            preprocessed = dict()
            value = player
            for s_key,s_value in value.iteritems():
                if type(s_value) == type(preprocessed):
                    preprocessed[s_key] = dict()
                    if s_value[0] != None:
                        preprocessed[s_key][0] = s_value[0]
                    else:
                        preprocessed[s_key][0] = -1
                    if s_value[1] != None:
                        preprocessed[s_key][1] = s_value[1]
                    else:
                        preprocessed[s_key][1] = 999
                elif s_value == None:
                    preprocessed[s_key] = '""'
                else:
                    if type(s_value) == type('string'):
                        preprocessed[s_key] = '"'+s_value+'"'
                    else:
                        preprocessed[s_key] = s_value
            preprocessed_list.append(preprocessed)
        return preprocessed_list

    def query_template(self,query_dict):
        with open('match_query_sample.txt','r') as f_i:
            template = f_i.read()
            preprocessed_query = self.preprocess_query_template(query_dict)
            player_query,player_string = self.player_template(preprocessed_query['Player'])
            query = template.format(preprocessed_query['Home_Team'],
                                    preprocessed_query['Away_Team'],
                                    preprocessed_query['Home_Goals'][0],
                                    preprocessed_query['Home_Goals'][1],
                                    preprocessed_query['Away_Goals'][0],
                                    preprocessed_query['Away_Goals'][1],
                                    preprocessed_query['Match_Date'][0],
                                    preprocessed_query['Match_Date'][1],
                                    player_query,
                                    player_string
                                   )
        return json.loads(query)

    def player_template(self,player_list):
        query_list = []
        query_string = []
        with open('player_query_sample.txt','r') as f_i:
            template = f_i.read()
            for player in player_list:
                query = template.format(player['Name'],
                                        player['Start_11'],
                                        player['Scores'][0],
                                        player['Scores'][1],
                                        player['Rate'][0],
                                        player['Rate'][1],
                                        player['Scores_Time'][0],
                                        player['Scores_Time'][1],
                                       )
                query_string.append(player['Name'])
                query_list.append(query)
        return ','.join(query_list),' '.join(query_string)

    def q_report(self,text):
        query = {
			'query': {
				'match':{
					'report':text
				}
			},
			'highlight': {
				'fields':{
					'report':{}
				}
			}
		}
        return self.q_query(query)
if __name__ == '__main__':
    m = MatchQuery()
    q1 = m.make_match_query_clause('home_team_red_cards',2)
    q2 = m.make_range_query_clause('date','2012-10-27','2012-10-28')
    q = m.make_and_query([q1,q2])
    print m.q_query(q)['hits']['hits'][0]['_source']['home_team']

    q1 = m.make_nested_match_query_clause('away_scorer','player','Lukaku')
    q2 = m.make_nested_range_query_clause('away_scorer','time',9,10)
    q3 = m.make_nested_range_query_clause('ratings','time',54,55)
    q4 = m.make_and_query([q1,q2])
    q = {
		'query':{
			'nested':{
				'path':'ratings',
				'query':{
					'bool':{
						'must':[
						{'match':{
							'ratings.name': 'Lukaku'
						}},
						{'range':{
							'ratings.scores': {'gte': -1, 'lte': 999}
						}},
						{'range':{
							'ratings.scores_time': {
								"gte":54,
								"lte":55
							}
						}}]
					}
				}
			}
		}
	}
    print q4
    #print json.dumps(q4,sort_keys=True,indent=4,separators=(',',':'))
    print m.q_query(q)['hits']['hits'][0]['_source']['away_scorer']#.keys()
    print m.q_query(q)['hits']['hits'][0]['_source']['home_team']#.keys()
    print m.q_query(q)['hits']['hits'][0]['_source']['away_team']#.keys()
    preprocessed_query = dict()
    preprocessed_query['Home_Team'] = 'Newcastle'
    preprocessed_query['Away_Team'] = 'everton'
    preprocessed_query['Home_Goals'] = dict()
    preprocessed_query['Home_Goals'][0] = None
    preprocessed_query['Home_Goals'][1] = None
    preprocessed_query['Away_Goals'] = dict()
    preprocessed_query['Away_Goals'][0] = None
    preprocessed_query['Away_Goals'][1] = None
    preprocessed_query['Match_Date'] = dict()
    preprocessed_query['Match_Date'][0] = None
    preprocessed_query['Match_Date'][1] = None
    preprocessed_query['Player'] = [dict()]
    preprocessed_query['Player'][0]['Name'] = 'Lukaku'
    preprocessed_query['Player'][0]['Start_11'] = None
    preprocessed_query['Player'][0]['Scores'] = dict()
    preprocessed_query['Player'][0]['Scores'][0] = 1
    preprocessed_query['Player'][0]['Scores'][1] = 1
    preprocessed_query['Player'][0]['Rate'] = dict()
    preprocessed_query['Player'][0]['Rate'][0] = None
    preprocessed_query['Player'][0]['Rate'][1] = None
    preprocessed_query['Player'][0]['Scores_Time'] = dict()
    preprocessed_query['Player'][0]['Scores_Time'][0] = 54
    preprocessed_query['Player'][0]['Scores_Time'][1] = 55
    q4 = m.query_template(preprocessed_query)
    print json.dumps(q4,sort_keys=True,indent=4,separators=(',',':'))
    q = {
    "query":{
        "bool":{
            "must":[
                {
                    "match":{
                        "home_team":{
				"query": 'West Brom',
				"fuzziness": "AUTO"
			}
                    }
                },
                {
                    "match":{
                        "away_team":{
				"query": 'Man Utd',
				"fuzziness": "AUTO",
			}
                    }
                },
                {
                    "range":{
                        "full_time_home_team_goals":{
                            "gte":-1,
                            "lte":999
                        }
                    }
                },
                {
                    "range":{
                        "full_time_away_team_goals":{
                            "gte":-1,
                            "lte":999
                        }
                    }
                }
            ]
        }
    }
}
    print m.q_query(q4)['hits']['hits'][0]['_source']['home_team']
    print m.q_query(q4)['hits']['hits'][0]['_source']['away_team']
    print m.q_query(q4)['hits']['hits'][0]['_source']['ratings']
    print m.q_query(q4)['hits']['hits'][0]['highlight']
    print m.q_report('newcastle everton lukaku')['hits']['hits'][0]['highlight']
