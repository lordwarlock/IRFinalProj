import re,urllib,glob

class GetTeams():
    def __init__(self,html_dir_pattern = '../extract/html_files/E0_*',
                      out_dir = '../teams_html_files/',
                      url_pattern = '"(http://www1.skysports.com/football/live/match/[0-9]+)'):
        self.url_pattern = url_pattern
        self.out_dir = out_dir
        file_dir_list = glob.glob(html_dir_pattern)
        for file_dir in file_dir_list:
            self.get_skysports_teams_for_match(file_dir)

    def get_url(self,html_file):
        with open(html_file,'r') as f_i:
            html_text = f_i.read()
            match_url = re.search(self.url_pattern,html_text)
            if match_url:
                return match_url.group(1)
            else:
                return None

    def get_skysports_teams_for_match(self,html_file = '../extract/html_files/E0_01_01_11_West_Brom'):
        key = self.get_name(html_file)
        skysports_url = self.get_url(html_file) + '/teams'
        urlobj = urllib.urlopen(skysports_url)
        text = urlobj.read()
        with open(self.out_dir+key,'w') as f_o:
            f_o.write(text)
        print key

    def get_name(self,html_file):
        match = re.search('.*/(E0_.*)',html_file)
        return match.group(1)

if __name__ == '__main__':
    GetTeams()
