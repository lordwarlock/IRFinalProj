#!/usr/bin/python

'''
Created on Apr 25, 2015

Defines the general behavior that can be used by club/player/match search

@author: Junchao Kang
'''

import unicodedata
import cgi
import cgitb
cgitb.enable()


def receive_data():
    '''Receive and return web input data'''
    print 'Content-Type: text/html\n\n'
    
    data = cgi.FieldStorage()
    
    return data


def find_search_result(rst, process_each_search_result):
    '''Return the search result in form of html'''
    
    # If search miss
    if len(rst) == 0:
        return 'Search miss!<br>\n'
    
    search_result = 'Total search hits number: ' + str(len(rst)) + '<br><br>\n'
    
    # Print out top 10 search hits
    for i in range(0, 10):
        if i >= len(rst):
            break
        
        if i % 2 == 0:
            search_result += '<div class="blog-top">\n'
        
        search_result += process_each_search_result(rst[i], i + 1)
        
        if i % 2 == 1:
            search_result += '''
                                <div class="clear"></div>
                                </div>\n
                             '''
    
    return search_result
        
        
def html_file_top():
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
                                <a href="index.html"><img src="images/another_search.png" alt=""/></a>
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
    return '''  </body>
            </html>
            '''
    

def write_and_jump(string):
    '''Write search result into ./soccer_search/result.html file; also jump web-page into http://localhost:8000/soccer_search/result.html'''
    
    # Write search result data (in form of html) into ./soccer_search/result.html file
    with open('./soccer_search/result.html', 'w') as html_file:
        html_file.write(html_file_top())
        html_file.write(string)
        html_file.write(html_file_bottom())
    
    # Jump web page into the result page
    print '''
            <html>
                <meta http-equiv="refresh" content="0.1;url=http://localhost:8000/soccer_search/result.html">
            </html>
          '''