import requests
from bs4 import BeautifulSoup
import string
from time import sleep
#get pages
#http://crosswordtracker.com/browse/answers-starting-with-a/?page=1 example page
#http://crosswordtracker.com/browse/answers-starting-with-a/?page=2
alpha = string.ascii_lowercase
#print(alpha)

for letter in alpha:
    #put everything in here
    url = 'http://crosswordtracker.com/browse/answers-starting-with-' + letter 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    #the last one is the » sign
    num_pages = soup.find_all('div',class_ = 'paginator')[-2].get_text()
    for index in range(1, int(num_pages)+1):
        url_index = url + '/?page=' + str(index)
        print(url_index)
        #search each url index for that's in the href
        #open that page
        # <a class='answer' href='/answer/volgariver/'>VOLGARIVER</a>
        page_index = requests.get(url_index)
        soup_index = BeautifulSoup(page_index.content, 'html.parser')
        
        for page_ans in soup_index.find_all('a', class_ ='answer'):
            file_name = 'crossword_answers_clues_' + letter + '.txt'
            text_file = open(file_name, 'a')
            answer = page_ans.text
            url_answer = 'http://crosswordtracker.com' + page_ans['href']
            print(url_answer)
            print(answer)
            url_answer_page = requests.get(url_answer)
            soup_answer_page = BeautifulSoup(url_answer_page.content, 'html.parser')
            clues_results = soup_answer_page.find('ul', class_ = 'clue-list')
            text_file.write(answer + '-' + clues_results.get_text('||').strip() + '\n')
            #if I don't sleep often enough something about my router has issues
            #note this takes quite a while given that there's probably around 80*40 words PER LETTER of alphabet
            sleep(.2)