#!/usr/bin/python
# -*- coding: utf-8 -*-
###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 11.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : app.py 
#   Goal : provide an ReSTful API that is connected to the database.
#   Help the user in managing his book library.
#   Main Libraries : Flask, Flask_restful and pymysql
#   API DOCUMENTATION URL : https://documenter.getpostman.com/collection/view/2471406-227dcc87-8dbe-e51d-264a-c6b929bc3593
# #########################################

from flask import Flask
from flask_restful import Api
from resources.user import UserRegister, UserList, User, UserEmail
from resources.book import Book, BookTitle, BookList, BookCategories, BookAuthors, BookSearch
from resources.author import Author, AuthorList, AuthorName
from resources.category import Category, CategoryList, CategoryName
from resources.portfolio_book import PortfolioBook, PortfolioBookList, PortfolioBookEdit
from resources.portfolio import Portfolio, PortfolioList, PortfolioUser
import pymysql

app = Flask(__name__)

# AWS credentials
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = 'oopdatabase.cq3xiqh7vtmo.eu-west-3.rds.amazonaws.com'
DB_NAME = 'bibliotek'

# URI builder
URI = "mysql+pymysql://{0}:{1}@{2}/{3}".format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)

# Setting up the config of our app
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'bastien'

# Instance of our Flask API
api = Api(app)

# Books
api.add_resource(BookList, '/books', methods=['GET','POST'])
api.add_resource(Book, '/books/<int:id>', methods=['POST','GET','DELETE','PUT'])
api.add_resource(BookTitle, '/books/title/<string:title>', methods=['POST','GET','DELETE','PUT'])
api.add_resource(BookAuthors, '/authors/<int:id>/books', methods=['GET'])
api.add_resource(BookCategories, '/categories/<int:id>/books', methods=['GET'])
api.add_resource(BookSearch, '/search/book', methods=['POST'])

# Categories
api.add_resource(CategoryList, '/categories', methods=['GET','POST'])
api.add_resource(Category, '/categories/<int:id>', methods=['POST','GET','DELETE','PUT'])
api.add_resource(CategoryName, '/categories/name/<string:name>', methods=['POST','GET','DELETE','PUT'])

# Authors
api.add_resource(AuthorList, '/authors', methods=['GET','POST'])
api.add_resource(Author, '/authors/<int:id>', methods=['POST','GET','DELETE','PUT'])
api.add_resource(AuthorName, '/authors/name/<string:name>', methods=['POST','GET','DELETE','PUT'])

# Portfolio Book API routes
api.add_resource(PortfolioBookList, '/portfolios/books', methods=['GET'])
api.add_resource(PortfolioBook, '/portfolios/<int:portfolioId>/books', methods=['GET', 'DELETE'])
api.add_resource(PortfolioBookEdit, '/portfolios/<int:portfolioId>/books/<int:bookId>', methods=['POST','DELETE'])
api.add_resource(PortfolioUser, '/users/<int:id>/portfolios', methods=['GET'])
api.add_resource(Portfolio, '/portfolios/<int:id>', methods=['GET','PUT','DELETE'])

# Portfolio API routes
api.add_resource(PortfolioList, '/portfolios', methods=['GET','POST'])

# User API routes
api.add_resource(UserRegister, '/register', methods=['POST'])
api.add_resource(User, '/users/<int:id>', methods=['GET','DELETE'])
api.add_resource(UserList, '/users', methods=['GET'])
api.add_resource(UserEmail, '/users/email/<string:email>', methods=['GET'])

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    with app.test_request_context():

        # We import the models
        from models import author
        from models import category
        from models import user
        from models import portfolio
        from models import portfolio_book
        from models import book
        db.create_all()

    # We run the app 
    app.run(port=5000, debug=True, threaded=True)
