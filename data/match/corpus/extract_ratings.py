import re

class ExtractRatings():
    def __init__(self):
        pass

    def process_HTML(self,file_dir = '../ratings_html_files/E0_01_04_12_Newcastle',corpus_dict = {}):
        with open(file_dir,'r') as f_h:
            text = f_h.read()
            key = self.get_name(file_dir)
            tbody_match = re.search('<th class="usr-rate">Your Rating</th>.*?<tbody>(.*?)</tbody>',text,re.DOTALL)
            try:
                ratings_raw = tbody_match.group(1)
            except:
                print '----Error----'
                print file_dir
                print '----Error----'
                return None
            corpus_dict[key] = self.get_player_ratings_raw(ratings_raw)
            print corpus_dict

    def get_player_ratings_raw(self,ratings_raw):
        result_dict = dict()
        rating_raw_list = re.findall('<tr class=.*?>(.*?)</tr>',ratings_raw,re.DOTALL)
        for rating_raw in rating_raw_list:
            self.get_player_rating(rating_raw,result_dict)
        return result_dict

    def get_player_rating(self,rating_raw,result_dict):
        match = re.search('<h5>(.*?)(?:<small>.*</small>)?\s*</h5>\s*<p>(.*?)</p>\s*</td>\s*<td>([0-9]+)</td>.*?<td>([0-9]*)</td>\s*<td class="ss-rate">([0-9]+)</td>',rating_raw,re.DOTALL)
        result_dict[match.group(1).strip()] = dict()
        result_dict[match.group(1).strip()]['comment'] =  match.group(2)
        result_dict[match.group(1).strip()]['fancy'] =  match.group(3)
        result_dict[match.group(1).strip()]['user_rate'] =  match.group(4)
        result_dict[match.group(1).strip()]['ss_rate'] =  match.group(5)

    def get_name(self,html_file):
        match = re.search('.*/(E0_.*)',html_file)
        return match.group(1)


if __name__ == '__main__':
    e=ExtractRatings()
    e.process_HTML()
