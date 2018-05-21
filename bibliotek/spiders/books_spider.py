###########################################
#   Author : Bastien Girardet, Deborah De Wolff, Constant Zurcher, Tomas Prada
#   Date : 26.04.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Goal : Book management system
#   Libraries : scrapy, bibtexparser, datetime, requests
#   API : Google book API
# #########################################
import scrapy
from scrapy.crawler import CrawlerProcess
from bibliotek import settings
from scrapy.http import Request
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibliotek.items import Book
from bibliotek.book_info import BookInfo
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
from pathlib import Path
from slugify import slugify
import urllib
import json
import re
import requests
import os

###########################################
#   Class : BooksSpider
#   Goal : Built on scrapy library, is required to crawl data on websites.
#   Each scraped Book Data is then store into an item (items.py) => (Book).
#   Each item is then processed through an item pipeline (pipelines.py)
#   Example-cli : scrapy crawl books -a title=
# #########################################
class BooksSpider(scrapy.Spider):
    # Global variable 
    # Name is required by scrapy
    name = "books"
    def __init__(self, extension="pdf",isbn="", title="", authors = "", *args, **kwargs):
        """Constructor of the BooksSpider scrapy class. Scrap the desired book and download it as pdf.
        
        Keyword Arguments:
            extension {str} -- type of the book we want (default: {"pdf"})
            isbn {str} -- isbn of the book (default: {""})
            title {str} -- title of the book (default: {"Introductory Econometrics: A Modern Approach"})
            authors {str} -- authors of the book (default: {"Jeffrey M. Wooldridge"})
        """

        super(BooksSpider, self).__init__(*args, **kwargs)

        # Because making a mistake while spelling is super easy to do,
        # first we look for the book on google book api then after having fetched correct informations about it,
        # we do make the request on libgen.io
        self.bookPreview = BookInfo(isbn, title, authors)
        self.logger.info("GOOGLE API : {}".format(self.bookPreview.url_request))

        # Build request
        request = "{0} {1}".format(self.bookPreview.get_title().split(",")[0],self.bookPreview.get_authors()[0])
        request = request.replace(" ", "+")

        # Build starting urls
        self.start_urls = [
            'http://libgen.io/search.php?req={}&open=0&res=25&view=simple&phrase=1&column=def'.format(request)
        ]

        # 'http://libgen.pw/search?q={}'.format(request)
        # Choose what extension the book will be downloaded in
        self.extension = extension
        
        # Number of query ( Number of book searched with the same name )
        self.query_number = 2

        # Authors name
        self.authors = self.bookPreview.get_authors()[0]

        # Book title
        self.title = self.bookPreview.get_title()

        # Subtitle
        self.subtitle = self.bookPreview.get_subtitle()

        # Logging all information about book best match
        self.logger.info("Cumulative ratio : {0}".format(self.bookPreview.get_cumulative_ratio()))
        self.logger.info("Number of best match found :{0}".format(self.bookPreview.top_books_number))
        self.logger.info("Book selected :{0}".format(self.bookPreview.selected))

        # Log to be sure that arguments passed correclty
        self.logger.info("authors : {0}\ttitle : {1}\tsubtitle : {2}".format(self.authors,  self.title, self.subtitle))
        self.logger.info("start_url : {0}".format(self.start_urls[0]))

    def parse(self, response):
        """
        First method that Go throught the given start_urls and for each url it parses it
        
        Arguments:
            response {scrapy.response} -- scrapy response
        """

        # Initiate a scrapper for each URL contained in start_urls
        for url in self.start_urls:
            yield response.follow(url, self.parse_item)

    def parse_item(self, response):
        """
        Go throught the given start_urls and for each url it parses it
        
        Arguments:
            response {scrapy.response} -- scrapy response
        """

        self.logger.info('You just got on parse_item : {0}'.format(response.url))

        # Iterators
        query = 1

        # In order to 
        book_list = []

        try:
            # Select the table that contains all the data
            table = response.css(".c")

            # Extract the relevant elements from the page
            # Go through each tr
            for row in table.css('tr'):           
                book_id = row.xpath("./td[1]/text()").extract_first()            
                authors = row.xpath("./td[2]").css('a:nth-child(1)::text').extract_first()
                title = row.xpath("./td[3]/a[@id='{0}']/text()".format(book_id)).extract_first()
                publisher = row.xpath("./td[4]/text()").extract_first()
                published_date = row.xpath("./td[5]/text()").extract_first()
                page_count = row.xpath("./td[6]/text()").extract_first()
                language = row.xpath("./td[7]/text()").extract_first()
                size = row.xpath("./td[8]/text()").extract_first()
                extension = row.xpath("./td[9]/text()").extract_first()
                download_link_1 = row.xpath("./td[10]").css('a:nth-child(1)::attr(href)').extract_first()
                download_link_2 = row.xpath("./td[11]").css('a:nth-child(1)::attr(href)').extract_first()
                download_link_3 = row.xpath("./td[12]").css('a:nth-child(1)::attr(href)').extract_first()
                download_link_4 = row.xpath("./td[13]").css('a:nth-child(1)::attr(href)').extract_first()
                try:
                    cumulative_ratio = round((fuzz.ratio(title,self.title)+fuzz.ratio(authors,self.authors))/2,2)
                except:
                    cumulative_ratio = 0
                book_info_temp = {}
                book_info_temp.update({'index':query,
                'title':title,
                'authors':authors,
                'publisher': publisher,
                'published_date': published_date,
                'page_count': page_count,
                'language': language,
                'size': size,
                'extension': extension,
                'download_link_1':download_link_1,
                'download_link_2':download_link_2,
                'download_link_3':download_link_3,
                'download_link_4':download_link_4,
                'cumulative_ratio':cumulative_ratio})
                book_list.append(book_info_temp)
        

            # Create the Dataframe of all the list of books
            df = pd.DataFrame(book_list)
            # Remove the first one since it's not a book but the header of the website
            df = df[1:]

            # Select only the one that respect the extension criteria
            df = df.loc[df['extension'] == self.extension]

            # sort by cumulative ratio and select the book best match
            best_match = df.sort_values(by='cumulative_ratio',ascending=False).iloc[0]

            # Show the book best match debug purpose
            print(best_match)
            
            #We select the url that goes on libgen.io
            dl_link = best_match['download_link_2']

            # We are scraping only libgen.io
            if dl_link is not None:
                request = Request(
                    url=response.urljoin(dl_link),
                    callback=self.parse_books_libgen
                )
                request.meta['authors'] = best_match['authors']
                request.meta['title'] = best_match['title']
                request.meta['dl_link1'] = best_match['download_link_1']
                request.meta['dl_link2'] = best_match['download_link_2']
                request.meta['chosen_url'] = "dl_link2"
            yield request
        except:
            print("="*150)
            print("Error while parsing data, the website might give back no entries. Check out Title, authors and ISBN")
            print("="*150)
            

    def parse_books_libgen(self, response):
        """
        Parse the items on the second page of libgen.io
        Once the download link and the bibtex have been parsed,
        The save_pdf method is called.
        
        Arguments:
            response {scrapy.response} -- scrapy response
        """

        # Select the download column
        download_column = response.css('td')[2]

        # Get the final download URL
        download_url = download_column.css('a:nth-child(1)::attr(href)').extract_first()

        # Parse the information in bibtex
        bibtex_raw = response.xpath('//*[@id="bibtext"]/text()').extract_first()
        bibtex_processed = self.bibtex_reader(bibtex_raw)
        
        self.logger.info("authors : {0} \t Title : {1}".format(self.authors, self.title))
        self.logger.info("Bibtex : {}".format(bibtex_processed))
        self.logger.info('You just got on page 2 on libgen.io : {0}'.format(response.urljoin(download_url)))
        request = Request(
            url = response.urljoin(download_url),
            callback = self.save
        )
        request.meta['url'] = download_url
        if hasattr(bibtex_processed, 'md5'):
            request.meta['md5'] = bibtex_processed['md5']
        else:
            request.meta['md5'] = ""
        request.meta['dl_link1'] = response.meta['dl_link1']
        request.meta['dl_link2'] = response.meta['dl_link2']
        request.meta['chosen_url'] = response.meta['chosen_url']
        yield request

    def save(self, response):
        """
        Download the file as a pdf and call the model to save the data into the database.
        
        Arguments:
            response {scrapy.response} -- scrapy response
        """

        # Create a book Item and store all variables
        book = Book()        

        # Getting back the book info that we precedently got from Google Book API
        bookInfo = self.bookPreview

        ###############################################################################
        # Assign all the google book api data to the Book Item
        # This solution swap the data provided by libgen with the google book api data
        # We assume that Google api data is cleaner
        ###############################################################################

        # logging the process
        self.logger.info("Saving the book info as an Item.")

        # Data
        book['title'] = self.formatString(bookInfo.get_title())

        # We need to check if the author exists and we return its id if he exists ifnot he is created, more details on him are fetched on wikipedia and the id is returned
        author_name = self.formatString(''.join(bookInfo.get_authors()))
        book['authorId'] = int(checkAuthor(bookInfo.get_author()))

        book['publisher'] = self.formatString(bookInfo.get_publisher())
        book['published_date'] = self.formatString(bookInfo.get_published_date())
        book['description'] = self.formatString(bookInfo.get_description())
        book['isbn10'] = self.formatString(bookInfo.get_isbn10())
        book['isbn13'] = self.formatString(bookInfo.get_isbn13())

        # WE need to check if the author exists and we return its id if he exists ifnot he is created and the id is returned
        category_name = self.formatString(''.join(bookInfo.get_categories()))
        book['categoryId'] = int(checkCategory(category_name))

        book['language'] = self.formatString(bookInfo.get_language())
        book['thumbnail'] = self.formatString(bookInfo.get_thumbnail())
        book['page_count'] = int(bookInfo.get_page_count())
        book['url_info'] = self.formatString(bookInfo.get_url_info())


        # Creating the filepath
        filename = slugify(book['title'])
        filename = "{0}.{1}".format(filename,self.extension)
        authorsfilepath = slugify(author_name)

        if not os.path.exists("{0}/{1}".format(settings.FILES_STORE,authorsfilepath)):
            os.makedirs("{0}/{1}".format(settings.FILES_STORE,authorsfilepath))

        path = "{0}/{1}/{2}".format(settings.FILES_STORE,authorsfilepath,filename)
        with open(path, 'wb') as f:
            f.write(response.body)
        self.logger.info("Saved PDF as  : {0}".format(path))

        ###############################################################################
        # The only data that cannot be retrieved on google book api is here
        ###############################################################################
        book['booktype'] = self.extension

        # If there exist an md5 (Hashed ID from libgen.io)
        if hasattr(response.meta, 'md5'):
            if response.meta['md5'] is not None:
                book['md5'] = response.meta['md5']
        else:
            book['md5'] = "NaN"

        # We assign the link of the first two download link
        if response.meta['dl_link1'] is not None:
            book['dl_link1']= response.meta['dl_link1']
        else:
            book['dl_link1'] = "NaN"
        if response.meta['dl_link2'] is not None:
            book['dl_link2']= response.meta['dl_link2']
        else:
            book['dl_link2'] = "NaN"
        
        # Assign the Download URL that we used
        if response.meta['chosen_url'] is not None:
            book['chosen_url']= response.meta['chosen_url']
        else:
            book['chosen_url'] = ""
    
        # If the path is not 
        if path is not None:
            book['filepath'] = path
        else:
            book['filepath'] = ""    
        
        yield book

    def bibtex_reader(self, bibtextdata):
        """
        Parse the bibtex data
        
        Arguments:
            bibtextdata {str} -- bibtexdata
        
        Returns:
            list -- list of all entries of the bibtex
        """
        parser = BibTexParser()
        parser.ignore_nonstandard_types = False
        parser.homogenise_fields = False
        parser.common_strings = False
        bib_database = bibtexparser.loads(bibtextdata, parser)
        return bib_database.entries[0]
    
    def formatString(self, string):
        """
        format the string into something updatable to the db, usefull especially for the description that might contain weird charachters
        
        Arguments:
            string {str} -- string to format
        
        Returns:
            str -- formatted string
        """
        string = string.replace("'","\'")
        # string = string.replace(":","")
        string = string.replace(",","")
        return string

def checkAuthor(author):
    """
    check whether the author is already registered in the database, ifnot, additional information about him is fetched from wikipedia (if possible)
    then the author is saved in the databse.

    Arguments:
        author {string} -- author name
    
    Returns:
        int -- authorId of the database
    """
    # headers in order to make the HTTP request
    headers = {'Content-Type': 'application/json'}

    # Request builder
    url_author = "http://127.0.0.1:5000/authors/name/{}".format(urllib.parse.quote(author))

    # We make the request
    response_author = requests.request("GET", url_author, headers=headers)

    # If the user already exists we user the existing data
    if response_author.status_code == 200:
        print("Author already exists...") 
        print("Author ID :{}".format((response_author.json()['authorId'])))
        print(response_author.text)
        return response_author.json()['authorId']

    # else we create it and fetch its information on wikipedia if there is any
    else:
        print("Creating author...")
        try:
            import wikipedia
            authors_search = wikipedia.search(author)
            print("Search : {}".format(authors_search))
            author_wiki = wikipedia.page(authors_search[0])

            # if authors has images on wikiepdia
            try:
                img = author_wiki.images[0]
            except:
                img = ""

            # we assign the variables that wikipedia gave us               
            url = author_wiki.url
            author_name = author_wiki.title
            description = author_wiki.content.split(".")[0]

        except:
            # we assign the variables
            print("Author is not on wikipedia. Creating it without other field.")
            author_name = author
            url = ""
            img = ""
            description = ""
        
        # formatted json response
        author_json = {
            "name": author_name,
            "description": description,
            "image_url": img,
            "wiki_url": url
        }
        
        # we push it to the Flask API
        url_author_post = "http://127.0.0.1:5000/authors"
        response = requests.request("POST", url_author_post, data=json.dumps(author_json, ensure_ascii=False).encode('utf8'), headers=headers)

        # If correctly created
        if response.status_code == 201:
            print("Author created.")
        else:
            print("HTTP CODE : {}".format(response.status_code))

        print("Author ID :{}".format(response.json()['authorId']))

        # We return the author Id that has been created or fetched
        return response.json()['authorId']

def checkCategory(category):
    """
    checkCategory is here to see if there is any category of the same name in the database by using a GET HTTP REQUEST
    and if there isn't the category will be created and its ID returned.
    
    Arguments:
        category {string} -- Name of the category
    
    Returns:
        int -- Return the category ID
    """
    
    # Required headers for the HTTP request
    headers = {'Content-Type': 'application/json'}

    # URL for the Request on categories
    url_category = "http://127.0.0.1:5000/categories/name/{}".format(urllib.parse.quote(category))

    # We make the request
    response_category = requests.request("GET", url_category, headers=headers)

    # if exists
    if response_category.status_code == 200:
        print("Category already exists...")    
        print("Category ID :{}".format(response_category.json()['categoryId']))
        return response_category.json()['categoryId']

    # else we create the category
    else:
        print("Creating category...")

        # Formatted JSON response
        category_json = {
            "name": category
        }

        # Post request to insert the cat
        url_category_post = "http://127.0.0.1:5000/categories"

        # We make the request
        response = requests.request("POST", url_category_post, data=json.dumps(category_json, ensure_ascii=False).encode('utf8'), headers=headers)
        
        # If correctly saved
        if response.status_code == 201:
            print("Category '{}' correctly saved into to the database".format(category))
        else:
            print("HTTP ERROR CODE : {}".format(response.status_code))
        
        # We print logs
        print(response.json()['categoryId'])
        print("Category created.")
        print("Category ID :{}".format(response.json()['categoryId']))

        # We return the categoryId that has been created or fetched
        return response.json()['categoryId']