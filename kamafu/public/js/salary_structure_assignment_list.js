frappe.listview_settings['Salary Structure Assignment'] = {
	onload: function(listview) {
		// your code here
		frappe.route_options = {"docstatus": ["=",1]};
	}
}
