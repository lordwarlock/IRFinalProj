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
if __name__ == '__main__':
    m = MatchQuery()
    q1 = m.make_match_query_clause('home_team_red_cards',2)
    q2 = m.make_range_query_clause('date','2012-10-27','2012-10-28')
    print m.make_and_query([q1,q2])

    q1 = m.make_nested_match_query_clause('away_scorer','player','Lukaku')
    q2 = m.make_nested_range_query_clause('away_scorer','time',54,55)
    q3 = m.make_and_query([q1,q2])
    print m.q_query(q3)['hits']['hits'][0]['_source'].keys()
