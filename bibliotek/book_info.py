###########################################
#   Author : Bastien Girardet, Deborah De Wolff, Constant Zurcher, Tominhas Prada Schneider
#   Date : 26.04.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Classname : BookInfo
#   Goal of the class : fetch all the data from google API provided a ISBN and a title.
#   Most of the time the data provided by google is more accurate than libgen.
# #########################################
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests
import urllib
import pandas as pd
import numpy as np

class BookInfo():
    """Provided a title, one or many authors (one preferred) and an ISBN (Optional), it looks for the google book api best match.
    Once found, it stores the data in instance variables.

    Args:
        isbn: isbn of the book may be left blank
        title: title of the book
        authors: authors of the book

    Attributes:
        arguments (str): Arguments passed to the HTTP GET request, usually contains title, authors and isbn
        url_request (str): Url of the request made
        json_response_raw (json): json response from HTTP GET request
        totalItems (int): number of item returned
        success (boolean): If found best match
        top_books (json): json of all the top matched books
        top_books_number (json): json of all the top matched books
        df_book_list (np.DataFrame): Dataframe of all the books found
        book_best_match (np.array): Array of the book best match
        title (str): title of the book_best_match
        authors (str): authors of the book_best_match
        publisher (str): publisher of the book_best_match
        published_date (str): published_date of the book_best_match
        description (str): description of the book_best_match
        isbn10 (int): isbn10 of the book_best_match
        isbn13 (int): isbn13 of the book_best_match
        categories (str): categories of the book_best_match
        thumbnail (str): thumbnail of the book_best_match
        language (str): language of the book_best_match
        page_count (int): page_count of the book_best_match
        url_info (str): url_info of the book_best_match
        cumulative_ratio (float): cumulative_ratio of the book_best_match
    """
    def __init__(self, isbn="", title="The intelligent Investor", authors="Benjamin Graham"):
        """Constructor of BookInfo class
        
        Keyword Arguments:
            isbn {str} -- isbn of the book (default: {""})
            title {str} -- title of the book (default: {"The intelligent Investor"})
            authors {str} -- authors of the book (default: {"Benjamin Graham"})
        """

        # format title
        self.arguments = urllib.parse.urlencode({'title':title,
        'authors':authors,
        'isbn' : isbn})

        # URL FROM GOOGLE API V.1 (OPEN API)
        url = 'https://www.googleapis.com/books/v1/volumes?q={0}'.format(self.arguments)

        self.url_request = url

        # LOG the first fetched URL
        print("GOOGLE BOOK API URL REQUEST : {0}".format(url))

        # Call the HTTP request on the URL
        request = requests.get(url)

        # Ask for a JSON
        self.json_response_raw = request.json()

        self.totalItems = self.json_response_raw['totalItems']

        # Initialize success to zero
        self.success = False

        # If there is a book at least
        if self.totalItems > 0:
            self.success = False
            # Select the top books
            self.top_books = self.json_response_raw['items']
            self.top_books_number = len(self.top_books)
            print("Number of book : {0}".format(self.top_books_number))

            book_list = []
            book_iterator = 1
            self.selected = None
            # Go through each book to compute accuracy check
            for book in self.top_books:

                # Assign title
                try:
                    title_google = book['volumeInfo']['title']
                    authors_google = book['volumeInfo']['authors']
                except:
                    continue
                #If there exist a subtitle we test the subtitle with the given title from the user,
                # because we do not know whether there is a subitle for each book
                try:
                    subtitle = book['volumeInfo']['subtitle']

                    # Assign its value to the class attributes
                    lev_ratio_subtitle = fuzz.ratio(title,subtitle)/100

                # In the case that there is no subtitle, the condition for passing void 
                # and subtitle is NaN     
                except:
                    subtitle = ""
                    lev_ratio_subtitle = None
                    
                # Compute ratios for title and authors
                lev_ratio_title = fuzz.ratio(title,title_google)/100
                lev_ratio_authors = fuzz.ratio(authors,authors_google[0])/100
                
                ##############################################
                # Conditions for string matching
                ##############################################
            
                if subtitle is not "":
                    # Condition 1 : If the fuzzy subtitle ratio is above 60% There is high chances to be the right book
                    # because, there is not always a subtitle
                    condition1 = lev_ratio_title > .7 and lev_ratio_subtitle > .6
                    # Condition 2 : If all ratios are above 50% This is highly probable that we have the right book
                    condition2 = lev_ratio_title > .6 and lev_ratio_authors > .6 and lev_ratio_subtitle > .5
                    # Condition 4 : If the subtitle exists and is above 75% there is high chance for the book to be the one.
                    condition4 = lev_ratio_subtitle > .75
                else:
                    # Condition 1 : Is set to false, since there is no subtitle
                    condition1 = lev_ratio_title > .8

                    # Condition 2 : Since there is no subtitle, condition 3 and 4 are similar.
                    condition2 = False

                    # Condition 4 : condition4 is set to false since subtitle doesn't exists                    
                    condition4 = False
                    
                # Condition 3 : If the fuzzy authors ratio as well as the fuzzy ratio title are above 65% There is hich chances that the book is the right one
                condition3 = lev_ratio_title > .6 and lev_ratio_authors > .7

                # Compute cumulative ratio
                if subtitle is not "":
                    # If there exists a subtitle, sum up all three levenstein ratios and divide it by the number of ratios
                    cumulative_ratio = round((lev_ratio_title+lev_ratio_authors+lev_ratio_subtitle)/3,2)
                else:
                    # Ifnot the same as before but without the subtitle ratio.
                    cumulative_ratio = round((lev_ratio_title+lev_ratio_authors)/2,2)

                #For DEBUGGING purpose
                print("="*98)
                print("Book N°{0}\t| lev Ratio\t | Cond 1 \t | Cond 2 \t | Cond 3 \t | Cond 4 \t |".format(book_iterator))
                print("-"*98)
                print("Title     \t|       {0}\t |     {1}\t |     {2}\t |     {3}\t |     {4}\t |".format(lev_ratio_title,condition1, condition2, condition3, condition4))
                print("Subtitle  \t|       {0}\t |     {1}\t |     {2}\t |     {3}\t |     {4}\t |".format(lev_ratio_subtitle,condition1, condition2, condition3, condition4))
                print("Authors   \t|       {0}\t |     {1}\t |     {2}\t |     {3}\t |     {4}\t |".format(lev_ratio_authors,condition1, condition2, condition3, condition4))
                print("Cumulative\t|       {0}\t |     {1}\t |     {2}\t |     {3}\t |     {4}\t |".format(cumulative_ratio,cumulative_ratio, cumulative_ratio, cumulative_ratio, condition4))

                # Set the rest of the attributes by trying if they exists and ifnot assign an NaN        
                # publisher
                try:
                    publisher = book['volumeInfo']['publisher']
                except:
                    publisher = "NaN"

                # Published_date
                try:
                    published_date = book['volumeInfo']['publishedDate']
                except:
                    published_date = "NaN"

                # Description
                try:
                    description = book['volumeInfo']['description']
                except:
                    description = "NaN"

                # ISBNS
                try:
                    if hasattr(book['volumeInfo']['industryIdentifiers'][0], "ISBN_10"):
                        isbn10 = book['volumeInfo']['industryIdentifiers'][0]['identifier']
                        isbn13 = book['volumeInfo']['industryIdentifiers'][1]['identifier']  
                    else:
                        isbn13 = book['volumeInfo']['industryIdentifiers'][0]['identifier']
                        isbn10 = book['volumeInfo']['industryIdentifiers'][1]['identifier'] 
                except:
                    isbn13 = "NaN"
                    isbn10 = "NaN"
                
                # Categories
                try:
                    categories = book['volumeInfo']['categories']
                except:
                    categories = "NaN"
                
                # Thumbnail
                try:
                    thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
                except:
                    thumbnail = "NaN"
                
                # Language
                try:
                    language = book['volumeInfo']['language']
                except:
                    language = "NaN"

                # Page Count
                try:
                    page_count = book['volumeInfo']['pageCount']
                except:
                    page_count = 0
                
                # Link where to obtain book info
                try:
                    url_info = book['selfLink']
                except:
                    url_info = "NaN"

                book_info_temp = {}
                book_info_temp.update({'index':book_iterator-1,
                'title':title_google,
                'subtitle':subtitle,
                'authors':authors_google,
                'publisher': publisher,
                'published_date': published_date,
                'description': description,
                'isbn10': isbn10,
                'isbn13': isbn13,
                'categories': categories,
                'thumbnail': thumbnail,
                'language': language,
                'page_count': page_count,
                'url_info': url_info,
                'lev_ratio_title':lev_ratio_title,
                'lev_ratio_authors':lev_ratio_authors,
                'lev_ratio_subtitle':lev_ratio_subtitle,
                'cumulative_ratio':cumulative_ratio,
                'condition1': condition1,
                'condition2': condition2,
                'condition3': condition3,
                'condition4': condition4})
                book_list.append(book_info_temp)
                book_iterator += 1

            self.df_book_list = pd.DataFrame(book_list)
            
            # CHoose the most accurate book depending on its cumulative ratio
            self.book_best_match = self.df_book_list.sort_values(by=['cumulative_ratio'],ascending=False).iloc[0]

            # If book has subtitle that match the title of about 75% you know that's the right book so we pass it as success 
            if self.book_best_match['condition4'] :
                self.success = True

            # Condition 1 with the title 
            if self.book_best_match['condition1'] :
                self.success = True
            
            #
            if self.book_best_match['condition2'] :
                self.success = True
            
            if self.book_best_match['condition3'] :
                self.success = True

            # If no book has been found
            if not self.success:
                print("No corresponding book was found, check title and authors spelling")
                print("Most accurate found and selected is :")
                print(self.book_best_match)
            else:
                print("Selected book number : {0}".format(self.book_best_match['index']))
                print(self.book_best_match)

            self.title = self.book_best_match['title']
            self.authors = self.book_best_match['authors']
            self.subtitle = self.book_best_match['subtitle']
            self.publisher = self.book_best_match['publisher']
            self.published_date = self.book_best_match['published_date']
            self.description = self.book_best_match['description']
            self.isbn10 = self.book_best_match['isbn10']
            self.isbn13 = self.book_best_match['isbn13']
            self.categories = self.book_best_match['categories']
            self.thumbnail = self.book_best_match['thumbnail']
            self.language = self.book_best_match['language']
            self.page_count = self.book_best_match['page_count']
            self.url_info = self.book_best_match['url_info']
            self.cumulative_ratio = self.book_best_match['cumulative_ratio']
            

    def showInfo(self):
        """Return all the instance variables."""
        if self.totalItems >0:
            print("title :{}".format(self.title))
            print("authors :{}".format(self.authors))
            print("publisher :{}".format(self.publisher))
            print("published_date :{}".format(self.published_date))
            print("description :{}".format(self.description))
            print("isbn10 :{}".format(self.isbn10))
            print("isbn13 :{}".format(self.isbn13))
            print("categories :{}".format(self.categories))
            print("thumbnail :{}".format(self.thumbnail))
            print("language :{}".format(self.language))
            print("page_count :{}".format(self.page_count))
            print("url_info :{}".format(self.url_info))
            print("cumulative_ratio :{}".format(self.cumulative_ratio))
        else:
            print("ERROR - 404 NOT FOUND")

    ###################
    #  Getter : title
    ###################
    def get_title(self):
        return self.title

    ###################
    #  Setter : title
    ###################
    def set_title(self, title):
        self.title = title
    
    ###################
    #  Getter : subtitle
    ###################
    def get_subtitle(self):
        return self.subtitle

    ###################
    #  Setter : subtitle
    ###################
    def set_subtitle(self, subtitle):
        self.subtitle = subtitle

    ###################
    #  Getter : authors
    ###################
    def get_authors(self):
        return self.authors

    ###################
    #  Getter : author
    ###################
    def get_author(self):
        return self.authors[0]

    ###################
    #  Setter : authors
    ###################
    def set_authors(self, authors):
        self.authors = authors
        
    ###################
    #  Getter : publisher
    ###################
    def get_publisher(self):
        return self.publisher

    ###################
    #  Setter : publisher
    ###################
    def set_publisher(self, publisher):
        self.publisher = publisher
        
    ###################
    #  Getter : published_date
    ###################
    def get_published_date(self):
        return self.published_date

    ###################
    #  Setter : published_date
    ###################
    def set_published_date(self, published_date):
        self.published_date = published_date
        
    ###################
    #  Getter : description
    ###################
    def get_description(self):
        return self.description

    ###################
    #  Setter : description
    ###################
    def set_description(self, description):
        self.description = description
        
    ###################
    #  Getter : isbn10
    ###################
    def get_isbn10(self):
        return self.isbn10

    ###################
    #  Setter : isbn10
    ###################
    def set_isbn10(self, isbn10):
        self.isbn10 = isbn10
        
    ###################
    #  Getter : isbn13
    ###################
    def get_isbn13(self):
        return self.isbn13

    ###################
    #  Setter : isbn13
    ###################
    def set_isbn13(self, isbn13):
        self.isbn13 = isbn13
        
    ###################
    #  Getter : categories
    ###################
    def get_categories(self):
        return self.categories

    ###################
    #  Setter : categories
    ###################
    def set_categories(self, categories):
        self.categories = categories
        
    ###################
    #  Getter : thumbnail
    ###################
    def get_thumbnail(self):
        return self.thumbnail

    ###################
    #  Setter : thumbnail
    ###################
    def set_thumbnail(self, thumbnail):
        self.thumbnail = thumbnail
        
    ###################
    #  Getter : language
    ###################
    def get_language(self):
        return self.language

    ###################
    #  Setter : language
    ###################
    def set_language(self, language):
        self.language = language
        
    ###################
    #  Getter : page_count
    ###################
    def get_page_count(self):
        return self.page_count

    ###################
    #  Setter : page_count
    ###################
    def set_page_count(self, page_count):
        self.page_count = page_count
        
    ###################
    #  Getter : url_info
    ###################
    def get_url_info(self):
        return self.url_info

    ###################
    #  Setter : url_info
    ###################
    def set_url_info(self, url_info):
        self.url_info = url_info

    ###################
    #  Getter : cumulative_ratio
    ###################
    def get_cumulative_ratio(self):
        return self.cumulative_ratio

    ###################
    #  Setter : cumulative_ratio
    ###################
    def set_cumulative_ratio(self, cumulative_ratio):
        self.cumulative_ratio = cumulative_ratio