import configparser
import os

class Enum(object):   
   
    def __init__(self, **named_values):
        self.named_values=named_values
        for k, v in named_values.items():
            exec("self.%s = %s" % (k, v))

    def size(self):
        return len(self.named_values)

class Property(object):

    def __init__(self, file):
        self.file=file
        self.parser = configparser.RawConfigParser()

    def write_file(self):
        with open(self.file, 'w') as configfile:
            self.parser.write(configfile)

    def get(self, section, key, default_value):
        if not os.path.exists(self.file):
            self.parser[section]={key: default_value}
            self.write_file()
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
            self.write_file()
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

        self.write_file()

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
