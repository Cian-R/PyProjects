import json
# importing the module

# Employee dictionary created with data written
dictionary_employees = {
 'employee_1': {"name": "453", "Department_1": "Data"},
 'employee_2': {"name": "457", "Department_2": "Finance"},
}


# Printing the dictionary data
print("The dictionary is as: \n", dictionary_employees, "\n")


# json object getting serialised
json_object = json.dumps(dictionary_employees, indent=4)

save_file = open('src/output.json', 'w')
save_file.write(json_object)
save_file.close()

# to print the json_object and see the output
print("The json_object is as below:", json_object)
print("\n\nAnd back to dictionary.")
new_dict = json.loads(json_object)

for key in new_dict.keys():
    print(key)

dic = {'all': {}}
