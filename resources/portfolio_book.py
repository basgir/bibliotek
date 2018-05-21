###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : portfolio_book.py Portfolio_book Flask_restful resource
# #########################################
from flask_restful import Resource, reqparse
from models.portfolio_book import PortfolioBookModel
from models.book import BookModel

class PortfolioBook(Resource):
    """PortfolioBook. Resource that helps with dealing with Http request for a portfolio_book provided an id.
    
    HTTP GET call : /portfolios/<int:portfolioId>/books

    HTTP DELETE call : /portfolios/<int:portfolioId>/books
    """
    # we parse the args
    parser = reqparse.RequestParser()

    # The parser require some arguments that ifnot fulfilled, return an error
    parser.add_argument('bookId',
                        type=int,
                        required=True,
                        help="Each relation does have a book id"
                        )
    parser.add_argument('portfolioId',
                        type=int,
                        required=True,
                        help="Each relation does have a portfolio id"
                        )

    def get(self, portfolioId):
        """GET request that deals with requests that look for a portfolio book relation given a portfolioId"""
        
        # Call the model to find the portfolio book relations that has a specific portfolio Id
        portfolio_book = PortfolioBookModel.find_by_portfolio_id(portfolioId)

        # If found
        if portfolio_book:
            # We return the list  of relations as json
            return {'Portfolio Book of Portfolio {}'.format(portfolioId): list(map(lambda x: x.json(), portfolio_book))}, 201
        else:
            # If not found we return an error
            return {'message': 'This portofolio does not exist or does not have any book in the portfolio'}, 404

    def delete(self, portfolioId):
        """DELETE request that deals with the deletion of all relations that belongs to a portfolioId"""

        # Call the model to find all entries that have a certain portfolioId
        portfolio_book = PortfolioBookModel.find_by_portfolio_id(portfolioId)
        
        # if found
        if portfolio_book:

            # we delete
            portfolio_book.delete_from_db()
            return {"Portfolio relations deleted"}, 201
        else:
            # Else error
            return {'message': 'This Portfolio relations does not exist or does not have any book in the portfolio'}, 404

class PortfolioBookList(Resource):
    """Portfoliobook. Resource that deals with requests that insert new portfolio _ book relations into the database.

    HTTP GET call : /portoflio/books
    """

    def get(self):
        """GET request that returns the list of all the portfolio book relations""" 

        # return all as json
        return {'Portfolio Books': list(map(lambda x: x.json(), PortfolioBookModel.query.all()))},200

class PortfolioBookEdit(Resource):
    """Book. Resource that helps with dealing with Http request that create or delete portfolio book relations provided a portfolioId and bookId.
    
    HTTP POST call : /portfolios/<int:portfolioId>/books/<int:bookId>

    HTTP DELETE call : /portfolios/<int:portfolioId>/books/<int:bookId>
    """
    def post(self, portfolioId, bookId):
        """POST request create a portfolio_book relation provided a portfolioId and a bookId"""

        relation = PortfolioBookModel.does_this_relation_exists(portfolioId, bookId)

        # Check if the relation already exists
        if  relation:
            return {"message": "The relation already exists"}, 500
        else:
            try:
                # Call the model by providing the two arguments
                relation = PortfolioBookModel(bookId,portfolioId)

                # Save and commit
                relation.save_to_db()
            except:
                return {"message": "An error occurred inserting the relation portfolio_book. Check whether the book or the portofolio do exist"}, 500

            # return the json
            return relation.json(), 201
    
    def delete(self, portfolioId, bookId):
        """DELETE request that delete a portfolio_book relation provided a portfolioId and a bookId"""

        # Fetch the relation
        relation = PortfolioBookModel.find_by_portfolio_and_book(portfolioId, bookId)
        
        # if exists
        if relation:
            try:
                # we delete it
                relation.delete_from_db()
                return {'message': 'Relation deleted'}
            except:
                return {'message': 'Error while deleting the relation.'}
        else:
            # if not found
            return {'message' : 'Relation not found'}, 404
