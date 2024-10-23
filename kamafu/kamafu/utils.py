# Copyright (c) 2021-2024, libracore and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from datetime import datetime, timedelta
import json
from frappe.utils import cint

"""
Process to create an akonto invoice from a sales order (using an akonto item)
"""
@frappe.whitelist()
def create_akonto(sales_order):
    so_doc = frappe.get_doc("Sales Order", sales_order)
    
    akonto = get_mapped_doc("Sales Order", sales_order, 
        {
            "Sales Order": {
                "doctype": "Sales Invoice",
                "field_map": {
                    "name": "sales_order"
                }
            },
            "Sales Taxes and Charges": {
                "doctype": "Sales Taxes and Charges",
                "add_if_empty": True
            }
        }
    )
    akonto.append('items', {
        'item_code': frappe.get_cached_value("Kamafu Settings", "Kamafu Settings", "akonto_item"),
        'qty': 1,
        'rate': round((so_doc.net_total * 0.3), 2),
        'sales_order': sales_order
    })
    # akonto.title = "Anzahlungsrechnung"           # 2023-03-20 do not override title
    akonto.set_missing_values()
    return akonto

"""
This function find applicable akonto invoices
"""
@frappe.whitelist()
def get_available_akonto(sales_order=None):
    if not sales_order:
        return []
    from kamafu.kamafu.report.offene_kundenguthaben.offene_kundenguthaben import get_data
    akonto = get_data({'sales_order': sales_order})
    return akonto

"""
This function will transfer the previous akonto amount to the revenue
"""
@frappe.whitelist()
def book_akonto(sales_invoice, net_amount):
    sinv = frappe.get_doc("Sales Invoice", sales_invoice)
    akonto_item = frappe.get_doc("Item", frappe.get_cached_value("Kamafu Settings", "Kamafu Settings", "akonto_item"))
    akonto_account = None
    for d in akonto_item.item_defaults:
        if d.company == sinv.company:
            akonto_account = d.income_account
    if not akonto_account:
        frappe.throw("Please define an income account for the Akonto Item")

    revenue_account = frappe.get_cached_value("Company", sinv.company, "default_income_account")
    if not revenue_account:
        frappe.throw("Please define a default revenue account for {0}".format(sinv.company))
        
    jv = frappe.get_doc({
        'doctype': 'Journal Entry',
        'posting_date': sinv.posting_date,
        'company': sinv.company,
        'accounts': [
            {
                'account': akonto_account,
                'debit_in_account_currency': net_amount
            },{
                'account': revenue_account,
                'credit_in_account_currency': net_amount
            }
        ],
        'user_remark': "Akonto from {0}".format(sales_invoice)
    })
    jv.insert(ignore_permissions=True)
    jv.submit()
    frappe.db.commit()
    return jv.name

@frappe.whitelist()
def get_item_tax_rate(item_code, sales=True):
    item = frappe.get_doc("Item", item_code)
    if item.item_defaults and len(item.item_defaults) > 0:
        if sales:
            account = item.item_defaults[0].income_account
        else:
            account = item.item_defaults[0].expense_account
        return frappe.get_value("Account", account, "steuersatz")
    else:
        return 0
        

@frappe.whitelist()
def get_next_item_code():
    pattern = {
        'prefix': "A",
        'length': 5
    }
    
    last_item_code = frappe.db.sql("""
        SELECT `name`
        FROM `tabItem`
        WHERE 
            `name` LIKE "{prefix}%"
            AND LENGTH(`name`) = {length}
        ORDER BY `name` DESC
        LIMIT 1;""".format(
        prefix=pattern['prefix'], length=len(pattern['prefix']) + pattern['length']),
        as_dict=True)
    
    if len(last_item_code) == 0:
        next_number = 1
    else:
        prefix_length = len(pattern['prefix'])
        last_number = cint((last_item_code[0]['name'])[prefix_length:])
        next_number = last_number + 1
    
    next_number_string = get_fixed_length_string(next_number, pattern['length'])
    
    return "{prefix}{n}".format(prefix=pattern['prefix'], n=next_number_string)
    
def get_fixed_length_string(n, length):
    next_number_string = "{0}{1}".format(
        (length * "0"), n)[((-1)*length):]
    # prevent duplicates on naming series overload
    if n > cint(next_number_string):
        next_number_string = "{0}".format(n)
    
    return next_number_string
    
