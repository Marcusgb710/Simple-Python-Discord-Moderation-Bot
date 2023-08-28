import json
import os

class Database(dict):
    def __init__(self, parent_file, path="DataBase/database.json"):
        self.path = os.path.join(parent_file, path)
        with open(self.path, "r") as f:
            self=dict(json.load(f))

    
    def new_entry(self, member_name):
        self[member_name] = {}
        self[member_name]["bad_word_counter"] = 0
    
    
    def delete_entry(self, member_name):
        self.__delitem__(member_name)

    def update_database(self):
        with open(self.path, "w") as f:
            json.dump(self, f, indent=6)

    def has_entry(self, member_name):
        if member_name in self:
            return True
        return False
    