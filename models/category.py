###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : category.py SQL Alchemy Model
# #########################################

from db import db


class CategoryModel(db.Model):
    """SQLAlchemy Portfolio Model"""

    # We assign the correct table
    __tablename__ = 'categories'
    
    # Table columns
    categoryId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))

    # In order to retrieve all books relations belonging to one category
    books = db.relationship("BookModel", cascade="save-update, merge, delete", lazy='dynamic')
    

    def __init__(self, name):
        """Constructor of the Portfolio model
        
        Arguments:
            name {string} -- name of the category
        """

        self.name = name

    def json(self):
        """Return a JSON data of the instance variables"""    

        return {'categoryId': self.categoryId , 'name': self.name, 'books' : [book.json() for book in self.books.all()]}

    # Important methods used to retrieve data through SQL Alchemy
    @classmethod
    def find_by_id(cls, id):
        """Retrieve the category provided its id"""
        
        return cls.query.filter_by(categoryId=id).first()
    
    @classmethod
    def find_by_name(cls, name):
        """Retrieve the category provided its name"""
        
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        """Methods used to push and commit to the database"""
        
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):

        """Methods used to delete and commit to the database"""  
        db.session.delete(self)
        db.session.commit()
