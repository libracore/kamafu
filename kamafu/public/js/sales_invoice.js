// Copyright (c) 2021-2023, libracore AG and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        // check if there are available akonto positions
        if (frm.doc.__islocal) {
            find_akontos(frm);
        }
    },
    on_submit: function(frm) {
        check_create_akonto_booking(frm);
    },
    before_save: function(frm) {
        if (frm.doc.items) {
            for (var i = 0; i < frm.doc.items.length; i++) {
                update_tax(frm, frm.doc.items[i].doctype, frm.doc.items[i].name);
            }
            compile_taxes(frm);
        }
    }
});

frappe.ui.form.on('Sales Invoice Item', {
    base_net_amount: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    },
    tax_rate: function(frm, cdt, cdn) {
        update_tax(frm, cdt, cdn);
    }
});

function find_akontos(frm) {
    if ((frm.doc.items) && (frm.doc.items.length > 0)) {
        frappe.call({
            "method": "kamafu.kamafu.utils.get_available_akonto",
            "args": {
                "sales_order": frm.doc.items[0].sales_order
            },
            "callback": function(response) {
                var akonto = response.message;
                console.log(akonto);
                if (akonto.length > 0) {
                    var akonto_total = 0;
                    cur_frm.clear_table("akontos");
                    for (var a = 0; a < akonto.length; a++) {
                        add_akonto(
                            "Akonto vom " + new Date(akonto[a].date).toLocaleString("de", {'day': '2-digit', 'month': '2-digit', 'year': 'numeric'}) + " (" + frm.doc.currency + " " + akonto[a].amount.toLocaleString("de-ch") + " inkl. MwSt)", 
                            akonto[a].amount, 
                            akonto[a].net_amount, 
                            akonto[a].reference
                        );
                        akonto_total += akonto[a].net_amount;
                    }
                    cur_frm.set_value("apply_discount_on", "Net Total");
                    cur_frm.set_value("discount_amount", akonto_total);
                }
            }
        });
    }
}

function add_akonto(text, amount, net_amount, reference) {
    var child = cur_frm.add_child('akontos');
    frappe.model.set_value(child.doctype, child.name, 'description', text);
    frappe.model.set_value(child.doctype, child.name, 'amount', net_amount);
    frappe.model.set_value(child.doctype, child.name, 'akonto_net_amount', net_amount);
    frappe.model.set_value(child.doctype, child.name, 'akonto_gross_amount', amount);
    frappe.model.set_value(child.doctype, child.name, 'akonto_invoice_item', reference);
    cur_frm.refresh_field('akontos');
}

// This function checks if an akonto has been used and books it
function check_create_akonto_booking(frm) {
    if (frm.doc.akontos) {
        for (var a = 0; a < frm.doc.akontos.length; a++) {
            if (frm.doc.akontos[a].akonto_invoice_item) {
                frappe.call({
                    "method": "kamafu.kamafu.utils.book_akonto",
                    "args": {
                        "sales_invoice": frm.doc.name,
                        "net_amount": frm.doc.akontos[a].akonto_net_amount
                    },
                    "callback": function(response) {
                        console.log("Akonto booked: " + response.message);

                    }
                });
            }
        }
    }
}

function update_tax(frm, cdt, cdn) {
    var row = locals[cdt][cdn];
    frappe.model.set_value(cdt, cdn, "tax_amount", (row.base_net_amount || 0) * ((row.tax_rate || 0) / 100));
}

function compile_taxes(frm) {
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

