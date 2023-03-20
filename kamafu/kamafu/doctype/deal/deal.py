# -*- coding: utf-8 -*-
# Copyright (c) 2023, libracore AG and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import (cstr, validate_email_address, cint, comma_and, has_gravatar, now, getdate, nowdate)
from frappe.model.mapper import get_mapped_doc

from erpnext.controllers.selling_controller import SellingController
from frappe.contacts.address_and_contact import load_address_and_contact
from erpnext.accounts.party import set_taxes
from frappe.email.inbox import link_communication_to_document
from frappe.model.document import Document

class Deal(Document):
	pass

@frappe.whitelist()
def make_customer(source_name, target_doc=None):

	return _make_customer(source_name, target_doc)

def _make_customer(source_name, target_doc=None, ignore_permissions=False):
	def set_missing_values(source, target):
		if source.company_name:
			target.customer_type = "Company"
			target.customer_name = source.company_name
		else:
			target.customer_type = "Individual"
			target.customer_name = source.lead_name

		target.customer_group = frappe.db.get_default("Customer Group")

	doclist = get_mapped_doc("Deal", source_name,
		{"Deal": {
			"doctype": "Customer",
			"field_map": {
				"name": "deal_name",
				"company_name": "customer_name",
				"contact_no": "phone_1",
				"fax": "fax_1"
			}
		}}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)
	
	return doclist

@frappe.whitelist()
def make_opportunity(source_name, target_doc=None):
	def set_missing_values(source, target):
		address = frappe.get_all('Dynamic Link', {
			'link_doctype': source.doctype,
			'link_name': source.name,
			'parenttype': 'Address',
		}, ['parent'], limit=1)

		if address:
			target.customer_address = address[0].parent

	target_doc = get_mapped_doc("Deal", source_name,
		{"Deal": {
			"doctype": "Opportunity",
			"field_map": {
				"campaign_name": "campaign",
				"doctype": "opportunity_from",
				"customer": "party_name",
				"lead_name": "contact_display",
				"company_name": "customer_name",
				"email_id": "contact_email",
				"mobile_no": "contact_mobile"
			}
		}}, target_doc, set_missing_values)

	return target_doc

@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	target_doc = get_mapped_doc("Deal", source_name,
		{"Deal": {
			"doctype": "Quotation",
			"field_map": {
				"customer": "party_name"
			}
		}}, target_doc)
	target_doc.quotation_to = "Customer"
	target_doc.run_method("set_missing_values")
	target_doc.run_method("set_other_charges")
	target_doc.run_method("calculate_taxes_and_totals")

	return target_doc
