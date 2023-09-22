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
