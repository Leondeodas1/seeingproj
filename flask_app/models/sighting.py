from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
mydb = 'exam'


class sighting:
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.date_of_sighting = data['date_of_sighting']
        self.number_of_sasquatches = data['number_of_sasquatches']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.his = []
        self.food=[]

    @staticmethod
    def validate_sighting(res):
        is_valid = True
        if len(res['location']) < 0:
            flash("Location is Required")
            is_valid = False
        elif len(res['location']) < 3:
            flash("Location must be at least 3 characters.")
            is_valid = False
        if len(res['what_happened']) < 0:
            flash("what_ happened is Required")
            is_valid = False
        elif len(res['what_happened']) < 3:
            flash("what happened must be at least 3 characters.")
            is_valid = False
        if len(res['date_of_sighting']) < 3:
            flash(" Date is Required")
            is_valid = False
        if len(res['number_of_sasquatches']) < 1:
            flash("number_of_sasquatches must be 1 or greater.")
            is_valid = False
        return is_valid

    @classmethod
    def all_sightings(cls):
        query =  "SELECT * from sighting;" 
        results = connectToMySQL(mydb).query_db(query)
            
        sighting = []
            
        for ever_sight in results:
            sighting.append( cls(ever_sight) )
        return sighting

    @classmethod
    def insert_sighting(cls,data):
        query = "INSERT INTO sighting(location,what_happened,date_of_sighting,number_of_sasquatches, created_at,updated_at,user_id) VALUES (%(location)s, %(what_happened)s, %(date_of_sighting)s, %(number_of_sasquatches)s, NOW(), NOW(), %(users_id)s );"
        return connectToMySQL(mydb).query_db(query,data)

    @classmethod
    def show_all_sighting(cls):
        query = "SELECT * FROM sighting LEFT JOIN users on users.id = sighting.user_id;"
        results = connectToMySQL(mydb).query_db(query)

        tog= cls(results[0])

        for usera in results:
            tog.his.append(usera)
            # print(usera)
            # print(tog.his)
        return tog

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM sighting WHERE id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)

    @classmethod
    def edit(cls,data):
        query = "update sighting SET location=%(location)s, what_happened=%(what_happened)s, date_of_sighting=%(date_of_sighting)s, number_of_sasquatches=%(number_of_sasquatches)s, updated_at=NOW() WHERE id =  %(users_id)s;"
        return connectToMySQL(mydb).query_db(query, data)




    @classmethod
    def show_sightings_by_id(cls,data):
        query = "SELECT * From sighting LEFT JOIN users on users.id = sighting.user_id where sighting.id = %(id)s;"
        results = connectToMySQL(mydb).query_db(query,data)
        # print(results)
        together= cls(results[0])
        # print(together)
        for usera in results:
            users_data = {
                "id" : usera['id'],
                "first_name" : usera['first_name'],
                "last_name" : usera['last_name'],
                "email" : usera['email'],
                "password": usera['password'],
                "created_at" : usera['created_at'],
                "updated_at" : usera['updated_at'] 
            }
            # print(usera)
            together.food.append(user.users(users_data))
            
            # for x in together.food:
            
        return together

    @classmethod 
    def delete_it(cls,data):
        query = "Delete From sighting Where id = %(id)s;"
        return connectToMySQL(mydb).query_db(query,data)
