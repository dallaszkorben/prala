import configparser
import os
import gettext

INI_FILE_NAME="config.ini"

DEFAULT_LANGUAGE="en"
DEFAULT_BASE_LANGUAGE="en"
DEFAULT_LEARNING_LANGUAGE="sv"
DEFAULT_SAY_OUT=True
DEFAULT_SHOW_PATTERN=True
DEFAULT_SHOW_NOTE=True

LOCALES_DIR='locales'
PACKAGE_NAME='prala'    

class Translation(object):
    """
    This singleton handles the translation.
    The object is created by calling the get_instance() method.
    The language is defined in the ini file's [language] section as "language" key
    The _() method is to get back the translated string.
    If the translation file or the translation in the file is not there then the 
    string in the parameter will we used instead of raiseing error
    Using this Object directly is not necessary. There is a _() method defined out of the class
    which creates the instance and calls the _() method.
    """
    __instance = None    
 
    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance)
        return inst
        
    def __init__(self):
        self.property=Property.get_instance()
        localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), LOCALES_DIR)
        self.translate = gettext.translation(PACKAGE_NAME, localedir=localedir, languages=self.__get_language_code(), fallback=True)

    def __get_language_code(self):
	    return [self.property.get('language', 'language', DEFAULT_LANGUAGE)]

    def _(self, text):
        return self.translate.gettext(text)

def _(text):
    return Translation.get_instance()._(text)

class Enum(object):   
   
    def __init__(self, **named_values):
        self.named_values=named_values
        for k, v in named_values.items():
            exec("self.%s = %s" % (k, v))

    def size(self):
        return len(self.named_values)

class Property(object):
    """
    This singleton handles the package's ini file.
    The object is created by calling the get_instance() method.
    If the ini file is not existing then it will be generated with default values

    It is possible to get a string value of a key by calling the get() method
    If the key is not existing then it will be generated with default value
    The get_boolean() method is to get the boolean values.

    update() method is to update a value of a key. If the key is not existing
    then it will be generated with default value
    """
    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance)     
        return inst
        
    def __init__(self):
        #self.file=file
        self.file=os.path.join(os.getcwd(), INI_FILE_NAME)
        self.parser = configparser.RawConfigParser()

    def __write_file(self):
        with open(self.file, 'w') as configfile:
            self.parser.write(configfile)

    def get(self, section, key, default_value):
        if not os.path.exists(self.file):
            self.parser[section]={key: default_value}
            self.__write_file()
        self.parser.read(self.file)

        try:
            result=self.parser.get(section,key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.update(section, key, default_value)
            result=self.parser.get(section,key)

        return result

    def get_boolean(self, section, key, default_value):
        if not os.path.exists(self.file):
            self.parser[section]={key: default_value}
            self.__write_file()
        self.parser.read(self.file)

        try:
            result=self.parser.getboolean(section,key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            self.update(section, key, default_value)
            result=self.parser.get(section,key)

        return result

    def update(self, section, key, value):
        if not os.path.exists(self.file):
            self.parser[section]={key: value}        
        else:
            self.parser.read(self.file)
            try:
                # if no section -> NoSectionError | if no key -> Create it
                self.parser.set(section, key, value)
            except configparser.NoSectionError:
                self.parser[section]={key: value}

        self.__write_file()

    def __str__(self):
        self.parser.read(self.file)
        out=[]
        for s, vs in self.parser.items():
            out += ["[" + s + "]"] + ["  " + k + "=" + v for k, v in vs.items()]
        return "\n".join(out)


def xzip(a, b, string_filler=""):
    """
    Returns a list of tuples, where the i-th tuple contains the i-th element 
    from each of the argument sequences or iterables. 
    If the argument sequences are of unequal lengths, then the shorter list
    will be complemented
    """
    #zipped_list= list(zip( 
    #a + [" "*len(i) for i in b][len(a):], 
    #b + [" "*len(i) for i in a][len(b):] ) )
    zipped_list= list(zip( 
    a + ["" for i in b][len(a):], 
    b + ["" for i in a][len(b):] ) )

    if string_filler:
        zipped_list = [ (
            str(i[0]) + (string_filler*len(str(i[1])))[len(str(i[0])):] , 
            str(i[1]) + (string_filler*len(str(i[0])))[len(str(i[1])):] ) 
                for i in zipped_list]
    return zipped_list
#file=os.path.join(os.getcwd(),'config.inii')
#p=Property(file)
#p.update("language4", "newe#from iso3166 import countries
