###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : author.py Author Flask_restful resource
# #########################################

from flask_restful import Resource, reqparse
from models.author import AuthorModel


class Author(Resource):
    """Author. Resource that helps with dealing with Http request for a book by providing its id.
    
    HTTP GET call : /authors/<int:id>

    HTTP POST call : /books/<int:id>
    
    HTTP DELETE call : /books/<int:id>

    HTTP PUT call : /books/<int:id>
    """

    # Create the parser for the content of the HTTP request    
    parser = reqparse.RequestParser()

    # The parser require some arguments that ifnot fulfilled, return an error    
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Each Author have to have a name"
                        )
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help="An author might have a description. (Short Biography)"
                        )
    parser.add_argument('image_url',
                        type=str,
                        required=False,
                        help="An image url might be assigned to an author if available."
                        )
    parser.add_argument('wiki_url',
                        type=str,
                        required=False,
                        help="Wikipedia link of the author if available."
                        )

    def get(self, id):
        """GET request that deals with requests that look for a author by id"""
        
        # Call the model        
        Author = AuthorModel.find_by_id(id)

        # If exists
        if Author:
            return Author.json()

        # If doesn't exists
        return {'message': 'Author not found'}, 404

    def post(self, id):
        """POST request that deals with the creation of an a new author"""

        if AuthorModel.find_by_id(id):
            return {'message': "An Author with id '{}' already exists.".format(id)}, 400

        # Parse the application/json data
        data = Author.parser.parse_args()

        # Call the model        
        author = AuthorModel(id, **data)

        try:
            # Try to save and commit the author
            author.save_to_db()
        except:
            # If it breaks
            return {"message": "An error occurred inserting the Author."}, 500

        # Return the json of the author
        return author.json(), 201

    def put(self, id):
        """PUT request that deals with the edit or a creation of an author with at a certain id"""

        # Parse the application/json data
        data = Author.parser.parse_args()

        # Call the model
        author = AuthorModel.find_by_id(id)

        # if exists
        if author:
            # Update the fields
            author.name = data['name']
            author.description = data['description']
            author.image_url = data['image_url']
            author.wiki_url = data['wiki_url']
        else:
            # Else we create
            author = AuthorModel(**data)
        # save and commit
        author.save_to_db()
        
        # Return json when all is done.
        return author.json()

    def delete(self, id):
        """DELETE request that deals with the deletion of an author provided a certain id"""

        # Call the model        
        Author = AuthorModel.find_by_id(id)

        # If exists
        if Author:
            try:
                # We try to delete
                Author.delete_from_db()
                return {'message': 'Author deleted'}
            except:
                return {'message': 'ERROR : During the deletion of author : {}'.foramt(id)}
        else:
            # In case we don't found the author
            return {'message' : 'Author not found'}, 404

class AuthorName(Resource):
    """Author Name. Resource that helps with dealing with Http request for a author by providing its name.
    
    HTTP POST call : /authors/name/<string:name>
    
    HTTP GET call : /authors/name/<string:name>

    HTTP POST call : /authors/name/<string:name>
    
    HTTP GET call : /authors/name/<string:name>
    """

    # Create the parser for the content of the HTTP request
    parser = reqparse.RequestParser()

    # The parser require some arguments that ifnot fulfilled, return an error
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Each Author have to have a name"
                        )
    parser.add_argument('description',
                        type=str,
                        required=False,
                        help="An author might have a description. (Short Biography)"
                        )
    parser.add_argument('image_url',
                        type=str,
                        required=False,
                        help="An image url might be assigned to an author if available."
                        )
    parser.add_argument('wiki_url',
                        type=str,
                        required=False,
                        help="Wikipedia link of the author if available."
                        )

    def get(self, name):
        """GET request that deals with requests that look for a author provided its name"""

        # Request to the model        
        Author = AuthorModel.find_by_name(name)

        # if found
        if Author:

            # Return a json
            return Author.json()

        # if not
        return {'message': 'Author not found'}, 404

    def post(self, name):
        """POST request that creates an author, provided a name and description, image_url, wiki_url"""

        # Request to the model and if found
        if AuthorModel.find_by_name(name):

            # Return meessage that author exists
            return {'message': "An Author with name '{}' already exists.".format(name)}, 400

        # Parse the application/json data
        data = Author.parser.parse_args()

        # We pass the arguments to the model
        author = AuthorModel(name, **data)

        # Try to save
        try:
            author.save_to_db()
        except:
            # if error
            return {"message": "An error occurred inserting the Author."}, 500

        # Return a json of the created author
        return author.json(), 201

    def put(self, name):
        """PUT request that creates an author, provided a name and description, image_url, wiki_url"""

        # Parse the application/json data
        data = Author.parser.parse_args()

        # Request to the model to find the author
        author = AuthorModel.find_by_name(name)

        # If found
        if author:
            # We update its variables
            author.name = data['name']
            author.description = data['description']
            author.image_url = data['image_url']
            author.wiki_url = data['wiki_url']
        else:
            # Else we create it
            author = AuthorModel(**data)
        
        # Then we save
        author.save_to_db()

        # We return the updated author in json
        return author.json()

    def delete(self, id):
        """DELETE request that deals with the deletion of an author provided an authorId"""

        # We look for the Author provided an id
        Author = AuthorModel.find_by_id(id)

        # If exists
        if Author:
            try:
                # We try to delete it from the database
                Author.delete_from_db()
                return {'message': 'Author deleted'}
            except:
                # If error
                return {'message': 'The author has relations you might want to delete the books that belongs to him first.'}
        else:
            # If he doesn't exist
            return {'message' : 'Author not found'}, 404

class AuthorList(Resource):
    """Author List. Resource that helps with dealing with Http request for creating a user or listing all users.
    
    HTTP POST call : /authors

    HTTP GET call : /authors
    """
    def post(self):
        """POST request that creates an author, provided a name and description, image_url, wiki_url"""  
              
        # Parse the application/json data
        data = Author.parser.parse_args()

        # Look if we find the author by its name
        if AuthorModel.find_by_name(data['name']):
            return {'message': "An author with name '{}' already exists.".format(data['name'])}, 400

        # If user doesn't exists then we create it
        author = AuthorModel(**data)

        # we try push and commit
        try:
            author.save_to_db()

        except:
            #if error
            return {"message": "An error occurred inserting the author."}, 500

        # We return a json of the author
        return author.json(), 201

    def get(self):
        """GET request that obtain a list of all Authors""" 
         
        # Return a JSON data of all authors.
        return {'Authors': list(map(lambda x: x.json(), AuthorModel.query.all()))}
