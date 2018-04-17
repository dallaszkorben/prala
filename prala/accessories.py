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

#file=os.path.join(os.getcwd(),'config.inii')
#p=Property(file)
#p.update("language4", "newe#from iso3166 import countries
