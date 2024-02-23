# -*- coding: utf-8 -*-
# Copyright (c) 2018-2024, libracore and contributors
# For license information, please see license.txt
#
# call the API from
#   /api/method/kamafu.kamafu.caldav.download_calendar?secret=[secret]&user=[user]

from icalendar import Calendar, Event, Todo
from datetime import datetime
import frappe

def get_calendar(secret, user):
    caldav_secret = frappe.db.get_value("Kamafu Settings", "Kamafu Settings", "caldav_secret")
    if not caldav_secret:
        return
    if secret != caldav_secret:
        return
    if not frappe.db.exists("User", user):
        return
        
    # initialise calendar
    cal = Calendar()

    # set properties
    cal.add('prodid', '-//libracore business software//libracore//')
    cal.add('version', '2.0')

    # get events
    events = frappe.db.sql("""
        SELECT * 
        FROM `tabDeal` 
        WHERE 
            `event_date` >= CURDATE()
            AND (`stage` = "Gewonnen" OR `stage` LIKE "Offerte%");
    """, as_dict=True)
    # add events
    for erp_visit in visits:
        event = Event()
        event.add('summary', erp_event['name'])
        event.add('dtstart', erp_event['visit_date'])
        #if erp_event['ends_on']:
        #    event.add('dtend', erp_event['ends_on'])
        event.add('dtstamp', erp_event['modified'])
        event.add('description', "{0}\n\r{1}\n\r{2}".format(
            erp_event['object_name'], 
            erp_event['object_street'], 
            erp_event['object_location']))
        # add to calendar
        cal.add_component(event)
    
    # get todos
    
    return cal

@frappe.whitelist(allow_guest=True)
def download_calendar(secret, user):
    frappe.local.response.filename = "caldav.ics"
    calendar = get_calendar(secret, user)
    if calendar:
        frappe.local.response.filecontent = calendar.to_ical()
    else:
        frappe.local.response.filecontent = "No access"
    frappe.local.response.type = "download"
    return
