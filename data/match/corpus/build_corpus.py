from crawler import MatchInfo
import re
import glob
import json
from extract_team import ExtractTeam
from extract_ratings import ExtractRatings
class BuildCorpus():
    def __init__(self,query_dir_pattern = '../match_list/*.csv',
                      html_dir = '../teams_html_files/',
                      text_dir = '../extract/txt_files/',
                      rate_dir = '../ratings_html_files/',
                      output_file = 'match_corpus_ratings.json'):
        self.match_data = dict()
        self.html_dir = html_dir
        self.text_dir = text_dir
        self.rate_dir = rate_dir
        self.extract_html = ExtractTeam().extract_html
        self.extract_rate = ExtractRatings().process_HTML
        file_dir_list = glob.glob(query_dir_pattern)
        for file_dir in file_dir_list:
            print len(self.readMatchData(file_dir))
        print len(self.match_data['E0_01_01_13_Man_City'])
        #with open(output_file,'w') as f_o:
        #    f_o.write(json.dumps(self.match_data))
        #print self.match_data
        with open(output_file,'w') as f_o:
            for value in self.match_data.values():
                f_o.write(json.dumps(value))
                f_o.write('\n')

    def readMatchData(self,query_dir = '../match_list/E0.csv'):

        with open(query_dir,'r') as f_csv:
            _ = f_csv.readline()
            for line in f_csv:
                splitted = line.split(',')
                data_key = splitted[0] + '_' + re.sub('/','_',splitted[1])\
                         + '_' + re.sub(' ','_',splitted[2])
                #print data_key
                self.match_data[data_key] = MatchInfo(splitted).__dict__
                self.match_data[data_key]['date'] = \
                    str(self.match_data[data_key]['date'].year) + '-'\
                  + str(self.match_data[data_key]['date'].month).zfill(2) + '-'\
                  + str(self.match_data[data_key]['date'].day).zfill(2)
                self.get_teams_info(data_key)
                self.get_ratings_info(data_key)
                self.match_data[data_key]['key_name'] = data_key
                with open(self.text_dir+data_key+'.txt','r') as f_t:
                    self.match_data[data_key]['report'] = f_t.read()
                #print self.match_data[data_key]
        return self.match_data

    def get_ratings_info(self,key):
        home_ratings,away_ratings = self.extract_rate(self.rate_dir + key)

        #Start 11
        for rate_dict in home_ratings:
            name = rate_dict['name']
            flag = 1
            for player in self.match_data[key]['home_start_11']:
                if player in name:
                    flag = 0
                    rate_dict['start_11'] = 1
                    break
            if flag:
                rate_dict['start_11'] = 0
            rate_dict['scores'] = 0
            rate_dict['scores_time'] = []
            for scorer_dict in self.match_data[key]['home_scorer']:
                if name in scorer_dict['player']:
                    rate_dict['scores'] = len(scorer_dict['time'])
                    rate_dict['scores_time'] = scorer_dict['time']
                    break

        for rate_dict in away_ratings:
            name = rate_dict['name']
            flag = 1
            for player in self.match_data[key]['away_start_11']+self.match_data[key]['away_sub']:
                if player in name:
                    flag = 0
                    rate_dict['start_11'] = 1
                    break
            if flag:
                rate_dict['start_11'] = 0
            rate_dict['scores'] = 0
            rate_dict['scores_time'] = []
            for scorer_dict in self.match_data[key]['away_scorer']:
                if name in scorer_dict['player']:
                    rate_dict['scores'] = len(scorer_dict['time'])
                    rate_dict['scores_time'] = scorer_dict['time']
                    break

        self.match_data[key]['ratings'] = home_ratings + away_ratings

    def get_teams_info(self,key):
        (self.match_data[key]['home_start_11'],\
        self.match_data[key]['away_start_11']),\
        (self.match_data[key]['home_scorer'],\
        self.match_data[key]['away_scorer']),\
        (self.match_data[key]['home_sub'],\
        self.match_data[key]['away_sub']) = \
        self.extract_html(self.html_dir + key)

if __name__ == '__main__':
    BuildCorpus()
