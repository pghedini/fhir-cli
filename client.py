'''
Created on 06 gen 2016

@author: ghedinip

Command Line Interface (CLI) to HL7 FHIR infrastructure

Ultimo aggiornamento 29/12/2015

'''
from __future__ import absolute_import, division, print_function, unicode_literals
__all__ = ['init_client', 'process_message', 'validate_local', 'validate',
           'read', 'vread', 'history', 'conformance',
           'create', 'update', 'search', 'delete', 'Where',
           'read_not_encoded_body', 'meta', 'meta_add', 'meta_delete', 'everything',
           'document', 'translate',
           'DateTime', 'Date', 'Time', 'Boolean', 'Period',
           'HumanName', 'Address', 'ALL',
           'Params', 'Bundle',
           'to_json', 'is_xml', 'xml2json',
           'HIGH', 'MEDIUM', 'LOW', 'ALL_RES',
           'Account',
           'Age',
           'AllergyIntolerance',
           'Annotation',
           'Appointment',
           'AppointmentResponse',
           'Attachment',
           'AuditEvent',
           'BackboneElement',
           'Basic',
           'Binary',
           'BodySite',
           'Bundle',
           'CarePlan',
           'Claim',
           'ClaimResponse',
           'ClinicalImpression',
           'CodeableConcept',
           'Coding',
           'Communication',
           'CommunicationRequest',
           'Composition',
           'ConceptMap',
           'Condition',
           'Conformance',
           'ContactPoint',
           'Contract',
           'Count',
           'Coverage',
           'DataElement',
           'DetectedIssue',
           'Device',
           'DeviceComponent',
           'DeviceMetric',
           'DeviceUseRequest',
           'DeviceUseStatement',
           'DiagnosticOrder',
           'DiagnosticReport',
           'Distance',
           'DocumentManifest',
           'DocumentReference',
           'DomainResource',
           'Duration',
           'Element',
           'ElementDefinition',
           'EligibilityRequest',
           'EligibilityResponse',
           'Encounter',
           'EnrollmentRequest',
           'EnrollmentResponse',
           'EpisodeOfCare',
           'ExplanationOfBenefit',
           'Extension',
           'FamilyMemberHistory',
           'Flag',
           'Goal',
           'Group',
           'HealthcareService',
           'Identifier',
           'ImagingObjectSelection',
           'ImagingStudy',
           'Immunization',
           'ImmunizationRecommendation',
           'ImplementationGuide',
           'List',
           'Location',
           'Media',
           'Medication',
           'MedicationAdministration',
           'MedicationDispense',
           'MedicationOrder',
           'MedicationStatement',
           'MessageHeader',
           'Meta',
           'Money',
           'NamingSystem',
           'Narrative',
           'NutritionOrder',
           'Observation',
           'OperationDefinition',
           'OperationOutcome',
           'Order',
           'OrderResponse',
           'Organization',
           'Parameters',
           'Patient',
           'PaymentNotice',
           'PaymentReconciliation',
           'Person',
           'Practitioner',
           'Procedure',
           'ProcedureRequest',
           'ProcessRequest',
           'ProcessResponse',
           'Provenance',
           'Quantity',
           'Questionnaire',
           'QuestionnaireResponse',
           'Range',
           'Ratio',
           'Reference',
           'ReferralRequest',
           'RelatedPerson',
           'Resource',
           'ResourceContainer',
           'RiskAssessment',
           'SampledData',
           'Schedule',
           'SearchParameter',
           'Signature',
           'SimpleQuantity',
           'Slot',
           'Specimen',
           'StructureDefinition',
           'Subscription',
           'Substance',
           'SupplyDelivery',
           'SupplyRequest',
           'TestScript',
           'Timing',
           'ValueSet',
           'VisionPrescription',
           'code',
           'markdown',
           'oid',
           'uri',
           'uuid',
           'RESOURCES']

import logging
import sys
import re
import shlex, subprocess
import json
from fhir.rest import init_client, Verbosity
from fhir.datatypes import *
from fhir.generated import *

LOW = Verbosity.low
MEDIUM = Verbosity.medium
HIGH = Verbosity.high
ALL_RES = "all_resources"

try:
    from urllib import urlencode as urlencode
except ImportError:
    from urllib.parse import urlencode as urlencode

def to_json(file_to_read):
    '''
    Function to_json
    
    This function read a resource in json format from file ad returns it to a json object
    
    file_to_read -> name of the file to read - use absolute path
    '''
    
    logging.info("Function to_json: file {0}".format(file_to_read))
    fi_in = open(file_to_read, "r")
    json_obj = json.load(fi_in)
    fi_in.close()        
    return json_obj

def process_message(cli_ref, message, async=False, response_url=None, format_acc="json"):
    '''
    process a FHIR message
    This operation accepts a message and send it to the server
    It returns the messages from the server
    
    cli_ref -> init_client() instance
    message -> message header to send
    async -> only supported async==False
    response_url -> not supported
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''
    
    logging.info("Entered in Function process_message.")
        
    if format_acc == 'json':
        text = {"resourceType":"Parameters",
            "parameter":[
                {
                    "name":"content",
                    "content":{}
                }
            ]
            }
        text["parameter"][0]["content"] = message
        text = json.dumps(text)
        print(text)
    else:
        text = '<Parameters xmlns="http://hl7.org/fhir"><parameter><name value="content"/><content>%s</content></parameter></Parameters>' % (message)
    
    return read_not_encoded_body(cli_ref, "$process-message", params = text, use_post = True, format_acc=format_acc)

def validate(cli_ref, resource, mode=None, profile=None, par=None, format_acc="json"):
    '''
    Validation operator
    The validate operation checks whether the attached content would be acceptable
    either generally, as a create, an update or as a delete to an existing resource.
    The action the server takes depends on the mode parameter:

    - [mode not provided]: The server checks the content of the resource against any schema,
      constraint rules, and other general terminology rules
    - create: The server checks the content, and then checks that the content would be
      acceptable as a create (e.g. that the content would not violate any uniqueness constraints)
    - update: The server checks the content, and then checks that it would accept it as an update
      against the nominated specific resource (e.g. that there are no changes to immutable fields
      the server does not allow to change, and checking version integrity if appropriate)
    - delete: The server ignores the content, and checks that the nominated resource is allowed
      to be deleted (e.g. checking referential integrity rules)      
    
    cli_ref -> init_client() instance
    resource -> "resource-tyoe", example "Patient"
    mode -> "", "create", "update", "delete", modes "update" and "delete" can only be used when the
            operation is invoked at the resource instance level (not yet supported in all test servers)
    profile -> if this is not None, then the resource is validated against this specific profile.
               If a profile is nominated and the server cannot validate against the nominated profile,
               it SHALL return an error
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''
    
    logging.info("Entered in Function validate.")
        
    if format_acc == 'json':
        text = par
        text = {"resourceType":"Parameters",
            "parameter":[
                {
                    "name":"resource",
                    "resource":{}
                }
            ]
            }
        text["parameter"][0]["resource"] = par
        if mode:
            text["parameter"].append({"name":"mode","valueCode":mode})
        if profile:
            text["parameter"].append({"name":"profile","valueUri":profile})
        text = json.dumps(text)
        print(text)
    else:
        mode_str= ""
        profile_str = ""
        
        if mode:
            mode_str = '<parameter><name value="mode"/>%s</parameter>' % mode
            
        if profile:
            profile_str = '<parameter><name value="profile"/>%s</parameter>' % profile
            
        text = '<Parameters xmlns="http://hl7.org/fhir"><parameter><name value="resource"/><resource>%s</resource></parameter>%s%s</Parameters>' % (par, mode_str, profile_str)
    
    return read_not_encoded_body(cli_ref, resource+"/$validate?async=false", params = text, use_post = True, format_acc=format_acc)

def meta_add(cli_ref = None, resource = None, par = None, format_acc="json"):
    '''
    Meta-add Operator
    '''
    
    logging.info("Entered in Function meta_add.")
    
    if (cli_ref == None) or (resource == None) or (par == None):
        print("Error: Missing parameter in Meta_add")
        return None

    if format_acc == 'xml':
        text = '<Parameters xmlns="http://hl7.org/fhir"><parameter><name value="meta"/><valueMeta>%s</valueMeta></parameter></Parameters>' % par
    else:
        text = {"resourceType":"Parameters",
                "parameter":[
                    {
                        "name":"meta",
                        "valueMeta":{}                    }
                ]
                }
        text["parameter"][0]["valueMeta"] = par
        print(text)
    
    return read_not_encoded_body(cli_ref, resource+"/$meta-add", params = text, use_post = True, format_acc=format_acc)

def meta_delete(cli_ref = None, resource = None, par = None, format_acc="json"):
    '''
    Meta-delete Operator
    '''
    
    logging.info("Entered in Function meta_delete.")
    
    if (cli_ref == None) or (resource == None) or (par == None):
        print("Error: Missing parameter in Meta_delete")
        return None

    if format_acc == 'xml':
        text = '<Parameters xmlns="http://hl7.org/fhir"><parameter><name value="meta"/><valueMeta>%s</valueMeta></parameter></Parameters>' % par
        print('Text: %s' % text)
    else:
        text = {"resourceType":"Parameters",
                "parameter":[
                    {
                        "name":"meta",
                        "valueMeta":{}                    }
                ]
                }
        text["parameter"][0]["valueMeta"] = par
        print(text)
    
    return read_not_encoded_body(cli_ref, resource+"/$meta-delete", params = text, use_post = True, format_acc=format_acc)

def document(cli_ref = None, resource = None, persist=False, format_acc="json"):
    '''
    Document operator
    A client can ask a server to generate a fully bundled document from a composition resource.
    The server takes the composition resource, locates all the referenced resources and other
    additional resources as configured or requested and either returns a full document bundle,
    or returns an error
    
    cli_ref -> init_client() instance
    resource -> Composition instance reference, example "Composition/example"
    persist -> false | true, persistance attribute
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''
    
    logging.info("Entered in Function document.")

    if persist:
        return read_not_encoded_body(cli_ref, resource+"/$document?persist=true", use_post = False, format_acc=format_acc)
    else:
        return read_not_encoded_body(cli_ref, resource+"/$document?persist=false", use_post = False, format_acc=format_acc)

def translate(cli_ref = None, target=None, code=None, system=None, version=None, valueSet=None, coding=None, codeableConcept=None, dependency=None, dependencyElement=None, dependencyConcept=None, format_acc="json"):
    '''
    Translate operator
    Translate a code from one value set to another, based on the existing value set and concept maps resources,
    and/or other additional knowledge available to the server.
    One (and only one) of the in parameters (code, coding, codeableConcept) must be provided, to identify
    the code that is to be translated.
    The operation returns a set of parameters including a 'result' for whether there is an acceptable match,
    and a list of possible matches. Note that the list of matches may include notes of codes for which mapping
    is specifically excluded, so implementers have to check the match.equivalence for each match.
    
    cli_ref -> init_client() instance
    system -> The system for the code that is to be translated
    code -> The code that is to be translated. If a code is provided, a system must be provided
    version -> The version of the system, if one was provided in the source data
    valueSet -> Identifies the value set used when the concept (system/code pair) was chosen. May be a logical id, or an absolute or relative location
    coding -> A coding to translate
    codeableConcept -> A full codeableConcept to validate. The server can translate any of the coding values (e.g. existing translations) as it chooses
    target -> Identifies the value set in which a translation is sought. May be a logical id, or an absolute or relative location
    dependency -> Another element that may help produce the correct mapping
    dependencyElement -> The element for this dependency
    dependencyConcept -> The value for this dependency
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''
    
    logging.info("Entered in Function translate.")
    
    tmpPar = {}
    if system:
        tmpPar["system"] = system
    if code:
        tmpPar["code"] = code
    if version:
        tmpPar["version"] = version
    if valueSet:
        tmpPar["valueSet"] = valueSet
    if coding:
        tmpPar["coding"] = coding
    if codeableConcept:
        tmpPar["codeableConcept"] = codeableConcept

    tmpPar["target"] = target

    if dependency:
        tmpPar["dependency"] = dependency
    if dependencyElement:
        tmpPar["dependencyElement"] = dependencyElement
    if dependencyConcept:
        tmpPar["dependencyConcept"] = dependencyConcept
   
    return read_not_encoded_body(cli_ref, "ConceptMap/$translate?" + urlencode(tmpPar), use_post = False, format_acc=format_acc)

def everything(cli_ref=None, resource=None, start_date=None, end_date=None, format_acc="json"):
    '''
    Everything operator
    This operation is used to return all the information related to the patient described
    in the resource on which this operation is invoked. The response is a bundle of type "searchset".
    At a minimum, the patient resource itself is returned, along with any other resources that
    the server has that are related to the patient, and that are available for the given user.
    The server also returns whatever resources are needed to support the records - e.g.
    linked practitioners, medications, locations, organizations etc
      
    cli_ref -> init_client() instance
    resource -> "Patient"
    start_date -> The date range relates to care dates, not record currency dates
                  - e.g. all records relating to care provided in a certain date range.
                  If no start date is provided, all records prior to the end date are in scope.
    end_date ->  The date range relates to care dates, not record currency dates
                  - e.g. all records relating to care provided in a certain date range.
                  If no end date is provided, all records subsequent to the start date are in scope.
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''
    
    logging.info("Entered in Function everything.")

    # Build a Null input Parameter
    if format_acc == 'xml':
        text = '<Parameters xmlns="http://hl7.org/fhir" />'
    else:
        text = {"resourceType" : "Parameters"}
    
    if (cli_ref == None) or (resource == None):
        print("Error: Missing parameter function")
        return None

    url_param = {} 
    if start_date:
        url_param["start"] = start_date
    if end_date:
        url_param["end"] = end_date

    input_str= ""
    if url_param != {}:
        input_str = "?" + urlencode(url_param)
        
    return read_not_encoded_body(cli_ref, resource+"/$everything"+input_str, params = text, use_post = True, format_acc=format_acc)

def meta(cli_ref = None, resource = None, format_acc="json"):
    '''
    Meta operator
    This operation retrieves a summary of the profiles, tags, and security labels
    for the given scope; e.g. for each scope:
    - system-wide: a list of all profiles, tags and security labels in use by the system
    - resource-type level: A list of all profiles, tags, and security labels for the resource type
    - individual resource level: A list of all profiles, tags, and security labels for the current
      version of the resource. Also, as a special case, this operation (and other meta operations)
      can be performed on a historical version of a resource)
      
    cli_ref -> init_client() instance
    resource -> "" if system-wide, "resource-tyoe" if resource type level,
                "Resource/id" if individual level
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''
    
    logging.info("Entered in Function meta.")

    # Build a Null Parameter
    if format_acc == 'xml':
        text = '<Parameters xmlns="http://hl7.org/fhir" />'
    else:
        text = {"resourceType" : "Parameters"}
    
    if (cli_ref == None) or (resource == None):
        print("Error: Missing parameter in function")
        return None

    if resource == "":
        return read_not_encoded_body(cli_ref, "$meta", params = text, use_post = True, format_acc=format_acc)
    else:
        return read_not_encoded_body(cli_ref, resource+"/$meta", params = text, use_post = True, format_acc=format_acc)

def validate_local(file_to_validate):
    '''
    Validation of a message by means of the java validator org.hl7.fhir.validator.jar
    '''

    text_to_execute = shlex.split("java -jar examples/org.hl7.fhir.validator.jar " \
                                  + file_to_validate + " -defn examples/validation.xml.zip")
    print("**************Validation in progress of %s *****************" % file_to_validate)
    print("Please wait...")
    str_out = subprocess.check_output(text_to_execute)
    print(str_out)
    match_obj = re.search("...success", str_out, re.M|re.I)
    if match_obj:
        print("*********************** Validated *************************")
        return True
    else:
        print("********************** NOT Validated***********************")
        return False

def create(cli_ref, resource, message, format_acc="json"):
    '''
    Resource creation
    This operation creates a Resource.
    
    cli_ref -> init_client() instance
    resource -> "resource-tyoe", example "Patient"
    message -> json representation of the resource to update or create
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''

    logging.info("Entered in Function create.")
    
    return cli_ref.create_rest(resource, message, format_acc)

def update(cli_ref, resource, message, format_acc="json"):
    '''
    Resource creation and update
    This operation creates and updates a resource.
    
    cli_ref -> init_client() instance
    resource -> "resource-type", example "Patient"
    message -> json representation of the resource to update or create
    format_acc -> response format, example "json" or "xml" it is equivalent to the parameter _format=json
               or _format=xml 
    '''
    
    logging.info("Entered in Function update.")
    
    if resource[-1:-1] != "/":
        resource += "/"
    try:
        if isinstance(message, dict):
            eval_text = eval(str(message))["id"]
        else:
            eval_text = eval(message)["id"]
    except Exception as inst:
        print(inst)
        sys.exit(1)  
    
    return cli_ref.update_rest(resource + eval_text, message, format_acc)

def read_not_encoded_body(cli_ref, resource, params = None, use_post = False, format_acc="json"):
    '''
    Use get or post to read a resource
    '''

    logging.info("Entered in Function read_not_encoded_body.")
    
    resp = None
    if isinstance(params, dict):
        # Attenzione Attenzione
        #body = urlencode(params)
        # In questo caso non posso usare urlencode perche' devo lasciare nel body del post 
        # il messaggio da parsare non toccato, cioe' in forma di dict,
        # devo solo trasformalo in stringa per serializzarlo
        body = json.dumps(params)
    else:
        body = params
        
    if use_post:
        if body:
            if format_acc == "json":
                resp = cli_ref.read_post(resource, body, format_acc, header="json+fhir")
            else:
                resp = cli_ref.read_post(resource, body, format_acc, header="xml+fhir")
        else:
            logging.debug("In Function read_not_encoded_body. Error null Body")
            print("In Function read_not_encoded_body. Error null Body")
            return None
                
    else:
        if body:
            resp = cli_ref.read_get(resource+"?"+body, format_acc)
        else:
            resp = cli_ref.read_get(resource, format_acc)
    return resp

def read(cli_ref, resource, params = None, use_post = False, format_acc="json"):
    '''
    Use get or post to read a resource
    '''

    logging.info("Entered in Function read.")
    
    resp = None
    if isinstance(params, dict):
        body = urlencode(params)
    else:
        body = params
        
    if use_post:
        if body:
            resp = cli_ref.read_post(resource, body, format_acc)
        else:
            resp = cli_ref.read_post(resource, "", format_acc)
    else:
        if body:
            resp = cli_ref.read_get(resource+"?"+body, format_acc)
        else:
            resp = cli_ref.read_get(resource, format_acc)
    return resp

def vread(cli_ref, resource, res_id, res_vid, mime_type=None, format_acc="json"):
    '''
    Use get to read a resource with a particular version id - vid
    '''

    logging.info("Entered in Function vread.")
    
    if mime_type:
        resp = cli_ref.read_get(resource+"/"+res_id+"/"+"_history/"+res_vid+"?_format="+mime_type, format_acc)
    else:
        resp = cli_ref.read_get(resource+"/"+res_id+"/"+"_history/"+res_vid, format_acc)
        
    return resp

def history(cli_ref, resource=None, res_id=None, params=None, mime_type=None, format_acc="json"):
    '''
    Use get or to read history
    '''

    logging.info("Entered in Function history.")
    
    resp = None
    if isinstance(params, dict):
        body = urlencode(params)
    else:
        body = params
        
    tmp_str = ""
    if params:
        tmp_str += "?" + body
        if len(tmp_str) > 0:
            if mime_type:
                tmp_str += "&_format=" + mime_type
        else:
            if mime_type:
                tmp_str += "_format=" + mime_type
    else:
        if mime_type:
            tmp_str += "?_format=" + mime_type

    if not resource:
        resp = cli_ref.read_get("_history"+tmp_str, format_acc)
    else:
        if not res_id:
            resp = cli_ref.read_get(resource + "/_history"+tmp_str, format_acc)
        else:
            resp = cli_ref.read_get(resource + "/" + res_id + "/_history"+tmp_str, format_acc)
            
    return resp

def conformance(cli_ref, mime_type=None, format_acc="json"):
    '''
    Use get or to read history
    '''

    logging.info("Entered in Function conformance.")
    
    tmp_str = ""
    if mime_type:
        tmp_str += "?_format=" + mime_type

    resp = cli_ref.read_get("metadata" + tmp_str, format_acc)
            
    return resp

def delete(cli_ref, resource, params = None, format_acc="json"):
    '''
    Delete a resource
    '''

    logging.info("Entered in Function delete.")
    
    return cli_ref.delete_rest(resource + "/" + params, format_acc)
            
def search(cli_ref, resource, params, use_post = False, format_acc="json"):
    '''
    Use get or post to search informations
    '''

    logging.info("Entered in Function search.")
    
    resp = None
    if isinstance(params, Where):
        body = str(params)
    else:
        body = urlencode(params)
    
    if resource != ALL_RES:
        if use_post:
            resp = cli_ref.read_post(resource+"/_search", body, format_acc)
        else:
            resp = cli_ref.read_get(resource+"?"+body, format_acc)
        return resp
    else:
        # resource == None, global search
        resp = cli_ref.read_get("_search?"+body, format_acc)
        return resp

class Where(object):
    def __init__(self, search_condition):
        self.__search_cond = [search_condition]
        
    def And(self, search_condition):
        self.__search_cond += [search_condition]
        return self
    
    def __repr__(self):
        '''
        FHIR Where condition Representation
        '''
        out_str = ""
        for element in self.__search_cond:
            if out_str == "":
                out_str += urlencode(element)
            else:
                out_str += '&' + urlencode(element)
                
        return out_str

if __name__ == '__main__':
    pass
    