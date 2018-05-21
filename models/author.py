###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : author.py SQL Alchemy Model
# #########################################
from db import db

class AuthorModel(db.Model):
    """SQLAlchemy Author Model"""

    # We assign the correct table
    __tablename__ = 'authors'
    
    # Table columns
    authorId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(500))
    image_url = db.Column(db.String(200))
    wiki_url = db.Column(db.String(200))
    
    # Children relationship in order to retrieve of all the author's books
    books = db.relationship("BookModel", cascade="save-update, merge, delete", lazy='dynamic')

    def __init__(self, name, description, image_url,wiki_url):
        """Constructor of the Author model
        
        Arguments:
            name {string} -- name of the author
            description {string} -- description of the author
            image_url {string} -- image url of the author 
            wiki_url {string} -- author wikipedia page url
        """

        self.name = name
        self.description = description
        self.image_url = image_url
        self.wiki_url = wiki_url

    def json(self):
        """Return a JSON data of the instance variables"""

        return {'authorId' : self.authorId, 'name': self.name, 'description': self.description, 'image_url': self.image_url, 'wiki_url': self.wiki_url, 'books' : [book.json() for book in self.books.all()]}

    # Important methods used to retrieve data through SQL Alchemy
    @classmethod
    def find_by_name(cls, name):
        """Retrieve the author provided its name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, authorId):
        """Retrieve the author provided its id"""        
        return cls.query.filter_by(authorId=authorId).first()

    def save_to_db(self):
        """Methods used to push and commit to the database"""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Methods used to delete and commit to the database"""        
        db.session.delete(self)
        db.session.commit()
