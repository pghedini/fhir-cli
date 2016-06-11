# fhir-cli
HL7 FHIR CLI (Command Line Interface) an easy to use python interface to HL7 FHIR® – Fast Healthcare Interoperability Resources
---------------------------------------------------------------------------------
## README
## FHIR CLI 1.0.0

Author: **Pierfrancesco Ghedini**
pierfrancesco.ghedini@gmail.com
Site: **http://www.informaticasanitaria.it**

Execute the commands listed in this README in a iPython interpreter - or an another interpreter, if you prefer - to experiment.

ipython useful features:
- to paginate the output use "%page command_to_paginate"
- to save a command and its output to a file use "%history -o line_number -f file_name_to_save_to" 
 
---------------------------------------------------------------------------------

## What is FHIR CLI?
**FHIR CLI - FHIR Command Line Interface -** is a command line interface to **HL7 FHIR**.
With FHIR CLI you will be able to interact with a FHIR server to read, create, update, delete resources in a quite simple way.
Several FHIR operations are supported:
- everything
- document
- meta
- etc...

**FHIR CLI** supports DSTU2 and will support future versions of the standard.  

## Requirements
**FHIR CLI** is tested to be used in python 2.7 and python 3.X.

It requires the python modules:
- datetime (use "pip install datetime" to install)
- dateutil.parser (use "pip install python-dateutil" to install)
- Enum (use "pip install Enum" to install)
- json (use "pip install simplejson" to install)
- os (normally already installed)
- re (normally already installed)
- shlex (normally already installed)
- subprocess (normally already installed)
- sys (normally already installed)

Optional modules:
- logging (use "pip install logging" to install)
 
## To initialize the client

import the library **client** and load the json library (not mandatory)

```
from client import *
import json # not mandatory
````

to improve readability of narratives use html2text (not mandatory)
```
from html2text import html2text as html2text
```
Initialize the client
```
cli = init_client()
```

The default call of function init_client() sets output to low verbosity,
in order to obtain more verbosity use
```
cli = init_client(verb=HIGH)
```

to select a different FHIR server use the command
```
cli = init_client(url="http://spark.furore.com/fhir/")
```

to enable logging use
```
cli = init_client(log_file="/tmp/FHIR_prova.txt")
#to enable also the viewing of the logging in console use
cli = init_client(con_log=True, log_file="/tmp/FHIR_prova.txt")
```
example of non default initialization
```
cli = init_client(url="http://spark.furore.com/fhir/", con_log=True, log_file="/tmp/FHIR_prova.txt", verb=HIGH)
```
### List all the available resource models
```
%page RESOURCES
```

### Low level approach

To get a Patient with a given id - low level approach -
use, directly, the rest method read_rest()
```
resp = cli.read_get("Patient/4", "json")
```

if you try to retrieve a patient that doesn't exist you obtain an error.
It's possible to decode the returned error by means of OperationOutcome object
```
resp = cli.read_get("Patient/notexistent")
oo = OperationOutcome(resp.obj().json)
oo
```

### Retrieve a patient with the ordinary client read function (preferred approach)
```
resp = read(cli, "Patient/4")
# resp contains a single resource of "resourceType" -> "Patient"
resp.is_bundle() # returns False
# to get a Bundle of patients use
resp = read(cli, "Patient")
resp.is_bundle() # returns True
```

### Use of Bundles (resources containers)
```
resp = read(cli, "MedicationDispense/meddisp001")
md = MedicationDispense(resp.obj())
md.text.div
print(html2text(md.text.div))
```

to get the first entry of a returned Bundle
```
resp.entry(0)
```

to get the json object with resp.obj()
we can use
```
resp.obj()["entry"][0]
```
the entry is a composed by "fullUrl" and "resource"
"fullUrl" is the address of the retrieved "entry" and "resource" is the resource content
to get the patient resource details use
```
resp.entry(0)["resource"]
```
or
```
resp.obj()["entry"][0]["resource"]
```
to decode a Patient resource you can use the Patient object
```
pa = Patient(resp.obj()["entry"][0]["resource"])
```
Now is possible to explore the patient instance
```
help(pa)
pa.id
pa.name
pa.name[0].family[0]
```
FHIR documentation says
>"Any resource that is a domain resource
>(almost all types of resource) may include a human-readable narrative
>that contains a summary of the resource, and may be used to represent
>the content of the resource to a human."

```
print(html2text(pa.text.div))
```

## Search Resources
search a Patient with given id (resource identifier)

```
resp = search(cli, "Patient", Patient.search.id_.EQ('4'))
resp.is_bundle() # returns True
resp.total()
resp.paths()
resp.entry(0)["resource"]["id"]
```

Search patients with name "Duck"
```
resp = search(cli, "Patient", Patient.search.name.Contains("Duck"), False)
resp.is_bundle() # returns True
bu = Bundle(resp.obj())
bu.total
for ent in bu.entry:
	print ent.resource["id"]
	print ent.resource["name"]
```
To show the index in the list use the command
```
for index in range(len(bu.entry)):
	print index
	print bu.entry[index].resource['id']
	print bu.entry[index].resource['name']
```

Search patients with **"or"** condition
```
resp = search(cli, "Patient", Patient.search.id_.EQ('4,5'), False)
resp.is_bundle() # returns True
bu = Bundle(resp.obj())
bu.total
```

Search patient with a complex selection, _text searches on narrative of the resource
 
```
where = Where(Patient.search.text_.EQ("Healthcare"))
resp = search(cli, "Patient", where)
resp.is_bundle() # returns True
bu = Bundle(resp.obj())
bu.total
print(html2text(bu.entry[0].resource["text"]["div"]))
```

### Search a inexistent resource

```
resp = search(cli, "Patient", Patient.search.family.EQ("non_existent_name"))
bu = Bundle(resp.obj())
bu.total  # it returns 0
```

### complex search statement examples

```
resp = read(cli, "MedicationDispense/meddisp001")
md = MedicationDispense(resp.obj())
md.text.div
print(html2text(md.text.div))
in_par = json.loads('{"system":"http://example.org/codes/tags", "code":"record-lost", "display": "Patient File Lost"}')
print(in_par)
resp = meta_add(cli, "Patient/pat1", par=in_par, format_acc="json")
where = Where(Patient.search.tag_.EQ("http://example.org/codes/tags|record-lost")).And(Patient.search.id_.EQ('pat1'))
resp = search(cli, "Patient", where)
resp.is_bundle() # returns True
bu = Bundle(resp.obj())
bu.total

where = Where(Patient.search.lastUpdated_.GT("2016-03-15")).And(ALL.sort_.asc("_id"))
resp = search(cli, "Patient", where)
for res in resp.entry_list():
    print(res["resource"]["id"])
```
### search an Observation whose subject has a specific name

```
where = Patient.search.name.EQ("Jones", full=True)
resp = search(cli, "Observation", where)
resp.obj()["entry"][0]["resource"]["subject"]["reference"]
resp = read(cli, resp.obj()["entry"][0]["resource"]["subject"]["reference"])
#
where = Where(ALL.include_.EQ("Observation:Patient")).And(Patient.search.name.EQ("Jones", full=True))
resp = search(cli, "Observation", where)
#
```

### search for a missing parameter

```
where = Patient.search.gender.Missing("true")
resp = search(cli, "Patient", where)
pa = Patient(resp.entry(0)["resource"])
pa.gender # return nothing, id est None
```
### search a Bundle with a lot of entries - pagination

```
resp = search(cli, "Patient", {})
bu = Bundle(resp.obj())
bu.total
len(bu.entry)
bu.link
bu.entry[0].resource['id']
bu.entry[1].resource["id"]
next = bu.link[2].url
resp1 = read(cli, next)
bu1 = Bundle(resp1.obj())
bu1.link
bu1.entry[0].resource["id"]
bu1.entry[1].resource["id"]
```
### Global search example
```
where = Where(ALL.text_.EQ("Duck")).And(ALL.sort_.asc("_id"))
resp = search(cli, ALL_RES, where)        
for ent in resp.entry:
    print((ent["resource"]["resourceType"], ent["resource"]["id"]))
```

### Search for MedicationOrders for a specific Patient
```
resp = search(cli, "MedicationOrder", MedicationOrder.search.patient.EQ("http://fhir.healthintersections.com.au/open/Patient/d1"))
#
# Search for linked resources
#
resp = read(cli, "Observation")
ob = Observation(resp.entry(0)["resource"])
resp = read(cli, "Patient/f001")
pa = Patient(resp.obj())
pa.managingOrganization
org = Organization(cli.read_rest("Organization/f001").obj())
help(Organization)
org.text
resp = read(cli, "Practitioner")
pract = Practitioner(resp.entry(0)["resource"])
pract.id
pa.careProvider = [{"display": "CareProv", "reference": "http://spark.furore.com/fhir/Practitioner/14"}]
resp = update(cli, "Patient", pa.json, "json")
resp.obj()["careProvider"]
```

### Create, Update, Delete examples

create a new patient from a retrieved one

```
# Use the first instance retrieved from the previous search
resp = read(cli, "Patient")
bu = Bundle(resp.obj())
pa = Patient(bu.entry[0].resource)
# change the patient family name
pa.id = None
pa.name[0].family[0] = "Test1"
# create a new patient
resp = create(cli, "Patient", pa.json, "json")
obj_id = resp.obj()["id"]
pa = Patient(resp.obj())
# update the family name
pa.name[0].family[0] = "Test2"
# update the resource instance
resp = update(cli, "Patient", pa.json, "json")
pa = Patient(resp.obj())
# verify the result
print(pa.name[0].family[0])
# delete the patient
resp = delete(cli, "Patient", obj_id, "json")
#
resp = history(cli, "Patient", obj_id)
```

### Reading history of a resource
```
resp = history(cli, "Patient", "f001")
```

### Reading narratives
```
resp = read(cli, "Observation")
ob = Observation(resp.entity(0)["resource"])
print(html2text(ob.text["div"]))
```

## Use of operators

### Use Everything example

```
resp = everything(cli, "Patient/"+pa.id)
resp.entry(0)["resource"]
```

## Search Profiles and instance adhering to profile

```
resp = meta(cli, "Patient")
resp.obj()["parameter"][0]["valueMeta"]["profile"]
```
Let's choose profile http://hl7.org/fhir/StructureDefinition/gao-patient,
so find the patient who is adhering to chosen profile.
```
resp = search(cli, "Patient", Patient.search.profile_.EQ("http://hl7.org/fhir/StructureDefinition/gao-patient"))
# the profile impose  cardinality min and max (1,1) in gender and birthDate
resp.obj()
```

## Rendering resource Narrative in text and in a browser
```
resp = read(cli, "MedicationDispense/meddisp001")
md = MedicationDispense(resp.obj())
md.text.div
print(html2text(md.text.div))
```

you can also use the browser to view div

```
#save the output of md.text.div in a file
%hist -o line_number_of_the_output_of_command_md_text_div -f file_name.html
# view it in the browser
!firefox file_name.html &
```

## Validating a resource by means of a FHIR server

Let's validate a resource in xml format...

Store the resource in a variable called res

```
res = '''<Patient xmlns="http://hl7.org/fhir">
  <id value="pat1"/>
  <text>
    <status value="generated"/>
    <div xmlns="http://www.w3.org/1999/xhtml">
      
      <p>Patient Donald DUCK @ Acme Healthcare, Inc. MR = 654321</p>
    
    </div>
  </text>
  <identifier>
    <use value="usual"/>
    <type>
      <coding>
        <system value="http://hl7.org/fhir/v2/0203"/>
        <code value="MR"/>
      </coding>
    </type>
    <system value="urn:oid:0.1.2.3.4.5.6.7"/>
    <value value="654321"/>
  </identifier>
  <active value="true"/>
  <name>
    <use value="official"/>
    <family value="Donald"/>
    <given value="Duck"/>
  </name>
  <gender value="male"/>
</Patient>'''

```

now execute the FHIR operation

```
resp = validate(cli, resource="Patient", par=res, format_acc="xml")
```

See the response code in order to check the operation result

```
resp.resp_code()
```
or simply type the variable name resp to display the output of the command

```
resp
```

To validate a resource in json format...

Build a resource to test

```
pa = Patient({"resourceType":"Patient", "id": "pat1", "name":[{"family":["Donald"],"given":["TestName"],"use":"official"}]})
# check the content of pa simply entering pa variable
pa
```

and validate it.
Pay attention: to obtain the json representation from Patient resource stored in "pa" variable, use pa.json

```
resp = validate(cli, resource="Patient", par=pa.json, format_acc="json")

```

See the response code in order to check the operation result

```
resp.resp_code()
```

## Meta Operator

Reading meta tags with $meta operator, Adding meta tags with $meta-add and Deleting meta tags with $meta-delete

Read meta tags of an existing Patient

```
resp = meta(cli, "Patient/5149")
```

Add meta tags

```
in_par = [{"system":"http://example.org/codes/tags", "code":"record-lost", "display": "Patient File Lost"}]
resp = meta_add(cli, "Patient/5149", par=in_par)
```

Delete meta tags

```
in_par = [{"system":"http://example.org/codes/tags", "code":"record-lost", "display": "Patient File Lost"}]
resp = meta_delete(cli, "Patient/5149", par=in_par)
```

## Document Operator

As FHIR Documentation says "FHIR resources can be used to build documents that represent a composition:
a set of coherent information that is a statement of healthcare information, particularly including clinical observations and services.
A document is an immutable set of resources with a fixed presentation that is authored and/or attested by humans, organizations and devices.
Documents built in this fashion may be exchanged between systems and also persisted in document storage and management systems, including systems such as IHE XDS.
Applications claiming conformance to this framework claim to be conformant to "FHIR documents"

The FHIR Document Operator produces a document from a given composition.

```
resp = document(cli, "Composition/example")
# resp is a bundle to decode
bu = Bundle(resp.obj())
# Now loop over bundle entries
for ent in bu.entry:
    print(html2text(ent.resource["text"]["div"]))
```

if you want to make the document persistent, set "persist" attribute to True

```
resp = document(cli, "Composition/example", persist=True)
```

## Everything Operator

This operation is used to return all the information related to the resource on which this operation is invoked, Encounter and Patient.
The response is a bundle of type "searchset".
At a minimum, the patient/encounter resource itself is returned, along with any other resources that
the server has that are related to the patient/encounter, and that are available for the given user.
The server also returns whatever resources are needed to support the records - e.g.
linked practitioners, medications, locations, organizations etc

Two input parameters are:
- start_date -> The date range relates to care dates, not record currency dates - e.g. all records relating to care provided in a certain date range. If no start date is provided, all records prior to the end date are in scope.
- end_date ->  The date range relates to care dates, not record currency dates - e.g. all records relating to care provided in a certain date range. If no end date is provided, all records subsequent to the start date are in scope.

```
# Basic invocation on a Patient instance
# 
resp = everything(cli, "Patient/example")
```

The operator can also be executed on all Patients

```
# Invocation on all Patient resources
# 
resp = everything(cli, "Patient")
```

In the same way the command can be used on Encounters

```
# Basic invocation on an Encounter instance 
resp = everything(cli, "Encounter/example")
# Invocation on all Encounter resources
resp = everything(cli, "Encounter")
```
