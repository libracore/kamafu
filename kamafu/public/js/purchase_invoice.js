// Copyright (c) 2021-2023, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
    before_save: function(frm) {
        if (frm.doc.items) {
            for (var i = 0; i < frm.doc.items.length; i++) {
                update_tax(frm, frm.doc.items[i].doctype, frm.doc.items[i].name);
            }
            compile_purchase_taxes(frm);
        }
    }
});

frappe.ui.form.on('Purchase Invoice Item', {
    rate: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    },    
    base_net_amount: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    },
    tax_rate: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    },
	item_code: function(frm, cdt, cdn) {
        // this is to force loading the tax rate because the core fetch is very unreliable
		var row = locals[cdt][cdn];
		if (row.item_code) {
		    frappe.call({
                "method": "frappe.client.get",
                "args": {
                    "doctype": "Item",
                    "name": row.item_code
                },
                "callback": function(response) {
                    var item = response.message;
                    if ((item.item_defaults.length > 0) && (item.item_defaults[0].expense_account)) {
                        frappe.call({
                            "method": "frappe.client.get",
                            "args": {
                                "doctype": "Account",
                                "name": item.item_defaults[0].expense_account
                            },
                            "callback": function(response) {
                                var account = response.message;
                                frappe.model.set_value(cdt, cdn, "tax_rate", account.steuersatz);
                            }
                        });
                    } 
                }
            });
		}
	}
});

