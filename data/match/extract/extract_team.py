import re,glob

class ExtractTeam():
    def __init__(self,teams_dir_pattern = None):
        #self.extract_html('../teams_html_files/E0_01_01_13_Southampton')
        if teams_dir_pattern == None:
            pass
        else:
            file_dir_list = glob.glob(teams_dir_pattern)
            for file_dir in file_dir_list:
                self.extract_html(file_dir)
                #break
    def extract_html(self,html_file):
        with open(html_file,'r') as f_i:
            text = f_i.read()
            #print self.extract_squad(text)
            print self.extract_scorer(text)
            #print self.extract_sub(text)

    def extract_squad(self,text):
        home_match = re.search('<div class="tab-section " id="teamlineup-homeTeam">(.*?)</div>',text,re.DOTALL)
        
        home_start_11 = re.findall('<span class="p-name">(.*?)</span>',home_match.group(1))

        away_match = re.search('id="teamlineup-awayTeam">(.*?)</div>',text,re.DOTALL)
        
        away_start_11 = re.findall('<span class="p-name">(.*?)</span>',away_match.group(1))

        return home_start_11,away_start_11

    def extract_scorer(self,text):
        home_match = re.search('<div class="side side-home">(.*?)</div>',
                               text,re.DOTALL)
        home_scorer_raw = re.findall('([A-Z].*?\(.*?\))',home_match.group(1))

        away_match = re.search('<div class="side side-away">(.*?)</div>',
                               text,re.DOTALL)
        away_scorer_raw = re.findall('([A-Z].*?\(.*?\))',away_match.group(1))

        home_dict = dict()
        for scorer_raw in home_scorer_raw:
            self.get_scorer_and_times(scorer_raw,home_dict)
        away_dict = dict()
        for scorer_raw in away_scorer_raw:
            self.get_scorer_and_times(scorer_raw,away_dict)

        print home_scorer_raw,away_scorer_raw
        return home_dict,away_dict

    def extract_sub(self,text):
        home_match = re.search('<div class="tab-section " id="teamlineup-homeTeam">.*?<h4 class="sq-head">Subs</h4>(.*?)</ul>',text,re.DOTALL)
        home_sub = re.findall('<span class="p-name">(.*?)</span>',home_match.group(1))
        away_match = re.search('id="teamlineup-awayTeam">.*?<h4 class="sq-head">Subs</h4>(.*?)</ul>',text,re.DOTALL)
        away_sub = re.findall('<span class="p-name">(.*?)</span>',away_match.group(1))
        return home_sub,away_sub

    def get_scorer_and_times(self,text,scorer_dict):
        match = re.match('([A-Z].*)\((.*)\)',text)
        times = re.findall('([0-9]+)(?:\+[0-9])?',match.group(2))
        scorer_dict[match.group(1)] = [int(x) for x in times]
        

if __name__ == '__main__':
    ExtractTeam('../teams_html_files/E0_*')
