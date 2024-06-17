from .custom_class.py import CustomClass

class CustomAnalyzer:
    def __init__(self):
        self.classes = []

    def analyze_data(self, names, view, recoms, reple):
        for name, view, recom, reple in zip(names, view, recoms, reple):
            found = False
            for custom_class in self.classes:
                if custom_class.name == name:
                    custom_class.add_member(view, recom, reple)
                    found = True
                    break

            if not found:
                new_class = CustomClass(name)
                new_class.add_member(view, recom, reple)
                self.classes.append(new_class)

    def get_classes_sorted_by_num(self):
        sorted_classes = sorted(self.classes, key=lambda x: x.num, reverse=True)
        return sorted_classes
