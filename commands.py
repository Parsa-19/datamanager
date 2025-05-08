import mysql.connector

class itemFinder(object):
	def __init__(self):
		self.item_methods = {
			'customer': self.customer,
			'employee': self.employee,
			'order': self.order,
			'product': self.product 
		}

def connect_sql():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		database="classicmodels"
	)
	return mydb

class Find(itemFinder): # SELECT
	
	def __init__(self):
		super().__init__()
		self.mydb = connect_sql()
	
	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(customerName OR phone) output(customer record)
		customer_name = input('Enter custumerName : ')
		phone = input('Enter phone number : ')
		query = f"SELECT * FROM customers WHERE customerName=\"{customer_name}\" AND phone=\"{phone}\""
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		return mycursor.fetchall()

	def employee(self): # input(lastName OR officeCode) output(employee record)
		employee_name = input('Enter employeeName : ')
		officeCode = input('Enter officeCode : ')
		query = f"SELECT * FROM employees WHERE lastName=\"{employee_name}\" AND officeCode=\"{officeCode}\""
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		return mycursor.fetchall()
	
	def order(self): # input(customerName AND phone) output(order_detailes records)
		customer_name = input('Enter custumerName : ')
		phone = input('Enter phone number : ')
		mycursor = self.mydb.cursor()

		# get customerNumber
		query = f"SELECT * FROM customers WHERE customerName=\"{customer_name}\" AND phone=\"{phone}\""
		mycursor.execute(query)
		records = mycursor.fetchall()
		cusrtomer_number = records[0][0]

		# get orderNumber
		query = f"SELECT * FROM orders WHERE customerNumber=\"{cusrtomer_number}\""
		mycursor.execute(query)
		records = mycursor.fetchall()
		return records

		# get orderDetailes
	
	def product(self): # input(productName) output(product record)
		product_name = input('Enter productName : ')
		query = f"SELECT * FROM products WHERE productName=\"{product_name}\""
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		return mycursor.fetchall()

	def amar(self):
		pass



class Add(itemFinder): # CREATE 

	def __init__(self):
		super().__init__()
		self.mydb = connect_sql()
	
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
		self.mydb = connect_sql()

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
		self.mydb = connect_sql()

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

