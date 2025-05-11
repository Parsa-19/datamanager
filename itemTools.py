'''
contains some tools to manage items:
(customer, employee, order, product)
'''

class itemFinder(object):
	def __init__(self):
		self.item_methods = {
			'customer': self.customer,
			'employee': self.employee,
			'order': self.order,
			'product': self.product 
		}
