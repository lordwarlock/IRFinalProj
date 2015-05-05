#!/usr/bin/python
from elasticsearch import Elasticsearch
import matplotlib.pylab as P

class HistogramQuery():
    """
        Handle Histogram Queries
    """
    def __init__(self,index_name = 'soccer',doc_type = 'match'):
        """
        initialize Elasticsearch settings

	@param index_name: index name in Elasticsearch
	@param doc_type: document type in Elasticsearch
        """
        self.index_name = index_name
        self.doc_type = doc_type
        self.es = Elasticsearch()

    def get_histo_by_team_name(self,team_name):
        """
	Create images of histograms for the given team

	@param team_name: the team name user input

	@return: whether the query is succeccful or not
        """
        home_query =     {
                'size': 100,
                'query': {
                    'match':{
                        'home_team':team_name
                    }
                }
            }
        home_res = self.es.search(index=self.index_name,
                             doc_type = self.doc_type,
                             body=home_query)

        away_query =     {
                'size': 100,
                'query': {
                    'match':{
                        'away_team':team_name
                    }
                }
            }
        away_res = self.es.search(index=self.index_name,
                             doc_type = self.doc_type,
                             body=away_query)
        try:
            self.extract_goal_time(home_res,away_res)
            self.extract_lose_goal_time(home_res,away_res)
            self.extract_goal(home_res,away_res)
            self.extract_lose_goal(home_res,away_res)
            self.extract_shots(home_res,away_res)
            self.extract_hit_woodwork(home_res,away_res)
            self.extract_yellow_cards(home_res,away_res)
            self.extract_shots_on_target(home_res,away_res)
        except:
            return False
        return True

    def extract_goal_time(self,home_res,away_res):
        """
	Extract the time of Goals of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        goals_time = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            for scorer in home_info['_source']['home_scorer']:
                goals_time += scorer['time']
        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            for scorer in away_info['_source']['away_scorer']:
                goals_time += scorer['time']
        P.hist(goals_time,normed = 1,range=(0,90),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/goal_time.png',dpi = 50)
        P.close()

    def extract_lose_goal_time(self,home_res,away_res):
        """
	Extract the time of Goals Against of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        goals_time = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            for scorer in home_info['_source']['away_scorer']:
                goals_time += scorer['time']
        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            for scorer in away_info['_source']['home_scorer']:
                goals_time += scorer['time']
        P.hist(goals_time,normed = 1,range=(0,90),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/goal_against_time.png',dpi = 50)
        P.close()

    def extract_goal(self,home_res,away_res):
        """
	Extract Goals of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        goals = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            goals.append( home_info['_source']['full_time_home_team_goals'] )

        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            goals.append( away_info['_source']['full_time_away_team_goals'] )

        P.hist(goals,normed = 1,range=(0,5),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/goal.png',dpi = 50)
        P.close()

    def extract_lose_goal(self,home_res,away_res):
        """
	Extract Goals Against of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        goals = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            goals.append( home_info['_source']['full_time_away_team_goals'] )

        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            goals.append( away_info['_source']['full_time_home_team_goals'] )

        P.hist(goals,normed = 1,range=(0,5),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/goal_against.png',dpi = 50)
        P.close()

    def extract_shots(self,home_res,away_res):
        """
	Extract Shots of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        shots = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            shots.append( home_info['_source']['home_team_shots'] )

        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            shots.append( away_info['_source']['away_team_shots'] )

        P.hist(shots,normed = 1,range=(0,50),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/shots.png',dpi = 50)
        P.close()

    def extract_hit_woodwork(self,home_res,away_res):
        """
	Extract Hit woodwork times of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        hit_woodwork = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            hit_woodwork.append( home_info['_source']['home_team_hit_woodwork'] )

        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            hit_woodwork.append( away_info['_source']['away_team_hit_woodwork'] )

        P.hist(hit_woodwork,normed = 1,range=(0,30),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/hit_woodwork.png',dpi = 50)
        P.close()

    def extract_yellow_cards(self,home_res,away_res):
        """
	Extract yellow cards of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        yellow_cards = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            yellow_cards.append( home_info['_source']['home_team_yellow_cards'] )

        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            yellow_cards.append( away_info['_source']['away_team_yellow_cards'] )

        P.hist(yellow_cards,normed = 1,range=(0,10),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/yellow_cards.png',dpi = 50)
        P.close()

    def extract_shots_on_target(self,home_res,away_res):
        """
	Extract Shots on target of the given results and store the image of histogram
	into disk

	@param home_res: result from elasticsearch where the given team is home team
	@param away_res: result from elasticsearch where the given team is away team
        """
        shots_on_target = []
        home_infos = home_res['hits']['hits']
        team_name = home_infos[0]['_source']['home_team']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            shots_on_target.append( home_info['_source']['home_team_shots_on_target'] )

        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            shots_on_target.append( away_info['_source']['away_team_shots_on_target'] )

        P.hist(shots_on_target,normed = 1,range=(0,10),color=['c'],label=[team_name])
        P.legend()
        P.savefig('./soccer_search/images/shots_on_target.png',dpi = 50)
        P.close()

if __name__ == '__main__':
    hq = HistogramQuery()
    hq.get_histo_by_team_name('everton')
