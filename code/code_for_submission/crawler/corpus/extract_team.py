import re,glob

class ExtractTeam():
    """Extract Team Information From Html Files"""
    def __init__(self,teams_dir_pattern = None):
        """
        Initialize

        @param teams_didr_pattern: pattern of directory of html containing team information
        """
        if teams_dir_pattern == None:
            pass
        else:
            file_dir_list = glob.glob(teams_dir_pattern)
            for file_dir in file_dir_list:
                self.extract_html(file_dir)

    def extract_html(self,html_file):
        """
        Extract certain field of information in html file

        @param html_file: directory of html files
        """
        with open(html_file,'r') as f_i:
            text = f_i.read()

            return self.extract_squad(text),\
                   self.extract_scorer(text),\
                   self.extract_sub(text)

    def extract_squad(self,text):
        """
        Extract Squad from the given text

        @param text: content of html file

        @return: squad of home team and away team
        """
        home_match = re.search('<div class="tab-section " id="teamlineup-homeTeam">(.*?)</div>',text,re.DOTALL)
        
        home_start_11 = re.findall('<span class="p-name">(.*?)</span>',home_match.group(1))

        away_match = re.search('id="teamlineup-awayTeam">(.*?)</div>',text,re.DOTALL)
        
        away_start_11 = re.findall('<span class="p-name">(.*?)</span>',away_match.group(1))

        return home_start_11,away_start_11

    def extract_scorer(self,text):
        """
        Extract Information of scorers from given text

        @param text: content of html file

        @return: list of scorer of home team and away team.
        """
        home_match = re.search('<div class="side side-home">(.*?)</div>',
                               text,re.DOTALL)
        home_scorer_raw = re.findall('([A-Z].*?\(.*?\))',home_match.group(1))

        away_match = re.search('<div class="side side-away">(.*?)</div>',
                               text,re.DOTALL)
        away_scorer_raw = re.findall('([A-Z].*?\(.*?\))',away_match.group(1))

        home_list = []
        for scorer_raw in home_scorer_raw:
            self.get_scorer_and_times(scorer_raw,home_list)
        away_list = []
        for scorer_raw in away_scorer_raw:
            self.get_scorer_and_times(scorer_raw,away_list)

        #print home_scorer_raw,away_scorer_raw
        return home_list,away_list

    def extract_sub(self,text):
        """
        Extract subs of each team

        @param text: content of html file

        @return: subs of home team and away team        
        """
        home_match = re.search('<div class="tab-section " id="teamlineup-homeTeam">.*?<h4 class="sq-head">Subs</h4>(.*?)</ul>',text,re.DOTALL)
        home_sub = re.findall('<span class="p-name">(.*?)</span>',home_match.group(1))
        away_match = re.search('id="teamlineup-awayTeam">.*?<h4 class="sq-head">Subs</h4>(.*?)</ul>',text,re.DOTALL)
        away_sub = re.findall('<span class="p-name">(.*?)</span>',away_match.group(1))
        return home_sub,away_sub

    def get_scorer_and_times(self,text,scorer_list):
        """
        Updatae the time of goals made by them

        @param text: content of html file
        @param scorer_list: list of scorers
        """
        match = re.match('([A-Z].*)\((.*)\)',text)
        times = re.findall('([0-9]+)(?:\+[0-9])?',match.group(2))
        result = dict()
        result['player'] = match.group(1)
        result['time'] = [int(x) for x in times]
        scorer_list.append(result)
        

if __name__ == '__main__':
    ExtractTeam('../teams_html_files/E0_*')