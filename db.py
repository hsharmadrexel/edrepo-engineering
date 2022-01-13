import os
import re
import sqlite3
import tables

SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'db1.db')


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_PATH)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    # These are all of the creation functions that execute inserts on the SQL database.
    
    # FRID-4 (New User Registration): Create a new user account
    # FRID-16: Add new user (Admin uses the same function below to add a new user to the system as the underlying back-end functionality of adding the user or registration is the same)
    def create_user(self, user_id, name, email, encrypted_password, user_type, education_level, groups, modules):
        self.execute('INSERT INTO users (user_id, name, email, password, user_type, education_level, groups, modules) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [user_id, name, email, encrypted_password, user_type, education_level, groups, modules])

    # FRID-10: Create and Submit New Module
    def create_module(self, module_id, name, description, language, subject, minutes, submitted_by, category, module_rating, date_time, material_set, education_level, pre_requisites):
        self.execute('INSERT INTO modules (module_id, name, description, language, subject, minutes, submitted_by, category, module_rating, date_time, material_set, education_level, pre_requisites) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [module_id, name, description, language, subject, minutes, submitted_by, category, module_rating, date_time, material_set, education_level, pre_requisites])
        print([module_id, name, description, language, subject, minutes, submitted_by,
               category, module_rating, date_time, material_set, education_level, pre_requisites])
        print("created module")

    def create_module_log(self, module_log_id, module_id, user_id, date_time, log):
        self.execute('INSERT INTO moduleLog (moduleLog_id, module_id, user_id, date_time, log) VALUES (?, ?, ?, ?, ?)',
                     [module_log_id, module_id, user_id, date_time, log])

    def create_material_set(self, material_set_id, materials_id, module_id):
        self.execute('INSERT INTO materialSet (material_set_id, materials_id, module_id) VALUES (?, ?, ?)',
                     [material_set_id, materials_id, module_id])

    def create_material(self, material_id, type, content, name, format, material_rating, category, date_time):
        self.execute('INSERT INTO materials (material_id, type, content, name, format, material_rating, category, date_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     [material_id, type, content, name, format, material_rating, category, date_time])

    def create_other_resources(self, resource_id, name, description, material_set_id, resource_link):
        self.execute('INSERT INTO otherResources (resource_id, name, description, material_set_id, resource_link) VALUES (?, ?, ?, ?, ?)',
                     [resource_id, name, description, material_set_id, resource_link])

    def create_rating(self, rating_id, rating, num_ratings):
        self.execute('INSERT INTO rating (rating_id, rating, num_ratings) VALUES (?, ?, ?)',
                     [rating_id, rating, num_ratings])

    def create_user_type(self, user_type_id, is_admin, is_student, permissions):
        self.execute('INSERT INTO userType (user_type_id, is_admin, is_student, permissions) VALUES (?, ?, ?, ?)',
                     [user_type_id, is_admin, is_student, permissions])

    def create_user_log(self, log_id, user_id, date_time, log):
        self.execute('INSERT INTO userLog (log_id, user_id, date_time, log) VALUES (?, ?, ?, ?)',
                     [log_id, user_id, date_time, log])

    def create_education_level(self, id, level):
        self.execute('INSERT INTO educationLevel (id, level) VALUES (?, ?)',
                     [id, level])

    def create_pre_requisites(self, pre_requisite_id, module_id, pre_requisite):
        self.execute('INSERT INTO preRequisites (preRequisite_id, module_id, pre_requisite) VALUES (?, ?, ?)',
                     [pre_requisite_id, module_id, pre_requisite])
                     
    # FRID-9: Submit Feedback
    def create_feedback(self, feedback_id, user_id, feedback_type, feedback_text):
        self.execute('INSERT INTO feedback (feedback_id, user_id, feedback_type, feedback_text) VALUES (?, ?, ?, ?)',
                     [feedback_id, user_id, feedback_type, feedback_text])

    # FRID-19: Edit Any Module
    # This function is meant to edit a module. It will take in json object that will map the values to the object
    def edit_module(self, module_edits):
        updateStatement = 'UPDATE modules SET '
        values = []
        for key in module_edits.keys():
            if key != "module_id":
                updateStatement += key + ' = (?), '
                values.append(module_edits[key])
        updateStatement = updateStatement[:-2] + ' WHERE module_id = (?)'
        values.append(module_edits["module_id"])
        print(updateStatement)
        self.execute(updateStatement, values)

    # FRID-18: Changes User Role
    def change_user_type(self, user_id, new_user_type):
        self.execute('UPDATE users SET user_type = (?) WHERE user_id = (?)', [new_user_type, user_id])

    # FRID-13: Delete Owned Module
    # FRID-20: Delete Any Module
    def remove_module(self, module_id):
        self.execute('DELETE FROM modules WHERE module_id = (?)', [module_id])

    # FRID-17: Remove User
    def remove_user(self, user_id):
        self.execute('DELETE FROM users WHERE user_id = (?)', [user_id])

    # FRID-8: This is adding a rating to an existing module
    def add_rating(self, module_id, rating):
        self.execute('UPDATE modules SET module_rating = (?) WHERE module_id = (?)', [rating, module_id]) 

    # FRID-1: Retrieve Specific Module
    def get_module_by_id(self, module_id):
        module = self.select('SELECT * FROM modules WHERE module_id = (?)', [module_id])
        return module

    # FRID-2: Get all Modules (Might need to add a function that builds a json with all of the data for the display)
    def get_all_modules(self):
        modules = self.select('SELECT * FROM modules')
        print("all modules")
        return modules
        
    # FRID-3: Search Module - On the UI, user would be presented with a drop-down menu which would consist of all the possible filters. Users can select one and type in the search parameter. Selected filter_name would be passed as a parameter from the UI file during a selected event as a wrapper.
    def search_module(self, filter_name, search_text):
        module_filtered = self.select('SELECT * from modules WHERE (?) = (?)', [filter_name, search_text])
        print("All module records with \"(?)\" matching text in the (?) filter/parameter", [search_text, filter_name])
        return module_filtered
        
    # FRID-4 (Sign-in): Validate User Sign-in
    def validate_sign_in(self, user_email, password):
        validation_result = self.select('SELECT CASE WHEN EXISTS (SELECT * from users WHERE email = (?) AND password = (?)) THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END', [user_email, password])
        print("User account validation prior to sign-in - 1 (account validated), 0 (incorrect email or password)")
        return validation_result
 
    # FRID-5: Get all the modules in a category
    def get_modules_category(self, category):
        modules = self.select('SELECT * FROM modules WHERE category = (?)', [category])
        return modules

    def create_all_tables(self) :
        allTables = tables.get_all_tables()
        for table in allTables :
            self.execute(table)

    def close(self):
        self.conn.close()
