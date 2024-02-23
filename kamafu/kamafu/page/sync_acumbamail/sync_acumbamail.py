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
def execute(endpoint, payload, verify_ssl=True, method="GET"):  
    try:
        payload['auth_token'] = get_decrypted_password("Kamafu Settings", "Kamafu Settings", "acumbamail_auth_token", False)
        host = os.path.join(acumbamail_host, endpoint)
        response = requests.request(
            method=method,
            url=host,
            json=payload,
            # auth=HTTPBasicAuth("libracore", api_token),
            verify=verify_ssl)
        
        status=response.status_code
        text=response.text
        if status not in [200, 404]:
            frappe.log_error("Unexpected Acumbamail response: http {method} {host} response {status} with message {text} on payload {payload}".format(
                status=status,text=text, payload=payload, method=method, host=host))
        if status == 404:
            return None
        
        return text
    except Exception as e:
        #frappe.log_error("Execution of http request failed. Please check host and API token.")
        frappe.throw("Execution of http request failed. Please check host and API token. ({0})".format(e))
        
@frappe.whitelist()
def get_lists():
    raw = execute(endpoint="getLists/", payload={})
    results = json.loads(raw)
        
    return { 'lists': results['lists'] }

@frappe.whitelist()
def get_members(list_id, count=10000):
 
    raw = execute(endpoint="getSubscribers/?list_id={list_id}&all_fields=1", payload={})
    results = json.loads(raw)
    return { 'members': results['members'] }

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
    member_status_map = create_member_status_map(members)
    
    # sync
    contact_written = []
    for cnt in erp_contacts:

        # load subscription status from acumbamail
        # default is unsubscribed
        if cnt['email_id'] in member_status_map:
            # contact already in acumbamail
            contact_status = member_status_map[cnt['email_id']]
            endpoint = "addSubscriber/?update_subscriber=1"
            
        else:
            # new contact
            contact_status = "unsubscribed" if cnt['unsubscribed'] else "subscribed"
            endpoint = "addSubscriber/?update_subscriber=0"

        contact_object = {
            "email_address": contact.email_id,
            "status": contact_status,
            "merge_fields": {
                "FNAME": contact.first_name or "", 
                "LNAME": contact.last_name or ""
            }
        }
            

        raw = execute(endpoint=endpoint, payload=contact_object)
        contact_written.append(contact.email_id)
    
    #add_log(title= _("Sync complete"), 
    #   description= ( _("Sync of contacts to {0} completed.\n{1}")).format(list_id, ",".join(contact_written)),
    #   status="Completed")
    return { 'members': results['members'] }

def create_member_status_map(members):
    member_status_map = {}
    for m in members:
        member_status_map[m.subscriber] = m.status
    return member_status_map
    
            
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
         
    #add_log(title= _("Sync complete"), 
    #   description= ( _("Sync of campaigns from {0} completed.")).format(list_id),
    #   status="Completed")
    return { 'campaigns': results['campaigns'] }


