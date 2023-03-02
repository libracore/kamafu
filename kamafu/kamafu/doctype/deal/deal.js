// Copyright (c) 2023, libracore AG and contributors
// For license information, please see license.txt

var customer;

frappe.ui.form.on('Deal', {

	onload: function (frm) {
		if (cur_frm.fields_dict.lead_owner.df.options.match(/^User/)) {
			cur_frm.fields_dict.lead_owner.get_query = function (doc, cdt, cdn) {
				return { query: "frappe.core.doctype.user.user.user_query" }
			}
		}

		if (cur_frm.fields_dict.contact_by.df.options.match(/^User/)) {
			cur_frm.fields_dict.contact_by.get_query = function (doc, cdt, cdn) {
				return { query: "frappe.core.doctype.user.user.user_query" }
			}
		}
		
		var last_route = frappe.route_history.slice(-2, -1)[0];
		if (last_route) {
            if (last_route[1] == "Customer") {
                console.log("last_route", last_route)
                frm.set_value("customer", last_route[2]);
            }
        }
        
        if (frm.doc.owner) {
           frm.set_value("lead_owner", frm.doc.owner);
        }
	},

	refresh: function (frm) {
		
		frm.page.add_inner_button('Quotation', (frm) => make_quotation(), 'Create')
		frm.page.add_inner_button('Opportunity', (frm) => create_opportunity(), 'Create')
		
		
		frm.fields_dict.customer.get_query = function (doc, cdt, cdn) {
			return { query: "erpnext.controllers.queries.customer_query" }
		}

		frm.toggle_reqd("lead_name", !frm.doc.organization_lead);
		
		
		if (frm.doc.customer) {
			customer = frm.doc.customer;
		} else {
			frm.page.add_inner_button('Customer', (frm) => create_customer(), 'Create')
		}
		
	},
	validate: function (frm) {
		// If the link added, make changes in the linked document
		if (frm.doc.customer) {
			setTimeout(function(){
				set_customer(frm, frm.doc.name)
			}, 1000);
		}
	}, 
	customer: function(frm) {
		// If the link is removed, make changes in the linked document
		if (!frm.doc.customer) {
			set_customer(frm, "")
		}
	},

	organization_lead: function (frm) {
		frm.toggle_reqd("lead_name", !frm.doc.organization_lead);
		frm.toggle_reqd("company_name", frm.doc.organization_lead);
	},

	company_name: function (frm) {
		if (frm.doc.organization_lead == 1) {
			frm.set_value("lead_name", frm.doc.company_name);
		}
	},

	contact_date: function (frm) {
		if (frm.doc.contact_date) {
			let d = moment(frm.doc.contact_date);
			d.add(1, "hours");
			frm.set_value("ends_on", d.format(frappe.defaultDatetimeFormat));
		}
	}
});

function create_customer(frm){
	console.log("create_customer")
	var doc = frappe.model.open_mapped_doc({
		method: "kamafu.kamafu.doctype.deal.deal.make_customer",
		frm: cur_frm
	})
	console.log("doc", doc.name)
	
}

function make_quotation(frm){
	frappe.model.open_mapped_doc({
		method: "kamafu.kamafu.doctype.deal.deal.make_quotation",
		frm: cur_frm
	})
}

function create_opportunity(frm){
	frappe.model.open_mapped_doc({
		method: "kamafu.kamafu.doctype.deal.deal.make_opportunity",
		frm: cur_frm
	})
}

function set_customer(frm, value){

	var doctype_name = customer || frm.doc.customer
	
	frappe.call({
		'method': "frappe.client.set_value",
		'args': {
			'doctype': "Customer",
			'name': doctype_name,
			'fieldname': {
					"deal_name": value,
			},
		},
    });
	
}
