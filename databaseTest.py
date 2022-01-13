# This file is meant to show the database functions properly in some aspects. 
# 
#
from db import Database
import uuid

def testDatabase() :
    database = Database()
    database.create_all_tables()

    # Create a module
    module_id = str(uuid.uuid4())
    name = "SE 410 Database Test"
    description = "Test for SE 410 Team Project"
    language = "English"
    subject = "Software Engineering"
    minutes = 10
    submitted_by = "Team Red"
    category = "None"
    module_rating = "None"
    date_time = "None"
    material_set = "None"
    education_level = "University"
    pre_requisites = "None"

    database.create_module(module_id, name, description, language, subject, minutes, submitted_by, category, module_rating, date_time, material_set, education_level, pre_requisites)

    module = database.get_module_by_id(module_id)
    print(module)
    
    newValues = { "module_id" : module_id, "description" : "Now we have a new description", "date_time" : "Right Now!" }
    database.edit_module(newValues)

    module = database.get_module_by_id(module_id)
    print(module)

    user_type_id = str(uuid.uuid4())
    is_admin = True
    is_student = False
    permissions = "admin"
    database.create_user_type(user_type_id, is_admin, is_student, permissions)

    education_level_id = str(uuid.uuid4())
    level = "PhD"
    database.create_education_level(education_level_id, level)

    user_id = str(uuid.uuid4())
    name = "Test User"
    email = "user@drexel.edu"
    password = "password"
    groups = None
    modules = module_id
    database.create_user(user_id, name, email, password,user_type_id, education_level_id, groups, modules)

    
    
    






if __name__ == "__main__" :
    testDatabase()
