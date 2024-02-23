// common functions for kamafu

function update_tax(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "tax_amount", (row.base_net_amount || 0) * ((row.tax_rate || 0) / 100));
}

function compile_sales_taxes(frm) {
    if ((frm.doc.items) && ((frm.doc.taxes_and_charges || "").includes("Automatisch"))) {
        // find taxes by rate
        var total_normal_tax = 0;
        var total_reduced_tax = 0;
        for (var i = 0; i < frm.doc.items.length; i++) {
            if (frm.doc.items[i].tax_rate < 5) {
                total_reduced_tax += frm.doc.items[i].tax_amount;
            } else {
                total_normal_tax += frm.doc.items[i].tax_amount;
            }
        }
        
        if (frm.doc.taxes.length !== 2) {
            frappe.msgprint(__("Ungültige Steuereinstellung. Bitte die Vorlage neu laden.") );
        } else {
            frappe.model.set_value(frm.doc.taxes[0].doctype, frm.doc.taxes[0].name, "description", "8.1% MwSt");
            frappe.model.set_value(frm.doc.taxes[0].doctype, frm.doc.taxes[0].name, "tax_amount", total_normal_tax);
            frappe.model.set_value(frm.doc.taxes[1].doctype, frm.doc.taxes[1].name, "description", "2.6% MwSt");
            frappe.model.set_value(frm.doc.taxes[1].doctype, frm.doc.taxes[1].name, "tax_amount", total_reduced_tax);
            cur_frm.refresh_fields("taxes");
        }
    }
}

function compile_purchase_taxes(frm) {
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

function set_sales_tax_rate(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    frappe.call({
        "method": "kamafu.kamafu.utils.get_item_tax_rate",
        "args": {
            "item_code": row.item_code,
            "sales": 1
        },
        "callback": function(response) {
            var tax_rate = response.message;
            frappe.model.set_value(cdt, cdn, "tax_rate", tax_rate);
        }
    });
}
