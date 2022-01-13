#SQL Create Table Commands



CREATE_USERS_TABLE = """ CREATE TABLE IF NOT EXISTS users (
                                        user_id text PRIMARY KEY,
                                        name text NOT NULL,
                                        email text NOT NULL,
                                        password text NOT NULL,
                                        user_type_id text NOT NULL, 
                                        education_level_id text NOT NULL, 
                                        groups text, 
                                        modules text,
                                        FOREIGN KEY(user_type_id) REFERENCES userType(user_type_id),
                                        FOREIGN KEY(education_level_id) REFERENCES educationLevel(id)
                                    ); """

CREATE_MODULES_TABLE = """ CREATE TABLE IF NOT EXISTS modules (
                                        module_id text PRIMARY KEY, 
                                        name text NOT NULL, 
                                        description text NOT NULL, 
                                        language text NOT NULL, 
                                        subject text NOT NULL, 
                                        minutes int NOT NULL, 
                                        submitted_by text NOT NULL, 
                                        category text NOT NULL, 
                                        module_rating text, 
                                        date_time text, 
                                        material_set text, 
                                        education_level text NOT NULL, 
                                        pre_requisites text,
                                        FOREIGN KEY (submitted_by) REFERENCES user (user_id),
                                        FOREIGN KEY (education_level) REFERENCES educationLevel (user_id),
                                        FOREIGN KEY (pre_requisites) REFERENCES preRequisites (preRequisites_id),
                                        FOREIGN KEY (module_rating) REFERENCES rating (rating_id)
                                        FOREIGN KEY (material_set) REFERENCES materialSet (material_set_id)
                                    ); """

CREATE_MODULELOG_TABLE = """ CREATE TABLE IF NOT EXISTS moduleLog (
                                        moduleLog_id text NOT NULL,
                                        module_id text NOT NULL, 
                                        user_id text NOT NULL, 
                                        date_time text NOT NULL, 
                                        log text NOT NULL,
                                        FOREIGN KEY (module_id) REFERENCES modules (module_id),
                                        FOREIGN KEY (user_id) REFERENCES user (user_id)
                                    ); """

CREATE_MATERIALSET_TABLE = """ CREATE TABLE IF NOT EXISTS materialSet (
                                        material_set_id text PRIMARY KEY,
                                        materials_id text NOT NULL, 
                                        module_id text NOT NULL,
                                        FOREIGN KEY (module_id) REFERENCES modules (module_id),
                                        FOREIGN KEY (materials_id) REFERENCES material (material_id)
                                    ); """

CREATE_RATING_TABLE = """ CREATE TABLE IF NOT EXISTS rating (
                                        rating_id text PRIMARY KEY, 
                                        rating int NOT NULL, 
                                        num_ratings int NOT NULL
                                    ); """

CREATE_USERTYPE_TABLE = """ CREATE TABLE IF NOT EXISTS userType (
                                        user_type_id text PRIMARY KEY,
                                        is_admin BIT(1) NOT NULL,
                                        is_student BIT(1) NOT NULL,
                                        permissions text NOT NULL
                                    ); """

CREATE_USERLOG_TABLE = """ CREATE TABLE IF NOT EXISTS userLog (
                                        log_id text PRIMARY KEY,
                                        user_id text NOT NULL,
                                        date_time text NOT NULL,
                                        log text NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                                    ); """

CREATE_EDUCATIONLEVEL_TABLE = """ CREATE TABLE IF NOT EXISTS educationLevel (
                                        id text PRIMARY KEY,
                                        level text NOT NULL
                                    ); """

CREATE_OTHERRESOURCES_TABLE = """ CREATE TABLE IF NOT EXISTS otherResources (
                                        resource_id text PRIMARY KEY,
                                        name text NOT NULL,
                                        description text NOT NULL,
                                        material_set_id text NOT NULL,
                                        resource_link text,
                                        FOREIGN KEY (material_set_id) REFERENCES materialSet (material_set_id)
                                    ); """

CREATE_PREREQUISITES_TABLE = """ CREATE TABLE IF NOT EXISTS preRequisites (
                                        preRequisite_id text NOT NULL,
                                        module_id text NOT NULL,
                                        pre_requisite text NOT NULL,
                                        FOREIGN KEY (module_id) REFERENCES modules (module_id)
                                    ); """

CREATE_MATERIAL_TABLE = """ CREATE TABLE IF NOT EXISTS material (
                                        material_id text PRIMARY KEY,
                                        type text NOT NULL,
                                        content text NOT NULL,
                                        name text NOT NULL,
                                        format text NOT NULL,
                                        material_rating int,
                                        category text NOT NULL,
                                        date_time text NOT NULL,
                                        FOREIGN KEY (material_rating) REFERENCES rating (rating_id)
                                    ); """
                                    
CREATE_FEEDBACK_TABLE = """ CREATE TABLE IF NOT EXISTS feedback (
                                        feedback_id text PRIMARY KEY,
                                        user_id text NOT NULL,
                                        feedback_type text NOT NULL,
                                        feedback_text text NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                                    ); """

def get_all_tables() :
    return [CREATE_MODULES_TABLE, CREATE_MODULELOG_TABLE, CREATE_EDUCATIONLEVEL_TABLE, CREATE_MATERIALSET_TABLE, CREATE_MATERIAL_TABLE,
            CREATE_OTHERRESOURCES_TABLE, CREATE_PREREQUISITES_TABLE, CREATE_RATING_TABLE, CREATE_USERLOG_TABLE, CREATE_USERS_TABLE, CREATE_USERTYPE_TABLE]                                          
