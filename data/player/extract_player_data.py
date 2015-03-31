'''
Created on Feb 6, 2015

@author: Junchao Kang

"player_corpus_small.txt": the first 100 wiki-page of the corpus, testing data
"palyer_corpus.txt": the full wiki-page corpus, actual data
'''
import json
import re

from wikitools import wiki
from wikitools import category

def build_corpus():
    '''Get wiki-page corpus, write into palyer_corpus.txt'''
    wikiobj = wiki.Wiki('http://en.wikipedia.org/w/api.php')
    wikicat = category.Category(wikiobj, title = 'Premier League players')
    wikipages = wikicat.getAllMembers()
    
    with open('player_corpus.txt', 'w') as corpus_file: 
        for wikipage in wikipages:
            if 'List of' in wikipage.title: # Escape the statistical information page
                continue
            
            # Write wiki-page title
            corpus_file.write('title: ' + wikipage.title.encode('utf-8') + '\n')
            
            # Write wiki-page text
            corpus_file.write(wikipage.getWikiText())
            
            # Write a special line to denote the end of a wiki-page
            corpus_file.write('\n********************************************************************\n')

    
def extract_information(corpus_file):
    '''Extract player's information into a dictionary'''
    rootDict = {}
    currentIntro = '' # Current wiki-page text
    isInInfobox = False
    isInIntro = False
    currentDict = {'name':'', 'height':'', 'birth_year':'', 'position':'', 'birth_place':'', 'intro':''}
    
    for line in corpus_file:    
        line = line.strip()
        if '******************************************' in line: # If reach the end of current wiki-page
            currentDict['intro'] = currentIntro.strip()
            rootDict[currentDict['name']] = currentDict
            currentIntro = ''
            isInInfobox = False
            isInIntro = False
            currentDict = {'name':'', 'height':'', 'birth_year':'', 'position':'', 'birth_place':'', 'intro':''}
        
        elif isInInfobox: # If current line is in infobox           
            if re.search('^}}', line): # If leave the infobox
                isInInfobox = False
            
            elif 'height' in line: # Get height, always in meter
                if re.search(r'[12]\.\d*', line): # If height is given in meter
                    height = re.search(r'[12]\.\d*', line).group()
                    currentDict['height'] = height[:4] # Keep 2 decimals
                    
                elif re.search(r'ft=(\d*)\|in=(\d*)', line): # If height is given in foot & inch
                    foot, inch = int(re.search(r'ft=(\d*)\|in=(\d*)', line).group(1)), int(re.search(r'ft=(\d*)\|in=(\d*)', line).group(2))
                    height = str(foot * 0.3048 + inch * 0.0254)
                    currentDict['height'] = height[:4] # Keep 2 decimals
                    
                
            elif 'birth_date' in line: # Get birth_year
                match = re.search(r'\d{4}', line)
                if match:
                    currentDict['birth_year'] = match.group()
                
            elif 'position' in line: # Get position, split each position by a comma
                position = ''
                for elem in line.split(','):
                    match = re.search(r'\[\[(.*?)\]\]', elem)
                    if match:
                        position += re.sub(r'\W', ' ', match.group(1)) + ','
                        
                currentDict['position'] = position[:-1] # Remove the last comma
            
            elif 'birth_place' in line: # Get birth place, split each level by a comma      
                birth_place = ''
                for elem in line.split(','):
                    match = re.search(r'\[\[(.*?)\]\]', elem)
                    if match:
                        birth_place += match.group(1) + ','
                        
                    elif re.search(r'\w+', elem):
                        birth_place += re.search(r'\w+', elem).group() + ','
                
                birth_place = birth_place.strip()
                if not len(birth_place) == 0:
                    currentDict['birth_place'] = birth_place[:-1] # Remove the last comma
        
        elif re.search(r'^{{infobox', line, re.IGNORECASE): # If entering an infobox
            isInInfobox = True
            isInIntro = True
        
        elif isInIntro:
            if re.search('^==', line): # If reach
                isInIntro = False
                continue
                
            elif ('External link' in line) or ('References' in line):
                continue
            
            # The * at the beginning of the string, denotes this string is not a plain text
            elif re.search(r'^\*', line):
                continue
            
            # Text block should not contain category, infobox, image, external file information
            elif ('Category:' in line) or ('infobox' in line) or ('Image:' in line) or ('File:' in line):
                continue
            
            currentIntro += parse_text(line)
                    
        elif re.search(r'^\{\{.*?\}\}', line): # If current line is a meta-data block
            pass
        
        elif re.search('^title: ', line): # Check name
            s = line.replace('title: ', '')
            currentDict['name'] = s.strip()
    
    return rootDict

        
def clean_up_string(s):
    '''Clean up the input string'''
    s = s.replace('[[', '')
    s = s.replace(']]', '')
    s = s.replace('|', '')
    
    # Remove XML tags
    s = re.sub(r'<.*?>', '', s)
    return s.strip()
        

def parse_text(text):
    '''Process the input wiki-page text'''
    text = clean_up_string(text)
            
    # Remove tags
    text = re.sub(r'(\{{2}.*?\}{2})', '', text)
    text = re.sub(r'[\{\}]', '', text)
    text = re.sub(r'[<>]', '', text)
    text = re.sub('url\text*=', '', text)    
    
    # Remove hyper-links
    text = re.sub(r'https?://.*?\text+', '', text)  
    text = re.sub(r'https?://.*', '', text)
    
    text = text.strip()
    
    if len(text) > 0:
        return text + '\n'
    else:
        return ''

if __name__ == '__main__':
#     build_corpus()
#     print 'Successfully built corpus'
    
    with open('player_corpus.txt', 'rU') as corpus_file:
        rootDict = extract_information(corpus_file)
        
    
    json.dump(rootDict, open('player_extraction.json', 'w')) # Dump the extracted information into a json file
    print 'Successfully extracted information'