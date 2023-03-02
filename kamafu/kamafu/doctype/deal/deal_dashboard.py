from frappe import _

def get_data():
   return {
      'fieldname': 'deal_name',
      'transactions': [
         {
            'items': ['Opportunity']
         },
         {
            'items': ['Quotation']
         },
      ]
   }
