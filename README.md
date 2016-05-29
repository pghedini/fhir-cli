# fhir-cli
HL7 FHIR CLI (Command Line Interface) an easy to use python interface to HL7 FHIR® – Fast Healthcare Interoperability Resources
---------------------------------------------------------------------------------
## README
## FHIR CLI 1.0.0

Author: **Pierfrancesco Ghedini**
pierfrancesco.ghedini@gmail.com

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

### Use of operation "document"

```
resp = document(cli, "Composition/example")
bu = Bundle(resp.obj())
for ent in bu.entry:
    print(html2text(ent.resource["text"]["div"]))
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
