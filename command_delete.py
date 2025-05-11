import itemTools
import customizedSQLConnector as classicDB

class Delete(itemTools.itemFinder): # DELETE

	def __init__(self):
		super().__init__()
		self.mydb = classicDB.connect_sql()

	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(key_column_value) output(True/False)
		pass
	def employee(self): # input(key_column_value) output(True/False)
		pass
	def order(self): # input(key_column_value) output(True/False)
		pass
	def product(self): # input(key_column_value) output(True/False)
		pass


