from flask_app.config.mysqlconnection import connectToMySQL

class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]

    @classmethod
    def new_recipe(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(user_id)s);"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def get_all_recipes(cls,data):
        query = "SELECT * FROM recipes;"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name =  %(name)s, description = %(description)s, instructions = %(instructions)s WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL("recipes").query_db(query, data)