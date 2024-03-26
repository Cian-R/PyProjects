import inspect


class Billbot():
    def __init__(self):
        self.categories = {"all": {}}

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

    def add_cat(self, category_name):
        self.categories[category_name] = {}

    def add_item(self, category, item, value):
        self.categories["all"][item] = value
        self.categories[category][item] = value

    def tree(self):
        for item in self.categories.keys():
            print("+", item)
            for line in self.categories[item].keys():
                print("    -", line, self.categories[item][line])

    def get_cats(self):
        return [name for name in self.categories.keys()]

    def get_items(self, cat):
        return [item for item in self.categories[cat].keys()]

    def remove_cat(self, cat):
        for key in self.categories[cat].keys():
            del self.categories["all"][key]
        del self.categories[cat]


app = Billbot()
