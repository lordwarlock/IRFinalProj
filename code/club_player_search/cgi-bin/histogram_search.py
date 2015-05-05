#!/usr/bin/python

import unicodedata

import sys
sys.path.append('/Users/apple/Documents/Eclipse_Workspace/IR_final_project') # Different for each machine

import histogram_query
import meta_search


def search(data):
    '''Elastic search the match data, and return the search result'''
    if 'team_name' == data['team_name'].value:
        meta_search.write_and_jump('Input a team name')
        return None
    
    else:
        return data['team_name'].value


def add_image(description, image_addr):
    rst = '<div class="col_1_of_b span_1_of_b">\n'
    
    rst += '<h3>{}</h3>\n'.format(description)
    
    rst += '<img src="{}" alt=""/>'.format(image_addr)
    
    rst += '</div>\n'
    
    return rst


if __name__ == '__main__':
    data = meta_search.receive_data()
    team_name = search(data)
         
    if not team_name == None:
    
        final_rst = ''
        description_list = [team_name, 'a', 'a', 'a', 'a', 'a', 'a', 'a']
        image_list = ['/soccer_search/images/b1.jpg', '/soccer_search/images/b1.jpg', '/soccer_search/images/b1.jpg', '/soccer_search/images/b1.jpg', '/soccer_search/images/b1.jpg', '/soccer_search/images/b1.jpg', '/soccer_search/images/b1.jpg', '/soccer_search/images/b1.jpg'] # list of image addresses
        
        for i in range(0, 8):
            
            if i % 2 == 0:
                final_rst += '<div class="blog-top">\n'
            
            final_rst += add_image(description_list[i], image_list[i])
            
            if i % 2 == 1:
                final_rst += '''
                                    <div class="clear"></div>
                                    </div>\n
                                 '''
                
        meta_search.write_and_jump(final_rst)