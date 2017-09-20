class BaseModule:
    name = None
    route = None
    def __init__(self):
        pass
    def run(self, route:list, method:str, args:dict):
        pass
    def __repr__(self):
        return "<a href='{}'>{}</a>".format(self.route, self.name)
    def __str__(self):
        return self.__repr__()