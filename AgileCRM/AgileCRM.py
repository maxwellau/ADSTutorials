#Ensure to import dependencies
# import pandas as pd
# import requests
# import json
class CRM:
    def __init__(self, apikey, email, domain):
        self.apikey = apikey
        self.email = email
        self.domain = domain
        
    def agileCRM(self, nextURL,method,data,contenttype):
        BASE_URL = "https://" + self.domain + ".agilecrm.com/dev/api/"
        url = BASE_URL + nextURL
        headers = {
            'Accept': 'application/json',
            'content-type': contenttype,
            }
        
        if ( method  == "GET" ) :
            response = requests.get(
            url,
            headers=headers,
            auth=(self.email, self.apikey)
            )
            return response

        if ( method  == "POST" ) :
            response = requests.post(
            url,
            data=json.dumps(data),
            headers=headers,
            auth=(self.email, self.apikey)
            )
            return response

        if ( method  == "PUT" ) :
            response = requests.put(
            url,
            data=json.dumps(data),
            headers=headers,
            auth=(self.email, self.apikey)
            )
            return response

        if ( method  == "DELETE" ) :
            response = requests.delete(
            url,
            headers=headers,
            auth=(self.email, self.apikey)
            )
            return response

        if ( method  == "POSTFORM" ) :

            response = requests.post(
            url,
            data=data,
            headers=headers,
            auth=(self.email, self.apikey)
            )
            return response
        return "Wrong method provided"
    
    def getIdFromEmail(self, email):
        assert email == str(email), 'email has to be a String'
        try:
            resp = self.agileCRM(f"contacts/search/email/{email}","GET",None,"application/json")
            return str(resp.json()['id'])
        except ValueError:
            print("check if your email is correct")
    
    def getContactFromId(self, userid):
        assert userid == str(userid), 'userid has to be a String'
        return self.agileCRM(f"contacts/{userid}","GET",None,"application/json")
    
    def searchCompanyIdFromName(self, company):
        assert company == str(company), 'company has to be a String'
        return self.agileCRM(f"search?q={company}&page_size=10&type='COMPANY'","GET",None,"application/json")
    
    def makeDeal(self, dealName, expectedValue, probability, milestone, contactID):
        assert dealName == str(dealName), 'dealName has to be a String'
        assert probability == str(probability), 'probability has to be a String'
        assert milestone == str(milestone), 'milestone has to be a String'
        assert type(contactID) == list, 'contactID has to be a list of Strings'
        deal_data = {
        "name": dealName,
        "expected_value": expectedValue,
        "probability": probability,
        "close_date": 0,
        "milestone": milestone,
        "contact_ids": contactID,
         }

        resp = self.agileCRM("opportunity","POST",deal_data,"application/json")
        return resp
    
    def makeNote(self, subject, description, contactID):
        assert subject == str(subject), 'subject has to be a String'
        assert description == str(description), 'description has to be a String'
        assert type(contactID) == list, 'contactID has to be a list of Strings'
        note_data = {
        "subject": subject,
        "description": description,
        "contact_ids": contactID
        }
        return self.agileCRM("notes","POST",note_data,"application/json")
    
    def createContact(self, firstName, lastName, company, title, email, address, customField, customContent):
        assert firstName == str(firstName), 'firstName has to be a String'
        assert lastName == str(lastName), 'probability has to be a String'
        assert company == str(company), 'company has to be a String'
        assert title == str(title), 'title has to be a String'
        assert email == str(email), 'email has to be a String'
        assert address == str(address), 'address has to be a String'
        assert customField == str(customField), 'customField has to be a String'
        assert customContent == str(customContent), 'customContent has to be a String'
        contact_data = {
        "star_value": "0",
        "lead_score": "",
        "tags": [],
        "properties": [
            {
                "type": "SYSTEM",
                "name": "first_name",
                "value": firstName + " "
            },
            {
                "type": "SYSTEM",
                "name": "last_name",
                "value": lastName
            },
            {
                "type": "SYSTEM",
                "name": "company",
                "value": company
            },
            {
                "type": "SYSTEM",
                "name": "title",
                "value": title
            },
            {
                "type": "SYSTEM",
                "name": "email",
                "subtype": "work",
                "value": email
            },
            {
                "type": "SYSTEM",
                "name": "address",
                "value": address
            },
            {
                "type": "CUSTOM",
                "name": customField,
                "value": customContent
            }
            ]
            }
        resp = self.agileCRM("contacts","POST",contact_data,"application/json")
        return resp
