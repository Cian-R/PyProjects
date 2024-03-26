import inspect
import json


class Billbot():
    def __init__(self):
        file = open('output.json', 'r')
        self.categories = json.load(file)

        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        self.method_dict = {name: method for name, method in methods}

        while True:
            print("===========")
            self.perform_inputs()

    def perform_inputs(self):
        inputs = input("> ").strip().split(" ")
        if inputs[0] not in self.method_dict:
            print("Not a method.")
            return None
        print("Inputs:", inputs)
        if len(inputs) == 1:
            self.method_dict[inputs[0]]()
        else:
            self.method_dict[inputs[0]](*inputs[1:])

    def addcat(self, category_name):
        self.categories[category_name] = {}

    def additem(self, category, item, value):
        self.categories["all"][item] = value
        self.categories[category][item] = value

    def tree(self):
        for item in self.categories.keys():
            print("+", item)
            for line in self.categories[item].keys():
                print("    -", line, self.categories[item][line])

    def getcats(self):
        return [name for name in self.categories.keys()]

    def getitems(self, cat):
        return [item for item in self.categories[cat].keys()]

    def rmcat(self, cat):
        for key in self.categories[cat].keys():
            del self.categories["all"][key]
        del self.categories[cat]

    def wipe(self):
        self.categories = {"all": {}}

    def exit(self):
        json_object = json.dumps(self.categories, indent=4)
        save_file = open('output.json', 'w')
        save_file.write(json_object)
        save_file.close()
        exit()


app = Billbot()
