###########################################
#   Author : Bastien Girardet, Deborah De Wolff
#   Date : 13.05.2018
#   Course : Applications in Object-oriented Programming and Databases
#   Teachers : Binswanger Johannes, Zürcher Ruben
#   Project : Bibliotek
#   Name : category.py Category Flask_restful resource
# #########################################
from flask_restful import Resource, reqparse
from models.category import CategoryModel


class Category(Resource):
    """Category. Resource that helps with dealing with Http request for a category by providing its id.
    
    HTTP GET call : /categories/<int:id>

    HTTP POST call : /categories/<int:id>

    HTTP PUT call : /categories/<int:id>
    
    HTTP DELETE call : /categories/<int:id>
    """

    # Create the parser for the content of the HTTP request
    parser = reqparse.RequestParser()
    
    # The parser require some arguments that ifnot fulfilled, return an error
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Each category have to have a name"
                        )

    def get(self, id):
        """GET request that deals with requests that look for a category by id"""

        # Request to the model        
        Category = CategoryModel.find_by_id(id)

        # If the category exists
        if Category:

            # We return it as json
            return Category.json()

        # If not found
        return {'message': 'Category not found'}, 404

    def post(self, id):
        """POST request that deals with creation of a category provided an id"""

        # Call the model in order to find the category provided its id
        if CategoryModel.find_by_id(id):
            return {'message': "A Category with id '{}' already exists.".format(id)}, 400
    
        # Push the data to the model
        Category = CategoryModel(id)
        try:
            # Try to save
            Category.save_to_db()
        except:
            # If error
            return {"message": "An error occurred creating the Category."}, 500

        # once done we return the object as json
        return Category.json(), 201

    
    def put(self, id):
        """PUT request that deals with the edition or a creation of a category with at a certain id"""

        # Parse the application/json data
        data = Category.parser.parse_args()

        # Call the model
        category = CategoryModel.find_by_id(id)

        # if the category already exists
        if category:

            # we update the field
            category.name = data['name']
        else:
            # Else we create it
            category = CategoryModel(**data)

        # then we save and commit
        category.save_to_db()

        # We return the category as json
        return category.json()


    def delete(self, id):
        """DELETE request that deals with the deletion of a category with at a certain id"""

        # Call the model that fetch the category provided its id
        Category = CategoryModel.find_by_id(id)

        # if exists
        if Category:
            try:
                # we try to delete
                Category.delete_from_db()
                return {'message': 'Category deleted'}
            except:
                # if error during deletion
                return {'message': 'The category might belong to many books. To delete this catery you might want to delete all portfolio_book relations first, then portfolio, then all the books fo that category then finally delete the category.'}
        else:
            # if category not found
            return {'message' : 'Category not found'}, 404

class CategoryName(Resource):
    """Category Title. Resource that helps with dealing with Http request for a category provided its name.
    
    HTTP GET call : /categories/name/<string:name>

    HTTP POST call : /categories/name/<string:name>

    HTTP PUT call : /categories/name/<string:name>
    
    HTTP DELETE call : /categories/name/<string:name>
    """
    # Create the parser for the content of the HTTP request
    parser = reqparse.RequestParser()

    # The parser require some arguments that ifnot fulfilled, return an error
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="Each category have to have a name"
                        )

    def get(self, name):
        """GET request that deals with requests that look for a category by name"""

        # Request to the model        
        Category = CategoryModel.find_by_name(name)
        
        # if exists
        if Category:

            # we return a json
            return Category.json()
        
        # if not found
        return {'message': 'Category not found'}, 404

    def post(self, name):
        """POST request that deals with creation of a category provided a name"""

        # Call the model to look for a category provided a name
        if CategoryModel.find_by_name(name):
            return {'message': "A Category with name '{}' already exists.".format(name)}, 400

        # We create the category with the given name      
        Category = CategoryModel(name)

        try:
            # try to save and commit
            Category.save_to_db()
        except:
            # if error during saving and committing
            return {"message": "An error occurred creating the Category."}, 500

        # we return the json of the category
        return Category.json(), 201

    
    def put(self, name):
        """PUT request that deals with the edition or a creation of a category with at a certain name"""

        # we parse the arguments of the JSON
        data = Category.parser.parse_args()

        # Call the model to find the category entry with a specific name
        category = CategoryModel.find_by_name(name)

        # if the category exists
        if category:

            # then we update
            category.name = data['name']
        else:

            # If doesn't exist we create it
            category = CategoryModel(**data)
        
        # we save and commit
        category.save_to_db()

        # Return a json of the object
        return category.json()


    def delete(self, name):
        """DELETE request that deals with the deletion of a category with at a certain name"""

        # Call the category Model to find a category with a specific name
        Category = CategoryModel.find_by_name(name)

        # If the category exists
        if Category:
            try:
                # then we try to delete
                Category.delete_from_db()
                return {'message': 'Category deleted'}
            except:
                # In case of error
                return {'message': 'ERROR : During the deletion of category : {}'.foramt(id)}
        else:
            # If the category not found
            return {'message' : 'Category not found'}, 404


class CategoryList(Resource):
    """Category List. Resource that contains methods that deal with the creation of new categories and the listing of all categories
    
    HTTP POST call : /categories

    HTTP GET call : /categories
    """
    def post(self):
        """POST request create a category, provided a name"""

        # we parse the args
        data = Category.parser.parse_args()

        # we call the model and find the category by name
        if CategoryModel.find_by_name(data['name']):

            # We return if the category already exist
            return {'message': "An category with name '{}' already exists.".format(data['name'])}, 400

        # Ifnot we create the category
        category = CategoryModel(**data)

        try:
            # We try to save and commit
            category.save_to_db()
        except:
            # In case of error we return an error
            return {"message": "An error occurred inserting the category."}, 500

        # Return a json of the object
        return category.json(), 201

    def get(self):
        """GET request that returns a list of all the categories"""
        return {'Categories': list(map(lambda x: x.json(), CategoryModel.query.all()))}
