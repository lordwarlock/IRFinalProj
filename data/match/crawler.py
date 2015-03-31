class MatchDate():
    def __init__(self,raw_date):
        splitted = raw_date.split('/')
        self.day = int(splitted[0])
        self.month = int(splitted[1])
        #all data are after 2000
        self.year = int(splitted[2]) + 2000

class match():
    def __init__(self,info_list):
        self.league = info_list[0]
        self.date = MatchDate(info_list[1])
        self.home_team = info_list[2]
        self.away_team = info_list[3]
        self.full_time_home_team_goals = info_list[4]
        self.full_time_away_team_goals = info_list[5]
        self.full_time_resut = info_list[6]
        self.half_time_home_team_goals = info_list[7]
        self.half_time_away_team_goals = info_list[8]
        self.half_time_result = info_list[9]
        self.referee = info_list[10]
        self.home_team_shots = info_list[11]
        self.away_team_shots = info_list[12]
        self.home_team_shots_on_target = info_list[13]
        self.away_team_shots_on_target = info_list[14]
        self.home_team_hit_woodwork = info_list[15]
        self.away_team_hit_woodwork = info_list[16]
        self.home_team_corners = info_list[17]
        self.away_team_corners = info_list[18]
        self.home_team_yellow_cards = info_list[19]
        self.away_team_yellow_cards = info_list[20]
        self.home_team_red_cards = info_list[21]
        self.away_team_red_cards = info_list[22]

class BingCrawler():
    def __init__(self,
                 pattern = '"http://www1.skysports.com/football/live/match/.*?/report"'),
                 query_dir_pattern = './match_list/*.csv')

    def readMatchData(self,query_dir = './match_list/E0.csv'):
        match_data = dict()
        with open(query_dir,'r') as f_csv:
            _ = f_csv.readline()
            for line in f_csv:
                splitted = line.split(',')
                data_key = splitted[0] + splitted[1] + splitted[2]
                
        
