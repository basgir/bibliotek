###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : user.py UserRegister Flask_restful resource
# #########################################
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """User Register. Resource that helps in creating an new user in the database through HTTP requests."""

    # Parse the request arguments.
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('surname',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        """POST request on the user in order to create a new entry in the database."""

        # We parse the data that is coming from the request
        data = UserRegister.parser.parse_args()

        # We look if the user is already registered.
        if UserModel.find_by_email(data['email']):

            # In case of the user is already registered we return a code 400 Bad Request with the message
            return {"message": "A user with that email already exists"}, 400

        # We create the user through the model
        user = UserModel(**data)

        # We save the data into the database through SQLAlchemy and Pymysql
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class UserList(Resource):
    """User List ressource. Create the REST resource for the list of the users """

    def get(self):
        """GET request that returns the list of all users."""

        # Create the JSON by mapping all paramaters
        return {'Users': list(map(lambda x: x.json(), UserModel.query.all()))}

class User(Resource):
    """ User resource. Create the User REST resource for the request that get one user by id"""

    def get(self, id):
        """GET request that return the data of one user searched by his id.""" 

        # Look for the user given the id
        User = UserModel.find_by_id(id)

        # If found return the json data of the user
        if User:
            return User.json()

        # ifnot not found message and code 404
        return {'message': 'User not found'}, 404 

    def delete(self, id):
        """DELETE request that delete the user and its childs""" 

        User = UserModel.find_by_id(id)
        if User:
            User.delete_from_db()
            return {'message': 'User deleted'}
        else:
            return {'message' : 'User not found'}, 404


class UserEmail(Resource):
    """ User Email resource. Create the User REST resource for the request that get one user by email"""    
    def get(self, email):
        """GET request that return the data of one user searched by his email."""

        # Look for the user given the email                 
        User = UserModel.find_by_email(email)

        # If found return the json data of the user
        if User:
            return User.json()

        # ifnot not found message and code 404
        return {'message': 'User not found or unkown email'}, 404 

    