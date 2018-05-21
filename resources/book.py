###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : book.py Book Flask_restful resource
# #########################################
from flask_restful import Resource, reqparse
from models.book import BookModel

class Book(Resource):
    """Book. Resource that helps with dealing with Http request for a book by providing its id.
    
    HTTP GET call : /books/<int:id>

    HTTP DELETE call : /books/<int:id>
    
    HTTP PUT call : /books/<int:id>
    """

    # Create the parser for the content of the HTTP request
    parser = reqparse.RequestParser()

    # The parser require some arguments that ifnot fulfilled, return an error
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="Every book needs a title!"
                        )
    parser.add_argument('authorId',
                        type=int,
                        required=True,
                        help="Foreign key of the Author, every book has an author. (FOREIGN KEY)"
                        )
    parser.add_argument('publisher',
                        type=str,
                        required=True,
                        help="Publisher name"
                        )
    parser.add_argument('published_date',
                        type=str,
                        required=False,
                        help="Published date"
                        )
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help="Description of the book"
                        )
    parser.add_argument('isbn10',
                        type=str,
                        required=False,
                        help="type 10 ISBN of the book"
                        )
    parser.add_argument('isbn13',
                        type=str,
                        required=False,
                        help="type 13 ISBN of the book"
                        )
    parser.add_argument('categoryId',
                        type=int,
                        required=True,
                        help="Id of the book's cateogry"
                        )
    parser.add_argument('booktype',
                        type=str,
                        required=True,
                        help="The book extension"
                        )
    parser.add_argument('categoryId',
                        type=int,
                        required=True,
                        help="the category of the book, (FOREIGN KEY)"
                        )
    parser.add_argument('language',
                        type=str,
                        required=True,
                        help="Language of the book"
                        )
    parser.add_argument('thumbnail',
                        type=str,
                        required=False,
                        help="If there is a thumbnail for the book cover"
                        )
    parser.add_argument('page_count',
                        type=int,
                        required=False,
                        help="The book's page count"
                        )
    parser.add_argument('md5',
                        type=str,
                        required=False,
                        help="libgen identifier"
                        )
    parser.add_argument('url_info',
                        type=str,
                        required=False,
                        help="url where you get all the info from google book api"
                        )
    parser.add_argument('dl_link1',
                        type=str,
                        required=False,
                        help="download link number 1"
                        )
    parser.add_argument('dl_link2',
                        type=str,
                        required=False,
                        help="download link number 2"
                        )
    parser.add_argument('chosen_url',
                        type=str,
                        required=False,
                        help="Download link chosen"
                        )
    parser.add_argument('filepath',
                        type=str,
                        required=True,
                        help="Path where the file is stored")
    def get(self, id):
        """GET request that deals with requests that look for a book by id"""

        # Request to the model
        book = BookModel.find_by_id(id)

        # if found
        if book:
            return book.json()

        # if not
        return {'message': 'Book not found'}, 404

    def delete(self, id):
        """DELETE request that deals with the deletion of book given its id"""

        # Request to the model
        book = BookModel.find_by_id(id)

        # if found we delete
        if book:
            book.delete_from_db()
            return {'message': 'Book deleted.'}
        # if not
        return {'message': 'Book not found.'}, 404

    def put(self, id):
        """PUT request that deals with the edition or a creation of a book with at a certain id"""

        # Parse the application/json data
        data = Book.parser.parse_args()

        # Call the model
        book = BookModel.find_by_id(id)
        
        # Update the data to the model
        book = BookModel(**data)

        # If there is an error during the saving. (Foreign keys incorrect)
        try:
            book.save_to_db()
        except:
            return {"message": "There is a problem witht the edition/create of the book. You might want to check that authorId and categoryId do exist."}, 404

        # Return json when all is done.
        return book.json(), 201

class BookTitle(Resource):
    """Book Title. Resource that helps with dealing with Http request for a book by providing its name.
    
    HTTP POST call : /books
    
    HTTP GET call : /books
    """
    def get(self, title):
        """GET request that deals with requests that look for a book by name"""

        # Call the model
        book = BookModel.find_by_title(title)

        # if exists
        if book:
            return book.json()

        # if doesn't
        return {'message': 'Book not found'}, 404

    def delete(self, title):
        """DELETE request that delete a book, provided a name"""

        # Call the model 
        book = BookModel.find_by_title(title)

        # if exists
        if book:
            # then we delete it.
            book.delete_from_db()
            return {'message': 'Book deleted.'}

        # if doesn't
        return {'message': 'Book not found.'}, 404

    def put(self, title):
        """PUT request that edit or create a book, provided a name and data"""
        
        # We parse the arguments
        data = Book.parser.parse_args()

        # Call the model
        book = BookModel.find_by_title(title)
        
        # Update the data to the model
        book = BookModel(**data)

        try:
            # Commit
            book.save_to_db()
        except:
            return {"message":"An error occured. You might want to check whether the foreign keys authorId and categoryId exist"}, 404

        # return the JSON when it's done
        return book.json(), 201


class BookList(Resource):
    """Book List. Resource that contains methods that deal with the creation of new books and the listing of all books
    
    HTTP POST call : /books

    HTTP GET call : /books
    """

    def post(self):
        """POST request create a book, provided a name and data"""

        # We parse the args request
        data = Book.parser.parse_args()

        # Call the model with the title
        if BookModel.find_by_title(data['title']):
            return {'message': "An book with title '{}' already exists.".format(data['title'])}, 400

        # Push the data to the model
        book = BookModel(**data)

        # we try to save into the database
        try:
            book.save_to_db()
        except:
            # If doesn't work for some reason
            return {"message": "An error occurred inserting the book. You might want to check whether authorId and categoryId does exist."}, 500

        # Return the updated book
        return book.json(), 201
    
    def get(self):
        """GET request that returns the list of all the books"""        
        return {'books': list(map(lambda x: x.json(), BookModel.query.all()))}


class BookCategories(Resource):
    """Book Categories. Resource that contains methods that deal the listing of books belonging to a certain category
    
    HTTP GET call : /categories/<int:id>/books
    """

    def get(self, id):
        """GET request that obtain the list of all books contained in a specific category, provided a categoryId""" 

        # Look for all the books contained in a category       
        Book = BookModel.find_by_category_id(id)

        # If found
        if Book:

            # return the list
            return {'Category {}'.format(id) : list(map(lambda x: x.json(), Book))}, 201
        else:
            return {'message': 'The category does not exists or does have no child'}, 404

class BookAuthors(Resource):
    """Book Authors. Resource that contains methods that deal the listing of books belonging to a certain category
    
    HTTP GET call : /authors/<int:id>/books
    """

    def get(self, id):
        """GET request that obtain the list of all books contained in a specific category, provided a categoryId""" 

        # Look for all the books belonging to a specific author      
        Book = BookModel.find_by_author_id(id)
        
        # If found
        if Book:
            # Return the list
            return {'Author {}'.format(id) : list(map(lambda x: x.json(), Book))}, 201
        else:
            # If not found, the author does not exist does not have children
            return {'message': 'The Author does not exists or does have no child'}, 404

class BookSearch(Resource):
    """Book Search. Resource that contains methods that deal the search and scraping of books.
    
    HTTP POST call : /search/book
    """

    def post(self):
        # We do need to instance a new parser, because we do not need all the arguments the class Book has
        parser = reqparse.RequestParser()

        # Add less arguments
        parser.add_argument('title',
                            type=str,
                            required=True,
                            help="Every book needs a title!"
                            )
        parser.add_argument('authors',
                            type=str,
                            required=True,
                            help="Every book has an author."
                            )
        parser.add_argument('isbn',
                            type=str,
                            required=False,
                            help="You might need an isbn"
                            )

        # We parse the args
        data = parser.parse_args()
        
        # if isbn exists we assign it
        if data['isbn']:
            isbn = data['isbn']

        # Else we make it an empty string in case the user did not entered it
        else:
            isbn = ""
        
        # Variable assignment
        title = data['title']
        authors = data['authors']

        # Call the model with the title
        Book = BookModel.find_by_title(data['title'])
        
        # If the book exists then we return the json
        if Book:
            return Book.json(), 201

        # ifnot we scrap it with a subprocess.
        else:

            from subprocess import call

            # Call a subprocess : scrapy crawl books -a title="Introductory Econometrics: A Modern Approach" -a authors="Jeffrey M. Wooldridge"
            call(["scrapy", "crawl", "books", "-a", 'title={}'.format(title), '-a', 'authors={}'.format(authors), '-a', 'isbn={}'.format(isbn) ])

            # Return message
            return {"message": "the book has been fetched and created."}, 201
        
        
        