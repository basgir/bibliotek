###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : portfolio.py Portfolio Flask_restful resource
# #########################################
from flask_restful import Resource, reqparse
from models.portfolio import PortfolioModel


class Portfolio(Resource):
    """Portfolio. Resource that helps with dealing with Http request for a portfolio by provided an id.
    
    HTTP GET call : /portfolios/<int:id>

    HTTP PUT call : /portfolios/<int:id>

    HTTP DELETE call : /portfolios/<int:id>
    """

    # Create the parser for the content of the HTTP request
    parser = reqparse.RequestParser()

    # The parser require some arguments that ifnot fulfilled, return an error
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Each portfolio have to have a name"
                        )
    parser.add_argument('userId',
                        type=str,
                        required=True,
                        help="Each Portfolio does belong to a user."
                        )

    def get(self, id):
        """GET request that deals with requests that look for a portfolio by id"""
        
        # Request to the model
        portfolio = PortfolioModel.find_by_id(id)

        # if found
        if portfolio:
            return portfolio.json()

        # if not
        return {'message': 'Portfolio not found'}, 404

    # Only the name can be updated.
    def put(self, id):
        """PUT request that deals with the edition or a creation of a portfolio with at a certain id"""

        # Parse the application/json data
        data = Portfolio.parser.parse_args()

        # Call the model
        portfolio = PortfolioModel.find_by_id(id)

        # if already exists we update
        if portfolio:
            portfolio.name = data['name']
        else:
            # if doesn't we create
            portfolio = PortfolioModel(**data)
        
        # save and commit to database
        portfolio.save_to_db()

        # return the object as json
        return portfolio.json()

    def delete(self, id):
        """DELETE request that deals with the deletion of book given its id"""

        # Look for the portfolio with a specific id
        Portfolio = PortfolioModel.find_by_id(id)

        # if exist
        if Portfolio:
            try:
                # we delete it
                Portfolio.delete_from_db()
                return {'message': 'Portfolio deleted'}
            except:
                # if error during deletion
                return {'message': 'A portfolio is linked to a many portfolio_book relations, so before deleting it you need to delete all these relations.'}
        else:
            # if doesn't exist
            return {'message' : 'Portfolio not found'}, 404


class PortfolioList(Resource):
    """Portfolio List. Resource that helps with dealing with Http requests that creates or list portfolios.
    
    HTTP POST call : /books

    HTTP GET call : /books
    """

    def post(self):
        """POST request that creates a new portfolio provided the correct data"""

        # if already exists
        if PortfolioModel.find_by_name(data['name']):
            return {'message': "An portfolio with name '{}' already exists.".format(data['name'])}, 400

        # Parse the application/json data
        data = Portfolio.parser.parse_args()

        # We create the portfolio
        portfolio = PortfolioModel(**data)

        # we try to save and commit
        try:
            portfolio.save_to_db()
        except:
            # in case of error
            return {"message": "An error occurred inserting the portfolio."}, 500

        # return a json
        return portfolio.json(), 201

    def get(self):
        """GET request returns the list of all portfolios"""

        return {'Portfolios': list(map(lambda x: x.json(), PortfolioModel.query.all()))}

class PortfolioUser(Resource):
    """Book. Resource that helps with dealing with Http request for a book by providing its id.
    
    HTTP GET call : /users/<int:id>/portfolios
    """
    def get(self, id):
        """GET request returns the list of all portfolios belonging to a user"""
        
        # We find all portfolios that belong to a user
        Portfolio = PortfolioModel.find_portfolios_by_user(id)

        # if there is any we return them as json
        if Portfolio:
            return {'Portfolios': list(map(lambda x: x.json(), Portfolio))}, 201
        else:
            # If there is none
            return {'message': 'This user does not exist or does not have any portfolio'}, 404



