'''
Created on 06 gen 2016

@author: ghedinip

REST interface to HL7 FHIR infrastructure

- mettere il verbo GET, PUT, ecc accanto a URL
- verificare l'autenticazione basic
- migliorare la gestione degli errori interpretando i codici di ritorno dal
     server FHIR

Ultimo aggiornamento 06/01/2016

'''

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import json
import sys
from enum import Enum
from generated import OperationOutcome

# conditional import to comply with python3
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
try:
    basestring
except NameError:
    basestring = str

def decode_obj(obj):
    '''
         It encodes the bytearray in str
    '''
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, list):
        out_list = []
        for elem in obj:
            out_list.append(decode_obj(elem))
        return out_list
    elif isinstance(obj, dict):
        out_dict = {}
        for key in obj:
            out_dict[decode_obj(key)] = decode_obj(obj[key])
        return out_dict           
    else:
        return obj           

class Verbosity(Enum):
    '''
       Enumeration class of verbosity level
    '''
    low = 0
    medium = 1
    high = 2

class OperationOutcomes(object):
    def __init__(self, response):
        '''
        Aggregator of OperationOutcome
        '''
        """
        self.outcomes = []
        extra_obj = ''
        for obj in response:
            # This odd concatenation introducted to deal with an error in response of the test site
            if (len(obj.lstrip()) > 0) and (obj.lstrip()[0] == '<'):
                self.outcomes.append(obj)
            else:
                if (obj == '{\r\n') or (obj == '{\n'):
                    extra_obj = obj
                    continue
                if len(obj.lstrip()) > 0:
                    self.outcomes.append(OperationOutcome(eval(extra_obj + obj)))    
                if (obj == '{\r\n') or (obj == '{\n'):
                    extra_obj = ''
        """
        self.json = ""
        for obj in response:
            print(obj)
            self.json += obj
        if not ((len(obj.lstrip()) > 0) and (obj.lstrip()[0] == '<')):
            self.json = eval(self.json)            
        
    def __repr__(self):
        '''
             Get the object representation
        '''
        """
        out_str = ""
        for obj in self.outcomes:
            out_str += obj.__repr__()
        return out_str
        """
        return str(self.json)

class Resp(object):
    '''
         Class to decode the FHIR answers
    '''
    def __init__(self, response=None, service_resp=None, response_code=None, response_type = "json"):
        '''
        Resp constructor
        '''
        self.__path_list = []
        if response:
            #if isinstance(response, (basestring, list)):
            #    str_response = str(response)
            #else:
            #    str_response = response.decode('utf-8')
            str_response = decode_obj(response)
        else:
            str_response = None
        if service_resp:
            #if isinstance(service_resp, basestring):
            #    str_service_resp = str(service_resp)
            #else:
            #    str_service_resp = service_resp.decode('utf-8')
            str_service_resp = decode_obj(service_resp)
        else:
            str_service_resp = None
            
        self.__resp = str_response
        if response_type == "error":
            self.__resp_obj = OperationOutcomes(str_response)
            self.__service_resp = str_service_resp
        else:
            if str_response:
                if response_type == "json":
                    self.__resp_obj = json.loads(str_response)
                else:
                    self.__resp_obj = str_response
            else:
                self.__resp_obj = None
            self.__service_resp = None
            if str_response and str_service_resp:
                self.__service_resp = self.__resp + str('\n') + str_service_resp
            if str_response and (not str_service_resp):
                self.__service_resp = self.__resp
            if (not str_response) and str_service_resp:
                self.__service_resp = str_service_resp

        self.__response_code = response_code

    def __path(self, obj_to_parse, path, path_list, verbose=False):
        '''
            Auxiliary function to parse the response obj
        '''
        if not (isinstance(obj_to_parse, list) or isinstance(obj_to_parse, dict)):
            path_list.append(path)
            return True

        if isinstance(obj_to_parse, list):
            counter = 0
            for obj in obj_to_parse:
                if verbose:
                    new_path = "[%d]" % counter
                    counter += 1
                    self.__path(obj, path + new_path,
                                path_list, verbose=verbose)
                else:
                    # Not Verbose
                    new_path = "[%d]" % (len(obj_to_parse) - 1)
                    self.__path(obj, path + new_path,
                                path_list, verbose=verbose)

        if isinstance(obj_to_parse, dict):
            for key in obj_to_parse:
                new_path = "[\"%s\"]" % key
                self.__path(obj_to_parse[key], path + new_path,
                            path_list, verbose=verbose)

    def paths(self, verbose=False):
        '''
            Show the structure of the responseObj
            it returns None if the Obj is None
        '''
        path_list = []
        if not self.__resp_obj:
            return None
        else:
            self.__path_list = self.__path(self.__resp_obj,
                                           "",
                                           path_list,
                                           verbose=verbose)
            return sorted(list(set(path_list)))

    def is_bundle(self):
        '''
             Tests if the response is a Bundle
        '''
        if self.__resp_obj:
            if self.__resp_obj["resourceType"] == "Bundle":
                return True
            else:
                return False
        else:
            return None

    def total(self):
        '''
             Get the Total number of entries of the Bundle
        '''
        if self.is_bundle():
            return int(self.__resp_obj["total"])
        else:
            return None

    def obj(self):
        '''
             Get the response object
        '''
        return self.__resp_obj

    def entry(self, index):
        '''
             Get a specific entry in the bundle
        '''
        if self.is_bundle():
            return self.__resp_obj["entry"][index]
        else:
            return None

    def entry_list(self):
        '''
             Get the entire Entry List, usefull to iterate on it
        '''
        if self.is_bundle():
            return self.__resp_obj["entry"]
        else:
            return None

    def entry_resource(self, index):
        '''
             Get the resource of a specific entry in the bundle
        '''
        if self.is_bundle():
            return self.__resp_obj["entry"][index]["resource"]
        else:
            return None

    def entry_full_url(self, index):
        '''
             Get the address of the resource of a specific entry in the bundle
        '''
        if self.is_bundle():
            return self.__resp_obj["entry"][index]["fullUrl"]
        else:
            return None

    def http_output(self):
        '''
             Get the response
        '''
        return self.__resp

    def resp_code(self):
        '''
             Get the response code
        '''
        return self.__response_code

    def __repr__(self):
        '''
             Get the string representation
        '''
        return str(self.__service_resp.encode("ascii", errors="ignore"))


class init_client(object):
    '''
    init_client Object
    '''

    logger = False
    
    def __init__(self, url=None, verb=Verbosity.low, con_log=None, log_file=None):
        '''
            init_client initialization
            - url -> url of the server to connect to. If url==None a default server "http://fhir3.healthintersections.com.au/open/"
                will be used
            - verb -> verbosity level; Verbosity.low | Verbosity.medium | Verbosity.high.
            - con_log -> display also the log in console: True | False | None.
            - log_file -> log file name, ATTENTION USE ABSOLUTE PATH.
        '''
        # create logger with 'fhir.client'
        if not init_client.logger:
            if log_file:
                logging.basicConfig(filename=log_file, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
                init_client.logger = True
            # set console logging
            if con_log:
                if log_file:
                    ch = logging.StreamHandler()
                    ch.setLevel(logging.DEBUG)
                    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                    ch.setFormatter(formatter)
                    logging.getLogger().addHandler(ch)
                else:
                    con_log=False
                
        default_url = "http://fhir3.healthintersections.com.au/open/"
        #default_url = "http://fhir2.healthintersections.com.au/closed/"
        #default_url = "https://fhir-open-api-dstu2.smarthealthit.org/"

        if url:
            self.url = url
        else:
            self.url = default_url
        self.verb = verb
        print("Using FHIR Server: %s" % self.url)
        if self.verb == Verbosity.low:
            print("Verbosity LOW")
        elif self.verb == Verbosity.medium:
            print("Verbosity MEDIUM")
        else:
            print("Verbosity HIGH")
        if log_file:
            print("Logging file: %s" % log_file)
        else:
            print("No logging file.")
        if con_log:
            print("Console logging.")
        else:
            print("No console logging.")

        logging.info('Function init_client completed {0}'.format(self.url))

    def __print_ver(self, text):
        '''
             It prints text with a level of
             detail defined by verbosity level
        '''
        
        logging.info('Function __print_ver')
        
        if self.verb != Verbosity.low:
            # Verbosity True
            print(text)
        else:
            # Verbosity False
            pass
        return

    def __print_args(self, resp):
        '''
             It prints the structure of the response messagge with a level of
             detail defined by verbosity level
        '''
        logging.info('Function __print_args')
        
        if self.verb == Verbosity.low:
            # do nothing
            return
        else:
            # verbosity High or Medium
            if (self.verb == Verbosity.high) and (resp.paths(verbose=True)):
                # Verbosity High
                for path in resp.paths(verbose=True):
                    print(path)
            else:
                # Verbosity False
                if resp.paths(verbose=False):
                    for path in resp.paths(verbose=False):
                        print(path)
        return

    def __url_open(self, request, format_acc="json"):
        '''
             It implements the connection with the server and deals with the answer
        '''
        tmp_str = 'Function __url_open, send to server url={0}'.format(request.get_full_url())
        tmp_str += ' data={0}'.format(request.data)
        tmp_str += ' headers={0}'.format(request.headers)
        logging.info(tmp_str)

        text = None
        response = None
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as err:
            self.__print_ver('The server couldn\'t fulfill the request.')
            text = err.readlines()
            self.__print_ver("Text: %s" % text)
            self.__print_ver("Url: %s" % err.geturl())
            self.__print_ver("Output code: %s %s" % (err.code, err.reason))
            re_obj = Resp(text, "The server couldn\'t fulfill the request. Url: %s Reason: %s" % (err.geturl(), err.reason), err.code, response_type = "error")
            return re_obj
            #return None
        except urllib2.URLError as err:
            self.__print_ver('Failed to reach a server.')
            self.__print_ver("Output code: %s" % err.reason)
            re_obj = Resp({}, "Failed to reach a server. Reason: %s" % (err.reason), None)
            return re_obj
            return None
        else:
            # everything is fine
            if response:
                text = response.read()
                service_resp = "%s Url: %s\n" % (request.get_method(), request.get_full_url())
                service_resp += "Output code: %s\n" % response.getcode()
                self.__print_ver(service_resp)
                logging.info('Function __url_open, read from server={0}'.format(service_resp))
                re_obj = Resp(text, service_resp, response.getcode(), format_acc)
                self.__print_args(re_obj)
                return re_obj
            else:
                service_resp = "%s Url: %s" % (request.get_method(), request.get_full_url())
                self.__print_ver(service_resp)
                return Resp(None, service_resp, response_code=None)

    def read_get(self, search_string, format_acc="json"):
        '''
             It implements the GET method to obtain a REST READ
        '''
        logging.info('Function read_get')
        
        #
        headers = {}
        if format_acc == "json":
            headers["Accept"] = "application/json+fhir"
        else:
            headers["Accept"] = "application/xml+fhir"
        #
        url_to_search = self.url + search_string
        request = urllib2.Request(url_to_search, headers=headers)
        response = self.__url_open(request, format_acc)
        #
        return response

    def read_post(self, search_string, body_string, format_acc="json", header="x-www-form-urlencoded"):
        '''
             It implements the POST method to obtain a REST READ
             
             Input parameters:
             - format_acc, the type of the requested answer from the server
             - header, Content_type parameter in the header of the request to the server
             
             format_acc -> json | xml
             header -> x-www-form-urlencoded | json+fhir | xml+fhir
        '''
        logging.info('Function read_post')
        
        #
        headers = {}
        if format_acc == "json":
            headers["Content-Type"] = "application/%s; charset=UTF-8" % header
            headers["Accept"] = "application/json+fhir; charset=UTF-8"
        else:
            headers["Content-Type"] = "application/%s; charset=UTF-8" % header
            headers["Accept"] = "application/xml+fhir; charset=UTF-8"
        #
        url_to_search = self.url + search_string
        request = urllib2.Request(url_to_search, bytearray(body_string, 'utf-8'), headers=headers)
        #request.get_method = lambda: 'POST'
        response = self.__url_open(request, format_acc)
        #
        return response

    def delete_rest(self, resource, format_acc="json"):
        '''
             It implements the DELETE method to obtain a REST DELETE
        '''
        logging.info('Function delete_rest')
        
        headers = {}
        if format_acc == "json":
            headers["Accept"] = "application/json+fhir"
        else:
            headers["Accept"] = "application/xml+fhir"
        #
        url_to_delete = self.url + resource

        request = urllib2.Request(url_to_delete, headers=headers)
        request.get_method = lambda: 'DELETE'
        response = self.__url_open(request, format_acc)
        #
        return response

    def create_rest(self, resource, body, format_acc="json"):
        '''
             It implements the POST method to obtain a REST CREATE
        '''
        logging.info('Function create_rest')
        
        #
        headers = {}
        headers["Content-Type"] = "application/json+fhir"
        if format_acc == "json":
            headers["Accept"] = "application/json+fhir"
        else:
            headers["Accept"] = "application/xml+fhir"
        #

        url_to_create = self.url + resource
        try:
            if isinstance(body, dict):
                eval_body = eval(str(body))
            else:
                eval_body = eval(body)
        except Exception as inst:
            print(inst)
            sys.exit(1)
            
        request = urllib2.Request(url_to_create,
                                  bytearray(json.dumps(eval_body), 'utf-8'),
                                  headers=headers)
        response = self.__url_open(request, format_acc)
        #
        return response

    def transaction_rest(self, body, format_acc="json"):
        '''
             It implements the POST method to obtain a REST CREATE
        '''
        logging.info('Function transaction_rest, body={0}'.format(body))
        
        #
        headers = {}
        headers["Content-Type"] = "application/json+fhir"
        if format_acc == "json":
            headers["Accept"] = "application/json+fhir"
        else:
            headers["Accept"] = "application/xml+fhir"
        #

        request = urllib2.Request(self.url,
                                  bytearray(json.dumps(body), 'utf-8'),
                                  headers=headers)
        response = self.__url_open(request, format_acc)
        #
        return response

    def update_rest(self, resource, body, format_acc="json"):
        '''
             It implements the PUT method to obtain a REST UPDATE
        '''
        logging.info('Function update_rest')
        
        headers = {}
        headers["Content-Type"] = "application/json+fhir"
        if format_acc == "json":
            headers["Accept"] = "application/json+fhir"
        else:
            headers["Accept"] = "application/xml+fhir"
        #
        # Attenzione: il valore in id deve essere lo stesso specificato nello url
        #

        try:
            if isinstance(body, dict):
                eval_body = eval(str(body))
            else:
                eval_body = eval(body)
        except Exception as inst:
            print(inst)
            sys.exit(1)
            
        url_to_update = self.url + resource
        request = urllib2.Request(url_to_update,
                                  bytearray(json.dumps(eval_body), 'utf-8'),
                                  headers=headers)
        request.get_method = lambda: 'PUT'
        response = self.__url_open(request, format_acc)
        #
        return response

if __name__ == '__main__':
    pass

        