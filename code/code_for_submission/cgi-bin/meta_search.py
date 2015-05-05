#!/usr/bin/python

'''
Defines the general behavior that can be used by all cgi search modules.
'''

import unicodedata
import cgi
import cgitb
cgitb.enable()


def receive_data():
    '''
    Receive and return the cgi data from web-page.
    
    @return: the cgi form data from the corresponding web-page
    '''
    
    print 'Content-Type: text/html\n\n'
    
    data = cgi.FieldStorage()
    
    return data


def find_search_result(rst_list, process_each_search_result):
    '''
    According to the search results list, and search result processing method,
    return a search results html string.
   
    @param rst_list: the search results list
    @param process_each_search_result: the method of processing each search result
    
    @return: the search result html string
    '''
    
    # If search miss
    if len(rst_list) == 0:
        return 'Search miss!<br>\n'
    
    rst_string = 'Total search hits number: ' + str(len(rst_list)) + '<br><br>\n'
    
    # Print out top 10 search hits
    for i in range(0, 10):
        if i >= len(rst):
            break
        
        if i % 2 == 0:
            rst_string += '<div class="blog-top">\n'
        
        search_result += process_each_search_result(rst_list[i], i + 1)
        
        if i % 2 == 1:
            search_result += '''
                                <div class="clear"></div>
                            </div>
                             '''
    
    return rst_string
        
        
def html_file_top():
    '''
    Return a html string that corresponds to the search result page's header.
    
    @return: a html string that corresponds to the search result page's header
    '''
    
    return '''
        <html>
            <head>
                <title>Search Result</title>
                <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                <link href="css/style.css" rel="stylesheet" type="text/css" media="all" />
                <link href='http://fonts.googleapis.com/css?family=Raleway' rel='stylesheet' type='text/css'>
                <script src="js/jquery.min.js"></script>
            </head>
            <body>
                <div class="index-banner1">
                    <div class="header-top">    
                        <div class="wrap">
                            <div class="logo">
                                <a href="home.html"><img src="images/another_search.png" alt=""/></a>
                            </div>
                            <div class="clear"></div>        
                        </div>    
                    </div>    
                </div>
                <div class="main">
                    <div class="wrap">
                        <div class="abstract">
                            
        '''
    
    
def html_file_bottom():
    '''
    Return a html string that corresponds to the search result page's footer.
    
    @return: a html string that corresponds to the search result page's footer
    '''
    
    return '''  </body>
            </html>
            '''
    

def write_and_jump(rst_html_str):
    '''
    Write the search result html string into ./soccer_search/result.html file,
    then jump current web-page into the result page (http://localhost:8000/soccer_search/result.html)
    
    @param rst_html_str: the search result html string
    '''
    
    # Write the processed search result html string into ./soccer_search/result.html file
    with open('./soccer_search/result.html', 'w') as html_file:
        html_file.write(html_file_top())
        html_file.write(rst_html_str)
        html_file.write(html_file_bottom())
    
    # Jump current web-page into the result page
    print '''
            <html>
                <meta http-equiv="refresh" content="0.1;url=http://localhost:8000/soccer_search/result.html">
            </html>
          '''