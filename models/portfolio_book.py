###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : portfolio_book.py SQL Alchemy Model
# #########################################

from db import db


class PortfolioBookModel(db.Model):
    """SQLAlchemy PortfolioBook Model"""

    # We assign the correct table
    __tablename__ = 'portfolios_books'
    
    # Table columns
    portfolio_bookId = db.Column(db.Integer, primary_key=True)

    # Foreign key a portfolio_book belongs to a portfolio and a book
    bookId = db.Column(db.Integer, db.ForeignKey('books.bookId'))
    portfolioId = db.Column(db.Integer, db.ForeignKey('portfolios.portfolioId'))

    # We reference the Parents
    book = db.relationship('BookModel', cascade="save-update")
    portfolio = db.relationship('PortfolioModel', cascade="save-update")

    def __init__(self, bookId, portfolioId):
        """Constructor of the PortfolioBook model
        
        Arguments:
            bookId {int} -- id of the book contained in the relation
            portfolioId {int} -- id of the portfolio contained in the relation
        """

        self.bookId = bookId
        self.portfolioId = portfolioId

    def json(self):
        """Return a JSON data of the instance variables"""    

        return {'portfolio_bookId': self.portfolio_bookId ,'bookId': self.bookId, 'portfolioId': self.portfolioId}

    # Important methods used to retrieve data through SQL Alchemy
    @classmethod
    def find_by_portfolio_id(cls, portfolioId):
        """Retrieve thelist of portfolio_book that belong to a specific portfolio provided a portfolioId"""
        
        return cls.query.filter_by(portfolioId=portfolioId).all()

    @classmethod
    def find_by_book_id(cls, bookId):
        """Retrieve the portfolio_book that has a specific bookId"""

        return cls.query.filter_by(bookId=bookId).first()

    @classmethod
    def find_by_portfolio_and_book(cls, portfolioId, bookId):
        """Retrieve the portfolio_book that has a specific bookId and a specific portfolioId"""

        return cls.query.filter_by(portfolioId=portfolioId).filter_by(bookId=bookId).first()

    @classmethod
    def does_this_relation_exists(cls, portfolioId, bookId):
        """Check whether the reltation containing a portfolioId and bookId exists in order to avoir duplicates."""
        
        # Set exists to false
        exists = False
        
        # if we find it we set exist to true.
        if cls.query.filter_by(portfolioId=portfolioId).filter_by(bookId=bookId).first():
            return True
        else:
            return False

    def save_to_db(self):
        """Methods used to push and commit to the database"""
        
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Methods used to delete and commit to the database"""  

        db.session.delete(self)
        db.session.commit()
