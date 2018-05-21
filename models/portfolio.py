###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : portfolio.py SQL Alchemy Model
# #########################################

from db import db

class PortfolioModel(db.Model):
    """SQLAlchemy Portfolio Model"""
    
    # We assign the correct table
    __tablename__ = 'portfolios'
    
    # Table columns
    portfolioId = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(300), nullable=False)

    # Foreign key a portfolio belongs to a user
    userId = db.Column(db.Integer, db.ForeignKey('users.userId'), nullable=False)
    
    # Cascade SQL ALCHEMY
    # In order to retrieve all portfolio books relations belonging to one portfolio
    portfolio_books = db.relationship("PortfolioBookModel", cascade="save-update, merge, delete", lazy="dynamic")
    
    # We reference the Parent
    user = db.relationship('UserModel', cascade="save-update")

    def __init__(self, name, userId):
        """Constructor of the Portfolio model
        
        Arguments:
            name {string} -- name of the portfolio
            userId {string} -- id of the parent user
        """

        self.name = name
        self.userId = userId

    def json(self):
        """Return a JSON data of the instance variables"""
        
        return {'portfolioId': self.portfolioId ,'portfolioId' : self.portfolioId ,'name': self.name, 'userId': self.userId, 'Portfolio_Book' : [portfolio_book.json() for portfolio_book in self.portfolio_books.all()]}

    # Important methods used to retrieve data through SQL Alchemy
    @classmethod
    def find_by_name(cls, name):
        """Retrieve the portfolio provided its name"""

        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_by_id(cls, portfolioId):
        """Retrieve the portfolio provided its id"""

        return cls.query.filter_by(portfolioId=portfolioId).first()

    @classmethod
    def find_portfolios_by_user(cls, userId):
        """Retrieve the portfolio provided its userId"""

        return cls.query.filter_by(userId=userId).all()

    def save_to_db(self):
        """Methods used to push and commit to the database"""

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Methods used to delete and commit to the database"""  
              
        db.session.delete(self)
        db.session.commit()
