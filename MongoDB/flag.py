
class Flag():

    def __init__(self, value=False):
        self.flag_value = False
    
    def set_true(self):
        self.flag_value = True
    
    def set_false(self):
        self.flag_value = False
    
    def check(self):
        return self.flag_value
