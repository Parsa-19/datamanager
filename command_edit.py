import itemTools
import customizedSQLConnector as classicDB

class Edit(itemTools.itemFinder): # UPDATE
	
	def __init__(self):
		super().__init__()
		self.mydb = classicDB.connect_sql()

	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(custumerName -> essential column values to change) output(True/False)
		pass
	def employee(self): # input(employeeName -> essential column values to change) output(True/False)
		pass
	def order(self): # input(customerName -> essential column values to change) output(True/False)
		pass
	def product(self): # input(choose between columns) output(True/False)
		pass