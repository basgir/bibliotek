###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : book.py SQL Alchemy Model
# #########################################

from db import db

class BookModel(db.Model):
    """SQLAlchemy Book Model"""

    # We assign the correct table
    __tablename__ = 'books'
    
    # Table columns
    bookId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    publisher = db.Column(db.String(150))
    published_date = db.Column(db.String(15))
    description = db.Column(db.Text())
    isbn10 = db.Column(db.String(20))
    isbn13 = db.Column(db.String(20))
    booktype = db.Column(db.String(30))
    language = db.Column(db.String(30))
    thumbnail = db.Column(db.String(200))
    page_count = db.Column(db.Integer)
    md5 = db.Column(db.String(32))
    url_info = db.Column(db.String(200))
    dl_link1 = db.Column(db.String(200))
    dl_link2 = db.Column(db.String(200))
    chosen_url = db.Column(db.String(200))
    filepath = db.Column(db.String(200))

    # Foreign key a book belongs to a category and an author
    categoryId = db.Column('categoryId', db.Integer, db.ForeignKey('categories.categoryId'))
    authorId = db.Column('authorId', db.Integer, db.ForeignKey('authors.authorId'))

    # We reference the parents
    category = db.relationship('CategoryModel',cascade="save-update")
    author = db.relationship('AuthorModel',cascade="save-update")
    
    # A book might many portfolio book relations
    portfolios_books = db.relationship("PortfolioBookModel", cascade="save-update, merge, delete")

    def __init__(self, title, authorId, categoryId,publisher,published_date,description,isbn10,isbn13,booktype,language,thumbnail,page_count,md5,url_info,dl_link1,dl_link2,chosen_url,filepath):
        """[summary]
        
        Arguments:
            title {string} -- title of the book
            authorId {int} -- id of the author of the book
            categoryId {int} -- id of the category of the book
            publisher {string} -- name of the publisher of the book
            published_date {string} -- publishing date
            description {string} -- description of the book
            isbn10 {string} -- isbn10 of the book
            isbn13 {string} -- isbn13 of the book
            booktype {string} -- type of the book (extension)
            language {string} -- Language of the book
            thumbnail {string} -- Url of the book's thumbnail
            page_count {int} -- Page count of the book
            md5 {string} -- libgen.io identifier
            url_info {string} -- google book api book info url
            dl_link1 {string} -- download link 1
            dl_link2 {string} -- download link 2
            chosen_url {string} -- Chosen url for the download (Whether dl_link1 or dl_link2)
            filepath {string} -- file path where the book is digitally contained
        """
        # Instance variables
        self.title = title
        self.authorId = authorId
        self.categoryId = categoryId
        self.publisher = publisher
        self.published_date = published_date
        self.description = description
        self.isbn10 = isbn10
        self.isbn13 = isbn13
        self.booktype = booktype
        self.language = language
        self.thumbnail = thumbnail
        self.page_count = page_count
        self.md5 = md5
        self.url_info = url_info
        self.dl_link1 = dl_link1
        self.dl_link2 = dl_link2
        self.filepath = filepath
        self.chosen_url = chosen_url

    def json(self):
        """Return a JSON data of the instance variables"""

        return {
                'bookId' : self.bookId,
                'title' : self.title,
                'authorId' : self.authorId,
                'categoryId' : self.categoryId,
                'publisher' : self.publisher,
                'published_date' : self.published_date,
                'description' : self.description,
                'isbn10' : self.isbn10,
                'isbn13' : self.isbn13,
                'booktype' : self.booktype,
                'language' : self.language,
                'thumbnail' : self.thumbnail,
                'page_count' : self.page_count,
                'md5' : self.md5,
                'url_info' : self.url_info,
                'dl_link1' : self.dl_link1,
                'dl_link2' : self.dl_link2,
                'filepath' : self.filepath,
                'chosen_url' : self.chosen_url}

    # Important methods used to retrieve data through SQL Alchemy
    @classmethod
    def find_by_title(cls, title):
        """Retrieve the book provided its title"""
        
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_by_id(cls, bookId):
        """Retrieve the book provided its bookId"""

        return cls.query.filter_by(bookId=bookId).first()

    @classmethod
    def find_by_author_id(cls, authorId):
        """Retrieve the book provided its authorId"""

        return cls.query.filter_by(authorId=authorId).all()
    
    @classmethod
    def find_by_category_id(cls, categoryId):
        """Retrieve the book provided its categoryId"""

        return cls.query.filter_by(categoryId=categoryId).all()

    def save_to_db(self):
        """Methods used to push and commit to the database"""

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Methods used to delete and commit to the database""" 

        db.session.delete(self)
        db.session.commit()
