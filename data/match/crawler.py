import urllib
import re
import glob

class MatchDate():
    def __init__(self,raw_date):
        splitted = raw_date.split('/')
        self.day = int(splitted[0])
        self.month = int(splitted[1])
        #all data are after 2000
        self.year = int(splitted[2]) + 2000

    def day_to_string(self):
        day = self.day
        if (day % 10 == 1): return str(day) + 'st'
        if (day % 10 == 2): return str(day) + 'nd'
        if (day % 10 == 3): return str(day) + 'rd'
        return str(day) + 'th'

    def month_to_string(self):
        month = self.month
        if (month == 1): return 'Jan'
        if (month == 2): return 'Feb'
        if (month == 3): return 'Mar'
        if (month == 4): return 'Apr'
        if (month == 5): return 'May'
        if (month == 6): return 'Jun'
        if (month == 7): return 'Jul'
        if (month == 8): return 'Aug'
        if (month == 9): return 'Sep'
        if (month == 10): return 'Oct'
        if (month == 11): return 'Nov'
        if (month == 12): return 'Dec'

class MatchInfo():
    def __init__(self,info_list):
        self.league = info_list[0]
        self.date = MatchDate(info_list[1])
        if info_list[2] == 'Birmingham':
            self.home_team = "Birm'ham"
        else:
            self.home_team = info_list[2]

        if info_list[3] == 'Birmingham':
            self.away_team = "Birm'ham"
        else:
            self.away_team = info_list[3]

        self.full_time_home_team_goals = int(info_list[4])
        self.full_time_away_team_goals = int(info_list[5])
        self.full_time_result = info_list[6]
        self.half_time_home_team_goals = int(info_list[7])
        self.half_time_away_team_goals = int(info_list[8])
        self.half_time_result = info_list[9]
        if info_list[10].isdigit():
            self.referee = None
            i = 9
        else:
            self.referee = info_list[10]
            i = 10
        self.home_team_shots = int(info_list[i+1])
        self.away_team_shots = int(info_list[i+2])
        self.home_team_shots_on_target = int(info_list[i+3])
        self.away_team_shots_on_target = int(info_list[i+4])
        self.home_team_hit_woodwork = int(info_list[i+5])
        self.away_team_hit_woodwork = int(info_list[i+6])
        self.home_team_corners = int(info_list[i+7])
        self.away_team_corners = int(info_list[i+8])
        self.home_team_yellow_cards = int(info_list[i+9])
        self.away_team_yellow_cards = int(info_list[i+10])
        self.home_team_red_cards = int(info_list[i+11])
        self.away_team_red_cards = int(info_list[i+12])

class BingCrawler():
    def __init__(self,
                 pattern = '"(http://www1.skysports.com/football/live/match/[0-9]+)',
                 query_dir_pattern = './match_list/*.csv'):
        self.f_err = open('err_log','w')
        self.pattern = pattern
        self.match_data = dict()
        file_dir_list = glob.glob(query_dir_pattern)
        for file_dir in file_dir_list:
            self.readMatchData(file_dir)
        self.build_corpus()
        self.f_err.close()

    def readMatchData(self,query_dir = './match_list/E0.csv'):

        with open(query_dir,'r') as f_csv:
            _ = f_csv.readline()
            for line in f_csv:
                splitted = line.split(',')
                data_key = splitted[0] + '_' + re.sub('/','_',splitted[1])\
                         + '_' + re.sub(' ','_',splitted[2])
                #print data_key
                self.match_data[data_key] = MatchInfo(splitted)
        return self.match_data

    def make_bing_query(self,match_info):
        query = 'http://www.bing.com/search?q='
        query += str(match_info.date.year) + '+'
        query += match_info.date.month_to_string() + '+'
        query += match_info.date.day_to_string() + '+'
        query += match_info.home_team + '+' + match_info.away_team
        query += '+skysports+report'
        return query

    def get_result_from_bing_query(self,match_info):
        query = self.make_bing_query(match_info)
        urlobj = urllib.urlopen(query)
        return urlobj

    def get_url_from_skysports_report(self,urlobj,match_info,key):
        search_obj = re.search(self.pattern,urlobj.read())
        urlobj.close()
        try:
            skysports_url = search_obj.group(1)
        except:
            print 'WARN: Skysports url Not Found',\
                  match_info.date.year,\
                  match_info.date.month,\
                  match_info.date.day,\
                  match_info.home_team,\
                  match_info.away_team
            self.f_err.write(key+'\n')
            return 'http://www1.skysports.com/football/live/match/no_such_page'
        print skysports_url+'/report'
        return skysports_url+'/report'

    def get_skysports_report_for_match(self,match_info,key):
        bing_result = self.get_result_from_bing_query(match_info)
        skysports_url = self.get_url_from_skysports_report(bing_result,
                                                           match_info,
                                                           key)
        urlobj = urllib.urlopen(skysports_url)
        return urlobj.read()

    def build_corpus(self):
        for key,match_info in self.match_data.iteritems():
            output_file = open('./html_files/'+key,'w')
            output_file.write(self.get_skysports_report_for_match(match_info,key))
            output_file.close()
            print key
if __name__ == '__main__':
    BingCrawler()
