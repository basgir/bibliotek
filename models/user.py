###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : user.py SQL Alchemy Model
# #########################################

from db import db


class UserModel(db.Model):
    """SQLAlchemy User Model"""
    
    # We assign the correct table
    __tablename__ = 'users'

    # Table columns
    userId = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    # Foreign key a user might have many portoflios
    portfolios = db.relationship("PortfolioModel", cascade="save-update, merge, delete", lazy='dynamic')

    def __init__(self, name, surname, email, password):
        """Constructor of the User model
        
        Arguments:
            name {string} -- name of the user
            surname {string} -- surname of the user
            email {string} -- email of the user
            password {string} -- password of the user
        """

        self.name = name
        self.surname = surname 
        self.email = email
        self.password = password

    def json(self):
        """Return a JSON data of the instance variables"""

        return {'userId': self.userId,'name': self.name, 'surname': self.surname, 'email': self.email, 'password': self.password, 'Portfolios' : [portfolio.json() for portfolio in self.portfolios.all()]}


    @classmethod
    def find_by_email(cls, email):
        """Retrieve the user provided its email"""        
        return cls.query.filter_by(email=email).first()
        
    @classmethod
    def find_by_id(cls, userId):
        """Retrieve the user provided its userId"""        
                        
        return cls.query.filter_by(userId=userId).first()

    @classmethod
    def check_user_exists_by_email(cls, email):
        """Check whether the user email exists"""        
        exists = False
        if cls.query.filter_by(email=email).first():
            return True
        else:
            return False

    # Important methods used to retrieve data through SQL Alchemy
    def save_to_db(self):
        """Methods used to push and commit to the database"""    
            
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Methods used to delete and commit to the database"""  
        
        db.session.delete(self)
        db.session.commit()
