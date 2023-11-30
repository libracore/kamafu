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
    base_net_amount: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    },
    tax_rate: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    }
});
