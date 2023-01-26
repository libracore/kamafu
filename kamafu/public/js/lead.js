/*
 * 
 * Additional script functions for the lead doctype
 * 
 */

// filter queries
cur_frm.fields_dict.contact.get_query =   
    function(frm) {
        return {
            query: "frappe.contacts.doctype.contact.contact.contact_query",
            filters: {
                "link_doctype": "Customer",
                "link_name": cur_frm.doc.customer || null
            }
        }
    };
    
frappe.ui.form.on('Lead', {
    customer(frm) {
        // fetch customer data
        if (frm.doc.customer) {
            get_customer(frm);
        }
    },
    contact(frm) {
        // fetch customer data
        if (frm.doc.contact) {
            get_contact(frm);
        }
    }
});

function get_customer(frm) {
    frappe.call({
        "method": "frappe.client.get",
        "args": {
            "doctype": "Customer",
            "name": frm.doc.customer
        },
        "callback": function(response) {
            var customer = response.message;
            cur_frm.set_value("company_name", customer.customer_name);
            
        }
    });
}

function get_contact(frm) {
    frappe.call({
        "method": "frappe.client.get",
        "args": {
            "doctype": "Contact",
            "name": frm.doc.contact
        },
        "callback": function(response) {
            var contact = response.message;
            cur_frm.set_value("lead_name", (contact.first_name || "") + " " + (contact.last_name || ""));
            cur_frm.set_value("email_id", contact.email_id || "");
        }
    });
}
