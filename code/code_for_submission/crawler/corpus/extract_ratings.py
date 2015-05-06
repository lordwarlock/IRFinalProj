import re,glob

class ExtractRatings():
    """Extract Ratings from html files"""
    def __init__(self,ratings_dir_pattern = None):
        """
        Initialize

        @param ratings_dir_pattern: directory patterns of html files containing rating information
        """
        if ratings_dir_pattern == None:
            pass
        else:
            file_dir_list = glob.glob(ratings_dir_pattern)
            for file_dir in file_dir_list:
                self.process_HTML(file_dir)

    def process_HTML(self,file_dir = '../ratings_html_files/E0_01_04_12_Newcastle',corpus_dict = {}):
        """
        Process html files and extract rating information

        @param file_dir: directory of html file

        @return: ratings of home team and away team
        """
        with open(file_dir,'r') as f_h:
            text = f_h.read()
            key = self.get_name(file_dir)
            tbody_match = re.search('<th class="usr-rate">Your Rating</th>.*?<tbody>(.*?)</tbody>.*?<th class="usr-rate">Your Rating</th>.*?<tbody>(.*?)</tbody>',text,re.DOTALL)
            try:
                home_ratings_raw = tbody_match.group(1)
                away_ratings_raw = tbody_match.group(2)
            except:
                #print '----Error----'
                #print file_dir
                #print '----Error----'
                return [],[]
            corpus_dict[key] = dict()
            corpus_dict[key]['home'] = self.get_player_ratings_raw(home_ratings_raw)
            corpus_dict[key]['away'] = self.get_player_ratings_raw(away_ratings_raw)

            return corpus_dict[key]['home'],corpus_dict[key]['away']

    def get_player_ratings_raw(self,ratings_raw):
        """
        Extract sections of player ratings from html file

        @param ratings_raw: raw html file containing rating information

        @return dictionary containing player ratings
        """
        result_dict = []
        rating_raw_list = re.findall('<tr class=.*?>(.*?)</tr>',ratings_raw,re.DOTALL)
        #print len(rating_raw_list)
        for rating_raw in rating_raw_list:
            result_dict.append(self.get_player_rating(rating_raw))
        return result_dict

    def get_player_rating(self,rating_raw):
        """
        Extract player rating from given raw text

        @param rating_raw: raw texting containg player rating

        @return: return dictionary containing rating information
        """
        result_dict = dict()
        match = re.search('<h5>(.*?)(?:<small>.*</small>)?\s*</h5>\s*<p>(.*?)</p>\s*</td>\s*<td>(?:.*?)</td>.*?<td>([0-9]*\.?[0-9]*)</td>\s*<td class="ss-rate">([0-9]*)</td>',rating_raw,re.DOTALL)

        result_dict["name"] = match.group(1).strip()
        result_dict["comment"] = match.group(2)
        if match.group(3) == '':
            rating = 6
        else:
            rating = int(round(float(match.group(3))))

        result_dict["rate"] = rating
        return result_dict

    def get_name(self,html_file):
        """
        Get file name from directory

        @param html_file: directory of html file

        @return: file name
        """
        match = re.search('.*/(E0_.*)',html_file)
        return match.group(1)


if __name__ == '__main__':
    e=ExtractRatings('../ratings_html_files/E*')

