import mysql.connector

class itemFinder(object):
	def __init__(self):
		self.item_methods = {
			'customer': self.customer,
			'employee': self.employee,
			'order': self.order,
			'product': self.product 
		}

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	database="classicmodels"
)


class Find(itemFinder): # SELECT
	
	def __init__(self):
		super().__init__()
		global mydb
		self.mydb = mydb
	
	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(customerName OR phone) output(customer record)
		customer_name = input('Enter custumerName : ')
		phone = input('Enter phone number : ')
		query = ""
		mycursor = mydb.cursor()
		mycursor.execute(query)
		return mycursor.fetchall()

	def employee(self): # input(lastName OR officeCode) output(employee record)
		print('inside employee')
	
	def order(self): # input(customerName AND phone) output(order_detailes records)
		print('inside order')
	
	def product(self): # input(productName) output(product record)
		print('inside product')

	def amar(self):
		pass



class Add(itemFinder): # CREATE 

	def __init__(self):
		super().__init__()
		global mydb
		self.mydb = mydb
	
	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(all_columns) output(True/False)
		pass
	def employee(self): # input(all_columns) output(True/False)
		pass
	def order(self): # input(all_columns) output(True/False)
		pass
	def product(self): # input(all_columns) output(True/False)
		pass



class Edit(itemFinder): # UPDATE
	
	def __init__(self):
		super().__init__()
		global mydb
		self.mydb = mydb

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



class Delete(itemFinder): # DELETE

	def __init__(self):
		super().__init__()
		global mydb
		self.mydb = mydb

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


mydb.close()