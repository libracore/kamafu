// Copyright (c) 2021-2023, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoice', {
    before_save: function(frm) {
        if (frm.doc.items) {
            for (var i = 0; i < frm.doc.items.length; i++) {
                update_tax(frm, frm.doc.items[i].doctype, frm.doc.items[i].name);
            }
            compile_taxes(frm);
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

function update_tax(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "tax_amount", (row.base_net_amount || 0) * ((row.tax_rate || 0) / 100));
}

function compile_taxes(frm) {
    if ((frm.doc.items) && ((frm.doc.taxes_and_charges || "").includes("Automatisch"))) {
        // find taxes by rate
        var total_direct_tax = 0;
        var total_indirect_tax = 0;
        for (var i = 0; i < frm.doc.items.length; i++) {
            
            if (["4"].includes(frm.doc.items[i].expense_account.substring(0, 1))) {
                total_direct_tax += frm.doc.items[i].tax_amount;
            } else {
                total_indirect_tax += frm.doc.items[i].tax_amount;
            }
        }
        
        if (frm.doc.taxes.length !== 2) {
            frappe.msgprint(__("Ungültige Steuereinstellung. Bitte die Vorlage neu laden.") );
        } else {
            for (var t = 0; t < frm.doc.taxes.length; t++) {
                if (frm.doc.taxes[t].account_head.substring(0, 4) === "1170") {
                    frappe.model.set_value(frm.doc.taxes[t].doctype, frm.doc.taxes[t].name, "tax_amount", total_direct_tax);
                } else {
                    frappe.model.set_value(frm.doc.taxes[t].doctype, frm.doc.taxes[t].name, "tax_amount", total_indirect_tax);
                }
            }
            cur_frm.refresh_fields("taxes");
        }
    }
}

