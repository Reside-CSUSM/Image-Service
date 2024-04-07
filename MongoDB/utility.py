import copy



class TwoValuePair():

    def __init__(self, abbr, full_name):
        self.abbreviation = abbr
        self.full_name = full_name
    
    def GetAbbr(self):
        return self.abbreviation

    def GetFullName(self):
        return self.full_name



class SmartMap():

    def __init__(self, map=None):
        self.original_map = {}
        self.reversed_map = {}
        if(map != None):
            self.original_map = map
            for item in self.original_map.items():
                self.reversed_map[item[1]] = item[0]
    
    def use_map(self, map):
        self.original_map = {}
        for item in self.original_map.items():
            self.reversed_map[item[1]] = item[0]

    def select_return_value(self, key):
        pass


STATE_ABBREVIATION = {
    'AL':'Alabama',
    'AK':'Alaska',
    'AZ':'Arizona',
    'AR':'Arkansas',
    'AS':'American Samoa',
    'CA':'California',
    'CO':'Colorado',
    'CT':'Connecticut',
    'DE':'Delaware',
    'DC':'District of Columbia',
    'FL':'Florida',
    'GA':'Georgia',
    'GU':'Guam',
    'HI':'Hawaii',
    'IL':'Illinois',
    'IN':'Indiana',
    'IA':'Iowa',
    'KS':'Kansas',
    'KY':'Kentucky',
    'LA':'Louisiana',
    'ME':'Maine',
    'MD':'Maryland',
    'MA':'Massachusetts',
    'MI':'Michigan',
    'MN':'Minnesota',
    'MS':'Mississippi',
    'MO':'Missouri',
    'MT':'Montana',
    'NE':'Nebraska',
    'NV':'Nevada',
    'NH':'New Hampshire',
    'NJ':'New Jersey',
    'NM':'New Mexico',
    'NY':'New York',
    'NC':'North Carolina',
    'ND':'North Dakota',
    'MP':'Northern Mariana Islands',
    'OH':'Ohio',
    'OK':'Oklahoma',
    'OR':'Oregon',
    'PA':'Pennsylvania',
    'PR':'Puerto Rico',
    'RI':'Rhode Island',
    'SD':'South Dakota',
    'SC':'South Carolina',
    'TN':'Tennessee',
    'TX':'Texas',
    'TT':'Territories',
    'UT':'Utah',
    'VT':'Vermont',
    'VA':'Virginia',
    'VI':'Virgin Islands',
    'WA':'Washington',
    'WV':'West Virginia',
    'WI':'Wisconsin',
    'WY':'Wyoming'
}


STATE_FULL_NAME = {
 
}

for item in STATE_ABBREVIATION.items():
    STATE_FULL_NAME[item[1]] = item[0]

STATE_NAMES = {

}

for item in STATE_ABBREVIATION.items():
    STATE_NAMES[item[0]] = TwoValuePair(item[0], item[1])

#Reversing order and adding Pair so that we can get any value regardless of which key it is
for item in STATE_FULL_NAME.items():
    STATE_NAMES[item[0]] = TwoValuePair(item[1], item[0])

class Flag():

    def __init__(self, value=False):
        self.flag_value = False
    
    def set_true(self):
        self.flag_value = True
    
    def set_false(self):
        self.flag_value = False
    
    def check(self):
        return self.flag_value

class CharGradient():
    def __init__(self, string, character, gradient_number=1):
        #NOTE: A gradient is particular section in string that is made up of single character
        #Example:  'Yaaashaswiiiiaaaaaa' here the gradient is 'aaaa' which can be manipulated in original string
        #Gradient number is a number that represents different section of gradient in same string
        self.string = string
        self.character = character
        self.gradient_number = gradient_number
        self.gradient = ""
        self.first_index = 0
        self.last_index = 0
        
        for j in range(0, self.gradient_number):
            #These two lines below only repeat if gradient_number > 1
            self.first_index = self.last_index

            self.gradient = ""

            #First index of gradient
            self.first_index = self.string[self.first_index:].find(self.character)
            self.last_index = None

            #Get the last index where the gradient ends
            for i in range(self.first_index, len(self.string)):
                if(self.string[i] != self.character):
                    self.last_index = i
                    break 
                self.gradient += self.character
            
            print("First i = ", self.first_index)
            print("Second i = ", self.last_index)

            ##NOTE It kinda works for the first gradient but when number is set to 2 or higher it doesn't work
            #Need to fix it
        
    def set_length(self, amount):
        newstr = ""
        for i in range(0, amount):
            newstr += self.character
        self.string = self.string.replace(self.gradient, newstr)

    def get_length(self):
        return len(self.gradient)

    def get(self):
        return self.gradient


def string_filter(name_org):
        
        print("\x1b[31mstring_filter()->Recieved String:\x1b[0m "+ name_org)
        name = copy.copy(name_org)
        unwanted_characters = ["#", "|", "*", "(", ")", "&", "^", "%", "$", "@", "!", "[", "]", "{", "}", ";", ">", "<", "?", "/", "/", "'", "~", "-", "+", "."]
        for character in unwanted_characters:
            if(character in name):
                print("Replaced Unwanted Charcter:", character)
                name = name.replace(character, " ")
                    

        #Try to look for white spaces on the ends
        rindex = name.rfind(" ")
        lindex = name.find(" ")

        #Find where do text characters appear
        global Ralphaindex, Lalphaindex
        if(lindex != -1):
            for i in range(0, len(name)):
                if((name[i] >= "A" and name[i] <= "z") or (name[i] >= "1" and name[i] <= "9")):
                    Lalphaindex = i
                    print("Alphabet found from Left at:", Lalphaindex)
                    break
            

            for i in range(len(name)-1, 0, -1):
                print("ralpa index itr:", i)
                if((name[i] >= "A" and name[i] <= "z") or (name[i] >= "1" and name[i] <= "9")):
                    Ralphaindex = i
                    print("Alphabet found from Right at:", Ralphaindex)
                    break
                
            #Ralpa > rindex   (should be ideally)   if opposite then there's a white space between 0th index and nth text chharcter
            #Lalpha < lindex   (should be ideally)  if opposite then there's a white space between last index and nth text chharcter

            Rspace = (Ralphaindex < rindex)
            Lspace = (Lalphaindex > lindex)

            if(Rspace == True):
                print("(" + name + ") There's white space in the back, BAD FORMAT WARNING")
                name = name[0:Ralphaindex+1]
                print("After popping the right space (" + name + ")")

            if(Lspace == True):
                print("(" + name + ") There's a white space infront, BAD FORMAT WARNING")
                name = name[Lalphaindex:]
                print("After popping the left space (" + name + ")")
                print("Final content of Name (" + name + ")")

        print("\x1b[31m_________end of filter_____\x1b[0m\n\n")
        return name

