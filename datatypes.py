'''
Created on 14 feb 2016

@author: ghedinip
'''
from __future__ import absolute_import, division, print_function, unicode_literals

__all__ = ["DateTime", "Date", "Time", "Boolean", "Period", "Address", "Params", "ALL"]

import json
import dateutil.parser
import re
from datetime import time, date, datetime

try:
    basestring
except NameError:
    basestring = str
    
class Boolean(object):
    '''
    FHIR Time Type
    '''

    def __new__(self, json = None):
        '''
        FHIR Reference __new__
        '''
        if json == None:
            return None
        else:
            return object.__new__(self)
        
    def __init__(self, json = None):
        '''
        Bool Constructor
        '''
        str_arg = json
        if isinstance(str_arg, basestring):
            if (str_arg == "true") or (str_arg == "True"):
                self.__bool = True
            else:
                self.__bool = False
        elif isinstance(str_arg, bool):
                self.__bool = str_arg
        else:
            print("FHIR Boolean: Bad Parameter")
            self.__bool = None

    @property
    def json(self):
        '''
        json
        '''
        if self.__bool != None:
            return self.__bool
        else:
            return None
            
    def __repr__(self):
        if self.__bool != None:
            if self.__bool:
                return "True"
            else:
                return "False"
        else:
            return None

class Date(object):
    '''
    FHIR Date Type
    '''

    def __new__(self, json = None, year = None, month = None, day = None):
        '''
        Date Constructor
        '''
        if (json == None) and (year == None) and (month == None) and (day == None):
            return None
        else:
            return object.__new__(self)
            
    def __init__(self, json = None, year = None, month = None, day = None):
        '''
        Date Constructor
        '''
        if json != None:            
            str_arg = json
            if isinstance(str_arg, basestring): 
                self.__date = dateutil.parser.parse(str_arg).date()
                self.year = self.__date.year
                self.month = self.__date.month
                self.day = self.__date.day                
            else:
                print("FHIR Date: Bad Parameter")
                print(str(json) + " - " +str(year) + " - " +str(month) + " - " +str(day))
                self.__date = None
                self.year = None
                self.month = None
                self.day = None                
        else:    
            if year:
                self.year = year
            else:
                self.year = 0
            if month:
                self.month = month
            else:
                self.month = 0
            if day:
                self.day = day
            else:
                self.day = 0
            self.__date = date(self.year, self.month, self.day)
    
    @property
    def json(self):
        '''
        json
        '''
        self.__date = date(self.year, self.month, self.day)
        return self.__date.isoformat()
    
    def __repr__(self):
        return self.json
    
class DateTime(object):
    '''
    FHIR DateTime Type
    '''

    def __new__(self, json = None, year = None, month = None, day = None, hour = None, minute = None, second = None, microsec = None, tz = None):
        '''
        DateTime Constructor
        '''
        if (json == None) and (year == None) and (month == None) and (day == None) and \
            (hour == None) and (minute == None) and (second == None) and (microsec == None) and (tz == None):
            return None
        else:
            return object.__new__(self)


    def __init__(self, json = None, year = None, month = None, day = None, hour = None, minute = None, second = None, microsec = None, tz = None):
        '''
        DateTime Constructor
        '''
        if  json != None:  
            str_arg = json
            if isinstance(str_arg, basestring):
                self.__dt = dateutil.parser.parse(str_arg)
                self.year = self.__dt.date().year
                self.month = self.__dt.date().month
                self.day = self.__dt.date().day
                self.hour = self.__dt.time().hour
                self.minute = self.__dt.time().minute
                self.second = self.__dt.time().second
                self.microsec = self.__dt.time().microsecond
                self.tz = self.__dt.tzinfo
                self.__datetime = datetime(self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsec, self.tz)
            else:
                print("FHIR DateTime: Bad Parameter")
                self.year = None
                self.month = None
                self.day = None
                self.hour = None
                self.minute = None
                self.second = None
                self.microsec = None
                self.tz = None
                self.__datetime = None
        else:
            if year:
                self.year = year
            else:
                self.year = 0
            if month:
                self.month = month
            else:
                self.month = 0
            if day:
                self.day = day
            else:
                self.day = 0
            if hour:
                self.hour = hour
            else:
                self.hour = 0
            if minute:
                self.minute = minute
            else:
                self.minute = 0
            if second:
                self.second = second
            else:
                self.second = 0
            if microsec:
                self.microsec = microsec
            else:
                self.microsec = 0
            self.tz = tz
            self.__datetime = datetime(self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsec, self.tz)
    
    @property
    def json(self):
        '''
        json
        '''
        self.__datetime = datetime(self.year, self.month, self.day, self.hour, self.minute, self.second, self.microsec, self.tz)
        return self.__datetime.isoformat()
        
    def __repr__(self):
        return self.json
    
class Time(object):
    '''
    FHIR Time Type
    '''

    def __new__(self, json = None, hour = None, minute = None, second = None, microsec = None):
        '''
        Time Constructor
        '''
        if (json == None) and (hour == None) and (minute == None) and (second == None) and (microsec == None):
            return None
        else:
            return object.__new__(self)

    def __init__(self, json = None, hour = None, minute = None, second = None, microsec = None):
        '''
        Time Constructor
        '''
        if  json != None:  
            str_arg = json
            if isinstance(str_arg, basestring):
                #self.datetime = datetime.__new__(self, *dateutil.parser.parse(str_arg).timetuple()[0:6])
                self.__ti = dateutil.parser.parse(str_arg).time()
                self.hour = self.__ti.hour
                self.minute = self.__ti.minute
                self.second = self.__ti.second
                self.microsec = self.__ti.microsecond
                self.__time = time(self.hour, self.minute, self.second, self.microsec)
            else:
                print("FHIR DateTime: Bad Parameter")
                self.hour = None
                self.minute = None
                self.second = None
                self.microsec = None
                self.__datetime = None
        else:
            if hour:
                self.hour = hour
            else:
                self.hour = 0
            if minute:
                self.minute = minute
            else:
                self.minute = 0
            if second:
                self.second = second
            else:
                self.second = 0
            if microsec:
                self.microsec = microsec
            else:
                self.microsec = 0
            self.__time = time(self.hour, self.minute, self.second, self.microsec)
    
    @property
    def json(self):
        '''
        json
        '''
        self.__time = time(self.hour, self.minute, self.second, self.microsec)
        return self.__time.isoformat()
        
    def __repr__(self):
        return self.json

class Period(object):
    '''
    FHIR Period Object
    '''
    def __add(self, key):
        if key in self.__json:
            #return DateTime(self.__json[key])
            return self.__json[key]
        else:
            return None

    def __new__(self, json = None, start = None, end = None):
        '''
        FHIR Period __new__
        '''
        if (json == None) and (start == None) and (end == None):
            return None
        else:
            return object.__new__(self)

    def __init__(self, json = None, start = None, end = None):
        '''
        FHIR Period constructor
        '''
        if json:
            self.__json = json
            self.start = DateTime(self.__add('start'))
            self.end = DateTime(self.__add('end'))
        else:
            self.start = DateTime(start)
            self.end = DateTime(end)
            self.__json = self.json

    @property
    def json(self):
        self.__json = {}
        if self.start:
            self.__json['start'] = self.start.json
        if self.end:
            self.__json['end'] = self.end.json
        return self.__json
        
    def __repr__(self):
        '''
        FHIR Period string Representation
        '''
        return json.dumps(self.json, indent=4, separators=(',', ': '))

class Address(object):
    '''
    FHIR Address object
    '''
    def __add(self, key):
        if key in self.__json:
            return self.__json[key]
        else:
            return None
 
    def __add_list(self, key):
        if key in self.__json:
            list_to_add = []
            for obj in self.__json[key]:
                list_to_add.append(obj) 
            return list_to_add
        else:
            return None

    def __get_list(self, var):
        if var == None:
            return None
        else:
            list_obj = []
            for obj in var:
                if isinstance(obj, dict) or isinstance(obj, list) or isinstance(obj, basestring):
                    list_obj.append(obj)
                else:
                    list_obj.append(obj.json)
            return list_obj
 
    def __new__(self, json = None, use = None, type_ = None, text = None, line = None, city = None,\
                district = None, state = None, postalCode = None, country = None, period = None):
        '''
        FHIR Address __new__
        '''
        if (json == None) and (use == None) and (type_ == None) and (text == None) and\
            (line == None) and (city == None) and (district == None) and\
            (state == None) and (postalCode == None) and (country == None) and\
            (period == None):
            return None
        else:
            return object.__new__(self)
        
    def __init__(self, json = None, use = None, type_ = None, text = None, line = None, city = None,\
                district = None, state = None, postalCode = None, country = None, period = None):
        '''
        FHIR Address constructor
        '''
        if json:
            self.__json = json
            self.use = self.__add('use')
            self.type = self.__add('type')
            self.text = self.__add('text')
            self.line = self.__add_list('line')
            self.city = self.__add('city')
            self.district = self.__add('district')
            self.state = self.__add('state')
            self.postalCode = self.__add('postalCode')
            self.country = self.__add('country')
            self.period = Period(self.__add('period'))

        else:
            self.use = use
            self.type = type_
            self.text = text
            self.line = line
            self.city = city
            self.district = district
            self.state = state
            self.postalCode = postalCode
            self.country = country
            self.period = Period(period)
            self.__json = self.json
    
    @property
    def json(self):
        self.__json = {}
        if self.use:
            self.__json['use'] = self.use
        if self.type:
            self.__json['type'] = self.type
        if self.text:
            self.__json['text'] = self.text
        if self.line:
            self.__json['line'] = self.__get_list(self.line)
        if self.city:
            self.__json['city'] = self.city
        if self.district:
            self.__json['district'] = self.district
        if self.state:
            self.__json['state'] = self.state
        if self.postalCode:
            self.__json['postalCode'] = self.postalCode
        if self.country:
            self.__json['country'] = self.country
        if self.period:
            self.__json['period'] = self.period.json
        return self.__json
        
    def __repr__(self):

        '''
        FHIR Address string Representation
        '''

        return json.dumps(self.json, indent=4, separators=(',', ': '))
"""
class HumanName(object):
    '''
    FHIR HumanName Object
    '''

    def __add(self, key):
        if key in self.__json:
            return self.__json[key]
        else:
            return None

    def __add_list(self, key):
        if key in self.__json:
            list_to_add = []
            for obj in self.__json[key]:
                list_to_add.append(obj) 
            return list_to_add
        else:
            return None

    def __get_list(self, var):
        if var == None:
            return None
        else:
            list_obj = []
            for obj in var:
                if isinstance(obj, dict) or isinstance(obj, list) or isinstance(obj, basestring):
                    list_obj.append(obj)
                else:
                    list_obj.append(obj.json)
            return list_obj
 
    def __new__(self, json = None, use = None, text = None, family = None, given = None, \
                prefix = None, suffix = None, period = None):
        '''
        FHIR HumaName __new__
        '''
        if (json == None) and (use == None) and (text == None) and (family == None) and \
            (given == None) and (prefix == None) and (suffix == None)  and (period == None):
            return None
        else:
            return object.__new__(self)
        
    def __init__(self, json = None, use = None, text = None, family = None, given = None, \
                prefix = None, suffix = None, period = None):
        '''
        FHIR HumanName constructor
        '''
        if json:
            self.__json = json
            self.use = self.__add('use')
            self.text = self.__add('text')
            self.family = self.__add_list('family')
            self.given = self.__add_list('given')
            self.prefix = self.__add_list('prefix')
            self.suffix = self.__add_list('suffix')
            self.period = Period(self.__add('period'))
        else:
            self.use = use
            self.text = text
            self.family = family
            self.given = given
            self.prefix = prefix
            self.suffix = suffix
            self.period = Period(period)
            self.__json = self.json

    @property
    def json(self):
        self.__json = {}
        if self.use:
            self.__json['use'] = self.use
        if self.text:
            self.__json['text'] = self.text
        if self.family:
            self.__json['family'] = self.__get_list(self.family)
        if self.given:
            self.__json['given'] = self.__get_list(self.given)
        if self.prefix:
            self.__json['prefix'] = self.__get_list(self.prefix)
        if self.suffix:
            self.__json['suffix'] = self.__get_list(self.suffix)
        if self.period:
            self.__json['period'] = self.period.json
        return self.__json

    def __repr__(self):
        '''
        FHIR HumanName string Representation
        '''
        return json.dumps(self.json, indent=4, separators=(',', ': '))
"""
class ALL(object):
    '''
    search on all Resources Object
    Auxiliary Object to deal with queries
    '''    
    class __Oper(object):
        '''
        Oper Object
        Auxiliary Object to deal with queries
        '''
        
        def __repr(self, fhir_obj):
            '''
            Auxiliary function to represent String without eclosure
            '''
            if isinstance(fhir_obj, basestring):
                return fhir_obj
            else:
                return repr(fhir_obj)
            
        def __operandNULL(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: self.__repr(fhir_obj)}
    
        def __operandEQ(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "eq" + self.__repr(fhir_obj)}
        
        def __operandNE(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "ne" + self.__repr(fhir_obj)}
        
        def __operandGT(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "gt" + self.__repr(fhir_obj)}
        
        def __operandLT(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "lt" + self.__repr(fhir_obj)}
        
        def __operandGE(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "ge" + self.__repr(fhir_obj)}
        
        def __operandLE(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "le" + self.__repr(fhir_obj)}
        
        def __operandSA(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "sa" + self.__repr(fhir_obj)}
        
        def __operandEB(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "eb" + self.__repr(fhir_obj)}
        
        def __operandAP(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param: "ap" + self.__repr(fhir_obj)}
    
        def __operandContains(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":contains": self.__repr(fhir_obj)}
    
        def __operandExact(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":exact": self.__repr(fhir_obj)}
    
        def __operandText(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":text": self.__repr(fhir_obj)}
    
        def __operandAbove(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":above": self.__repr(fhir_obj)}
    
        def __operandBelow(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":below": self.__repr(fhir_obj)}
    
        def __operandNot(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":not": self.__repr(fhir_obj)}
    
        def __operandNotIn(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":not-in": self.__repr(fhir_obj)}
    
        def __operandIn(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":in": self.__repr(fhir_obj)}
    
        def __operandMissing(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {self.__param + ":missing": self.__repr(fhir_obj)}
    
        def __sort_asc(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {"_sort:asc": self.__repr(fhir_obj)}
    
        def __sort_desc(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            # la chiave del dictionary e' cio' che viene prima dell'uguale
            # self.__repr(fhir_obj) e' il valore immesso da linea di comando
            # self.param e' ad esempio name, cioe' l'attributo di ricerca di cui gestire il il modificatore e il valore
            return {"_sort:desc": self.__repr(fhir_obj)}
    
        def __count(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {"_count": self.__repr(fhir_obj)}
    
        def __elements(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {"_elements": self.__repr(fhir_obj)}
    
        def __contained(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {"_contained": self.__repr(fhir_obj)}
    
        def __containedType(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {"_containedType": self.__repr(fhir_obj)}
    
        def __summary_true(self):
            '''
            operand: Get fhir Object representation
            '''
            return {"_summary": "true"}
    
        def __summary_text(self):
            '''
            operand: Get fhir Object representation
            '''
            return {"_summary": "text"}
    
        def __summary_data(self):
            '''
            operand: Get fhir Object representation
            '''
            return {"_summary": "data"}
    
        def __summary_count(self):
            '''
            operand: Get fhir Object representation
            '''
            return {"_summary": "count"}
    
        def __summary_false(self):
            '''
            operand: Get fhir Object representation
            '''
            return {"_summary": "false"}
    
        def __include(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {"_include": self.__repr(fhir_obj)}
    
        def __revinclude(self, fhir_obj):
            '''
            operand: Get fhir Object representation
            '''
            return {"_revinclude": self.__repr(fhir_obj)}
    
        def __init__(self, param, value):
            '''
            Oper Constructor
            '''
            self.__param = param
            
            if (value == "number") or (value == "date") or (value == "quantity"):
                str_op = [("Missing", self.__operandMissing), ("EQ", self.__operandEQ), ("NE", self.__operandNE), ("GT", self.__operandGT),
                          ("LT", self.__operandGT), ("GE", self.__operandGE), ("LE", self.__operandLE),
                          ("SA", self.__operandSA), ("EB", self.__operandEB), ("AP", self.__operandAP)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "reference"):
                str_op = [("Missing", self.__operandMissing), ("EQ", self.__operandNULL)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "sort"):
                # value e' il tipo del parametro di ricerca, che da' luogo alle operazioni possibili
                # nel caso il tipo sia sort, sono disponibili i modificatori asc e desc
                # che compaiono come tipo di operazioen possibile dopo l'attributo sort  
                str_op = [("asc", self.__sort_asc), ("desc", self.__sort_desc)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "count"):
                str_op = [("EQ", self.__count)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "elements"):
                str_op = [("EQ", self.__elements)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "contained"):
                str_op = [("EQ", self.__contained)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "containedType"):
                str_op = [("EQ", self.__containedType)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "summary"):
                str_op = [("TrueOp", self.__summary_true), ("TextOp", self.__summary_text), ("DataOp", self.__summary_data),
                          ("CountOp", self.__summary_count), ("FalseOp", self.__summary_false)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "include"):
                str_op = [("EQ", self.__include)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "revinclude"):
                str_op = [("EQ", self.__revinclude)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "token"):
                str_op = [("EQ", self.__operandNULL), ("Text", self.__operandText), ("Not", self.__operandNot), ("Above", self.__operandAbove),
                          ("Below", self.__operandBelow), ("In", self.__operandIn), ("Not_in", self.__operandNotIn), ("Missing", self.__operandMissing)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "string"):
                str_op = [("EQ", self.__operandNULL), ("Contains", self.__operandContains), ("Exact", self.__operandExact), ("Text", self.__operandText),
                          ("Missing", self.__operandMissing)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "text"):
                str_op = [("In", self.__operandIn), ("Not_in", self.__operandNotIn), 
                          ("Missing", self.__operandMissing), ("Above", self.__operandAbove), ("Below", self.__operandBelow)]
                for par in str_op:
                    setattr(self, par[0], par[1])
            elif (value == "uri"):
                str_op = [("EQ", self.__operandNULL), ("Above", self.__operandAbove), ("Below", self.__operandBelow),
                          ("Missing", self.__operandMissing)]
                for par in str_op:
                    setattr(self, par[0], par[1])

    id_ = __Oper("_id","string")
    lastUpdated_ = __Oper("_lastUpdated","date")
    tag_ = __Oper("_tag","token")
    profile_ = __Oper("_profile","uri")
    security_ = __Oper("_security","token")
    text_ = __Oper("_text","string")
    content_ = __Oper("_content","string")
    list_ = __Oper("_list","string")
    query_ = __Oper("_query","string")
    sort_ = __Oper("_sort","sort")
    count_ = __Oper("_count", "count")
    elements_ = __Oper("_elements", "elements")
    contained_ = __Oper("_contained", "contained")
    containedType_ = __Oper("_containedType", "containedType")
    include_ = __Oper("_include", "include")
    revinclude_ = __Oper("_revinclude", "revinclude")
    summary_ = __Oper("_summary", "summary")

    def __init__(self):
        '''
        search_cond Constructor
        '''
        
class Params(object):
    '''
    Params Object
    Auxiliary Object to deal with queries
    '''
    def __norm(self, str_in):
        #str_out = re.sub("_", "C_", str_in)
        #str_out = re.sub("-", "_", str_out)
        str_out = re.sub("-", "_", str_in)
        return str_out
    
    def __new__(self, *args, **kwargs):
        '''
        FHIR Period __new__
        '''
        if args[0] == None:
            return None
        else:
            return object.__new__(self)

    def __init__(self, params, resource):
        '''
        Params Constructor
        '''
        self.id_ = Oper("_id","string")
        self.lastUpdated_ = Oper("_lastUpdated","date")
        self.tag_ = Oper("_tag","token")
        self.profile_ = Oper("_profile","uri")
        self.security_ = Oper("_security","token")
        self.text_ = Oper("_text","string")
        self.content_ = Oper("_content","string")
        self.list_ = Oper("_list","string")
        self.query_ = Oper("_query","string")
        for par in params:
            setattr(self, self.__norm(par[0]), Oper(par[0], par[1], resource))
        
class Oper(object):
    '''
    Oper Object
    Auxiliary Object to deal with queries
    '''
    
    def __repr(self, fhir_obj, full=None):
        '''
        Auxiliary function to represent String without eclosure
        '''
        if isinstance(fhir_obj, basestring):
            return fhir_obj
        else:
            return repr(fhir_obj)
        
    def __operandNULL(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: self.__repr(fhir_obj)}
        else:    
            return {self.__param: self.__repr(fhir_obj)}

    def __operandEQ(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "eq" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "eq" + self.__repr(fhir_obj)}
    
    def __operandNE(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "ne" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "ne" + self.__repr(fhir_obj)}
    
    def __operandGT(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "gt" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "gt" + self.__repr(fhir_obj)}
    
    def __operandLT(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "lt" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "lt" + self.__repr(fhir_obj)}
    
    def __operandGE(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "ge" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "ge" + self.__repr(fhir_obj)}
    
    def __operandLE(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "le" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "le" + self.__repr(fhir_obj)}
    
    def __operandSA(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "sa" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "sa" + self.__repr(fhir_obj)}
    
    def __operandEB(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "eb" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "eb" + self.__repr(fhir_obj)}
    
    def __operandAP(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param: "ap" + self.__repr(fhir_obj)}
        else:
            return {self.__param: "ap" + self.__repr(fhir_obj)}

    def __operandContains(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":contains": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":contains": self.__repr(fhir_obj)}

    def __operandExact(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":exact": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":exact": self.__repr(fhir_obj)}

    def __operandText(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":text": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":text": self.__repr(fhir_obj)}

    def __operandAbove(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":above": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":above": self.__repr(fhir_obj)}

    def __operandBelow(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":below": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":below": self.__repr(fhir_obj)}

    def __operandNot(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":not": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":not": self.__repr(fhir_obj)}

    def __operandNotIn(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":not-in": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":not-in": self.__repr(fhir_obj)}

    def __operandIn(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":in": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":in": self.__repr(fhir_obj)}

    def __operandMissing(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        if full:
            return {self.__res_param + ":missing": self.__repr(fhir_obj)}
        else:
            return {self.__param + ":missing": self.__repr(fhir_obj)}

    def __sort_asc(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_sort:asc": self.__repr(fhir_obj)}

    def __sort_desc(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        # la chiave del dictionary e' cio' che viene prima dell'uguale
        # self.__repr(fhir_obj) e' il valore immesso da linea di comando
        # self.param e' ad esempio name, cioe' l'attributo di ricerca di cui gestire il il modificatore e il valore
        return {"_sort:desc": self.__repr(fhir_obj)}

    def __count(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_count": self.__repr(fhir_obj)}

    def __elements(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_elements": self.__repr(fhir_obj)}

    def __contained(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_contained": self.__repr(fhir_obj)}

    def __containedType(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_containedType": self.__repr(fhir_obj)}

    def __summary(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_summary": self.__repr(fhir_obj)}

    def __include(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_include": self.__repr(fhir_obj)}

    def __revinclude(self, fhir_obj, full=None):
        '''
        operand: Get fhir Object representation
        '''
        return {"_revinclude": self.__repr(fhir_obj)}
        
    def __init__(self, param, value, resource=None):
        '''
        Oper Constructor
        '''
        self.__param = param
        if resource:
            self.__res_param = resource + "." + param
        else:
            self.__res_param = param
        
        if (value == "number") or (value == "date") or (value == "quantity"):
            str_op = [("Missing", self.__operandMissing), ("EQ", self.__operandEQ), ("NE", self.__operandNE), ("GT", self.__operandGT),
                      ("LT", self.__operandGT), ("GE", self.__operandGE), ("LE", self.__operandLE),
                      ("SA", self.__operandSA), ("EB", self.__operandEB), ("AP", self.__operandAP)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "reference"):
            str_op = [("Missing", self.__operandMissing), ("EQ", self.__operandNULL)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "sort"):
            # value e' il tipo del parametro di ricerca, che da' luogo alle operazioni possibili
            # nel caso il tipo sia sort, sono disponibili i modificatori asc e desc
            # che compaiono come tipo di operazioen possibile dopo l'attributo sort  
            str_op = [("asc", self.__sort_asc), ("desc", self.__sort_desc)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "count"):
            str_op = [("EQ", self.__count)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "elements"):
            str_op = [("EQ", self.__elements)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "contained"):
            str_op = [("EQ", self.__contained)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "containedType"):
            str_op = [("EQ", self.__containedType)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "summary"):
            str_op = [("EQ", self.__summary)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "include"):
            str_op = [("EQ", self.__include)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "revinclude"):
            str_op = [("EQ", self.__revinclude)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "token"):
            str_op = [("EQ", self.__operandNULL), ("Text", self.__operandText), ("Not", self.__operandNot), ("Above", self.__operandAbove),
                      ("Below", self.__operandBelow), ("In", self.__operandIn), ("Not_in", self.__operandNotIn), ("Missing", self.__operandMissing)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "string"):
            str_op = [("EQ", self.__operandNULL), ("Contains", self.__operandContains), ("Exact", self.__operandExact), ("Text", self.__operandText),
                      ("Missing", self.__operandMissing)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "text"):
            str_op = [("In", self.__operandIn), ("Not_in", self.__operandNotIn), 
                      ("Missing", self.__operandMissing), ("Above", self.__operandAbove), ("Below", self.__operandBelow)]
            for par in str_op:
                setattr(self, par[0], par[1])
        elif (value == "uri"):
            str_op = [("EQ", self.__operandNULL), ("Above", self.__operandAbove), ("Below", self.__operandBelow),
                      ("Missing", self.__operandMissing)]
            for par in str_op:
                setattr(self, par[0], par[1])

    def __repr__(self):
        return self.__param
