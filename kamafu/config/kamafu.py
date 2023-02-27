from __future__ import unicode_literals
from frappe import _

def get_data():
    return[
        {
            "label": _("CRM"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Lead",
                    "label": _("Lead"),
                    "description": _("Lead")
                },
                {
                    "type": "doctype",
                    "name": "Customer",
                    "label": _("Customer"),
                    "description": _("Customer")
                },
                {
                    "type": "doctype",
                    "name": "Contact",
                    "label": _("Contact"),
                    "description": _("Contact")
                },
                {
                    "type": "doctype",
                    "name": "Event",
                    "label": _("Event"),
                    "description": _("Event")
                },
                {
                    "type": "doctype",
                    "name": "ToDo",
                    "label": _("ToDo"),
                    "description": _("ToDo")
                }
            ]
        },
        {
            "label": _("Selling"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Customer",
                    "label": _("Customer"),
                    "description": _("Customer")
                },
                {
                    "type": "doctype",
                    "name": "Item",
                    "label": _("Item"),
                    "description": _("Item")
                },
                {
                    "type": "doctype",
                    "name": "Quotation",
                    "label": _("Quotation"),
                    "description": _("Quotation")
                },
                {
                    "type": "doctype",
                    "name": "Sales Order",
                    "label": _("Sales Order"),
                    "description": _("Sales Order")
                },
                {
                    "type": "doctype",
                    "name": "Sales Invoice",
                    "label": _("Sales Invoice"),
                    "description": _("Sales Invoice")
                },
                {
                    "type": "doctype",
                    "name": "Payment Reminder",
                    "label": _("Payment Reminder"),
                    "description": _("Payment Reminder")
                },
                {
                    "type": "report",
                    "name": "Accounts Receivable",
                    "label": _("Accounts Receivable"),
                    "doctype": "Sales Invoice",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Offene Kundenguthaben",
                    "label": _("Offene Kundenguthaben"),
                    "doctype": "Sales Invoice",
                    "is_query_report": True
                }
            ]
        },
        {
            "label": _("Buying"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "doctype",
                    "name": "Supplier",
                    "label": _("Supplier"),
                    "description": _("Supplier")
                },
                {
                    "type": "doctype",
                    "name": "Purchase Invoice",
                    "label": _("Purchase Invoice"),
                    "description": _("Purchase Invoice")
                },
                {
                    "type": "report",
                    "name": "Accounts Payable",
                    "label": _("Accounts Payable"),
                    "doctype": "Purchase Invoice",
                    "is_query_report": True
                }
            ]
        },
        {
            "label": _("Banking"),
            "icon": "fa fa-money",
            "items": [
                   {
                       "type": "page",
                       "name": "bank_wizard",
                       "label": _("Bank Wizard"),
                       "description": _("Bank Wizard")
                   },
                   {
                       "type": "doctype",
                       "name": "Payment Proposal",
                       "label": _("Payment Proposal"),
                       "description": _("Payment Proposal")
                   }
            ]
        },
                {
            "label": _("Finance"),
            "icon": "fa fa-money",
            "items": [
                {
                    "type": "report",
                    "name": "General Ledger",
                    "label": _("General Ledger"),
                    "doctype": "GL Entry",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Balance Sheet",
                    "label": _("Balance Sheet"),
                    "doctype": "GL Entry",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Profit and Loss Statement",
                    "label": _("Profit and Loss Statement"),
                    "doctype": "GL Entry",
                    "is_query_report": True
                },
                {
                    "type": "doctype",
                    "name": "Payment Entry",
                    "label": _("Payment Entry"),
                    "description": _("Payment Entry")
                },
                {
                    "type": "doctype",
                    "name": "Journal Entry",
                    "label": _("Journal Entry"),
                    "description": _("Journal Entry")
                },
                {
                    "type": "doctype",
                    "name": "VAT Declaration",
                    "label": _("VAT Declaration"),
                    "description": _("VAT Declaration")
                },
                {
                    "type": "report",
                    "name": "Kontrolle MwSt",
                    "label": _("Kontrolle MwSt"),
                    "doctype": "Sales Invoice",
                    "is_query_report": True
                },
                {
                    "type": "report",
                    "name": "Account Sheets",
                    "label": _("Account Sheets"),
                    "doctype": "GL Entry",
                    "is_query_report": True
                }
            ]
        },
        {
            "label": _("Human Resources"),
            "icon": "fa fa-users",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Employee",
                       "label": _("Employee"),
                       "description": _("Employee")
                   },
                   {
                       "type": "doctype",
                       "name": "Timesheet",
                       "label": _("Timesheet"),
                       "description": _("Timesheet")
                   },
                   {
                       "type": "doctype",
                       "name": "Salary Structure Assignment",
                       "label": _("Salary Structure Assignment"),
                       "description": _("Salary Structure Assignment")
                   },
                   {
                       "type": "doctype",
                       "name": "Payroll Entry",
                       "label": _("Payroll Entry"),
                       "description": _("Payroll Entry")
                   },
                   {
                       "type": "doctype",
                       "name": "Salary Certificate",
                       "label": _("Salary Certificate"),
                       "description": _("Salary Certificate")
                   },
                   {
                        "type": "report",
                        "name": "Worktime Overview",
                        "label": _("Worktime Overview"),
                        "doctype": "Timesheet",
                        "is_query_report": True
                   },
                   {
                        "type": "report",
                        "name": "Monthly Worktime",
                        "label": _("Monthly Worktime"),
                        "doctype": "Timesheet",
                        "is_query_report": True
                   },
                   {
                        "type": "report",
                        "name": "Annual Salary Sheet",
                        "label": _("Annual Salary Sheet"),
                        "doctype": "Salary Slip",
                        "is_query_report": True
                   }
            ]
        },
        {
            "label": _("Settings"),
            "icon": "fa fa-users",
            "items": [
                   {
                       "type": "doctype",
                       "name": "Kamafu Settings",
                       "label": _("Kamafu Settings"),
                       "description": _("Kamafu Settings")
                   }
            ]
        }
    ]
    
