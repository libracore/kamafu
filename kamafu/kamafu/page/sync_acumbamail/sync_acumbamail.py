# -*- coding: utf-8 -*-
# Copyright (c) 2017-2024, libracore and contributors
# License: AGPL v3. See LICENCE

# import definitions
from __future__ import unicode_literals
import frappe
from frappe import throw, _
import json
import base64
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import hashlib
from frappe.utils.background_jobs import enqueue
from frappe.utils.password import get_decrypted_password
import os

acumbamail_host = "https://acumbamail.com/api/1"

# execute API function
def execute(endpoint, verify_ssl=True, method="GET"):  
    try:
        auth_token = get_decrypted_password("Kamafu Settings", "Kamafu Settings", "acumbamail_auth_token", False)
        host = os.path.join(acumbamail_host, endpoint)
        if "?" in host:
            host += "&auth_token={0}".format(auth_token)
        else:
            host += "?auth_token={0}".format(auth_token)
        response = requests.request(
            method=method,
            url=host,
            verify=verify_ssl)
        
        status=response.status_code
        text=response.text
        if status not in [200, 404]:
            frappe.log_error("Unexpected Acumbamail response: http {method} {host} response {status} with message {text}".format(
                status=status,text=text, method=method, host=host))
        if status == 404:
            return None
        
        return text
    except Exception as e:
        #frappe.log_error("Execution of http request failed. Please check host and API token.")
        frappe.throw("Execution of http request failed. Please check host and API token. ({0})".format(e))
        
@frappe.whitelist()
def get_lists():
    raw = execute(endpoint="getLists/")
    results = {}
    try:
        results = json.loads(raw)
    except Exception as err:
        frappe.throw("Unexepcted response: {0}".format(raw))
    
    """
    Lists provided as:
        {
            'list_id': {'name': 'list_name', 'description': 'description}
        }
    """
    return results

@frappe.whitelist()
def get_members(list_id, count=10000):
 
    raw = execute(endpoint="getSubscribers/?list_id={list_id}&all_fields=1".format(list_id=list_id))
    
    """
    Members provided as:
        {
            'email_id': {'status': 'active', 'create_date': '...', 'email': '...', 'id': '1234'}
        }
    """
    results = json.loads(raw)
    return results

@frappe.whitelist()
def enqueue_sync_contacts(list_id):
    add_log(title= _("Starting sync"), 
       description= ( _("Starting to sync contacts to {0}")).format(list_id),
       status="Running")
       
    kwargs={
          'list_id': list_id
        }
    enqueue("kamafu.kamafu.page.sync_acumbamail.sync_acumbamail.sync_contacts",
        queue='long',
        timeout=15000,
        **kwargs)
    frappe.msgprint( _("Queued for syncing. It may take a few minutes to an hour."))
    return
    
def sync_contacts(list_id):
    # prepare local contacts: all contacts with an email
    erp_contacts = frappe.get_list('Contact', 
        filters={'email_id': ['LIKE', u'%@%.%']}, 
        fields=["name", "email_id", "first_name", "last_name", "unsubscribed"])
    
    if not erp_contacts:
        frappe.msgprint( _("No contacts found") )
        return
    
    # get list members
    members = get_members(list_id)
    
    # sync
    contact_written = []
    for cnt in erp_contacts:

        # load subscription status from acumbamail
        # default is unsubscribed
        if cnt['email_id'] in members:
            # contact already in acumbamail
            contact_status = members[cnt['email_id']]['status']
            endpoint = "addSubscriber/?update_subscriber=1&list_id={list_id}".format(list_id=list_id)
            
        else:
            # new contact
            contact_status = "inactive" if cnt['unsubscribed'] else "active"
            endpoint = "addSubscriber/?update_subscriber=0&list_id={list_id}".format(list_id=list_id)

        endpoint += "&merge_fields[email]={email}&merge_fields[status]={status}&merge_fields[fname]={fname}&merge_fields[lname]={fname}".format(
            email=cnt['email_id'], status=contact_status, fname=cnt['first_name'] or "", lname=cnt['last_name'] or "")
            
        raw = execute(endpoint=endpoint)
        contact_written.append(cnt['email_id'])
    
    add_log(title= _("Sync complete"), 
       description= ( _("Sync of contacts to {0} completed.\n{1}")).format(list_id, ",".join(contact_written)),
       status="Completed")
    return contact_written
            
@frappe.whitelist()
def enqueue_get_campaigns(list_id):
    add_log(title= _("Starting sync"), 
       description=( _("Starting to sync campaigns from {0}")).format(list_id),
       status="Running")
       
    kwargs={
          'list_id': list_id
        }
    enqueue("kamafu.kamafu.page.sync_acumbamail.sync_acumbamail.get_campaigns",
        queue='long',
        timeout=15000,
        **kwargs)
    frappe.msgprint( _("Queued for syncing. It may take a few minutes to an hour."))
    return
    
def get_campaigns():
    raw = execute(endpoint="getCampaigns/?complete_json=1", payload={})
    results = json.loads(raw)
    for campaign in results['campaigns']:
        try:
            erp_campaign = frappe.get_doc("Campaign", campaign['settings']['title'])
            # update if applicable
            
        except:
            # erp does not know this campaignyet, create
            new_campaign = frappe.get_doc({'doctype': 'Campaign'})
            new_campaign.campaign_name = campaign['settings']['title']
            new_campaign.insert()
         
    add_log(title= _("Sync complete"), 
       description= ( _("Sync of campaigns from {0} completed.")).format(list_id),
       status="Completed")
    return { 'campaigns': results['campaigns'] }

def delete_member(list_id, email):
    endpoint = "deleteSubscriber/?list_id={list_id}&email={email}".format(list_id=list_id, email=email)
    raw = execute(endpoint=endpoint)
    return

def add_log(title, description, status="OK"):
    new_log = frappe.get_doc({
        'doctype': 'Acumbamail Log',
        'title': title,
        'description': description,
        'status': status,
        'date': datetime.now()
    })
    new_log.insert()
    frappe.db.commit()
    return
