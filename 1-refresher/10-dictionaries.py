"""
Dictionaries
"""

user_dict = {
    'name': "eric",
    'age': 32,
    'children': []
}

# Get and item
print(user_dict["name"])
print(user_dict.get("name", "unknown"))

# Set an item
user_dict["parents"] = ["bob", "jane"]

print(user_dict)

# Keys
keys = user_dict.keys() # list of keys

# Values
values = user_dict.values() # list of values

for key, value in user_dict.items():
    print(f"key {key}, value {value}")#

import copy

new_user_dict = copy.deepcopy(user_dict)    # dict's .copy method is shallow so use copy module's deep copy method
new_user_dict["name"] = "daniel"
print(new_user_dict)
