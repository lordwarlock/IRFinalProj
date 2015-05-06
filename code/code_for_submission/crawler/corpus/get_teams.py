import re,urllib,glob

class GetTeams():
    """
    Retrieve html files from websites containing team information
    """
    def __init__(self,html_dir_pattern = '../extract/html_files/E0_*',
                      out_dir = '../teams_html_files/',
                      url_pattern = '"(http://www1.skysports.com/football/live/match/[0-9]+)'):
        """
        Initialize

        @param html_dir_pattern: pattern of html directories
        @param out_dir: output directories
        """
        self.url_pattern = url_pattern
        self.out_dir = out_dir
        file_dir_list = glob.glob(html_dir_pattern)
        for file_dir in file_dir_list:
            self.get_skysports_teams_for_match(file_dir)

    def get_url(self,html_file):
        """
        Get required url from retrieved html file

        @param html_file: previously retrieved html file

        @return: required url
        """
        with open(html_file,'r') as f_i:
            html_text = f_i.read()
            match_url = re.search(self.url_pattern,html_text)
            if match_url:
                return match_url.group(1)
            else:
                return None

    def get_skysports_teams_for_match(self,html_file = '../extract/html_files/E0_01_01_11_West_Brom'):
        """ 
        Get html containing team information by using retrieved html files 

        @param html_file: directory of previously retrieved html file
        """
        key = self.get_name(html_file)
        skysports_url = self.get_url(html_file) + '/ratings'
        urlobj = urllib.urlopen(skysports_url)
        text = urlobj.read()
        with open(self.out_dir+key,'w') as f_o:
            f_o.write(text)
        print key

    def get_name(self,html_file):
        """
        Get the name of file through directory

        @param html_file: html file directory

        @return: name of file
        """
        match = re.search('.*/(E0_.*)',html_file)
        return match.group(1)

if __name__ == '__main__':
    GetTeams(out_dir = '../ratings_html_files/')
