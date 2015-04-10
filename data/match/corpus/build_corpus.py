from crawler import MatchInfo
import re
import glob

class BuildCorpus():
    def __init__(self,query_dir_pattern = '../match_list/*.csv'):
        self.match_data = dict()
        file_dir_list = glob.glob(query_dir_pattern)
        for file_dir in file_dir_list:
            self.readMatchData()
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
                  + str(self.match_data[data_key]['date'].month) + '-'\
                  + str(self.match_data[data_key]['date'].day)

        return self.match_data

