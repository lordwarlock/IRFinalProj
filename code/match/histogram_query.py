from elasticsearch import Elasticsearch
import matplotlib.pylab as P
class HistogramQuery():
    def __init__(self,index_name = 'soccer',doc_type = 'match'):
        self.index_name = index_name
        self.doc_type = doc_type
        self.es = Elasticsearch()

    def get_histo_by_team_name(self,team_name):
        home_query = 	{
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

        away_query = 	{
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
        self.extract(home_res,away_res)

    def extract(self,home_res,away_res):
        goals_time = []
        home_infos = home_res['hits']['hits']
        #print home_res['hits']['total'],len(home_res['hits']['hits'])
        for home_info in home_infos:
            for scorer in home_info['_source']['home_scorer']:
                goals_time += scorer['time']
        away_infos = away_res['hits']['hits']
        for away_info in away_infos:
            for scorer in away_info['_source']['home_scorer']:
                goals_time += scorer['time']
        P.hist(goals_time,normed = 1,range=(0,90))
        P.savefig('goal_time.png',dpi = 40)

if __name__ == '__main__':
    hq = HistogramQuery()
    hq.get_histo_by_team_name('everton')
