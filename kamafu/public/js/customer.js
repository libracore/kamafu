/*
 * 
 * Script extensions for customer
 * 
 */

try {
    cur_frm.dashboard.add_transactions([
        {
            'label': 'Leads',
            'items': ['Lead']
        }
    ]);
} catch { /* do nothing for older versions */ }
        
frappe.ui.form.on('Lead', {
    refresh(frm) {
        
    }
});
