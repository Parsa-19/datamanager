from tabulate import tabulate
import itemTools
import customizedSQLConnector as classicDB

class Delete(itemTools.itemFinder): # DELETE

	def __init__(self):
		super().__init__()
		self.mydb = classicDB.connect_sql()

	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(key_column_value) output(True/False)
		customer_name = input("\ncustomer\'s full name: ")
		phone = input("phone: ")
		query = f'DELETE FROM customers WHERE customerName=\"{customer_name}\" AND phone=\"{phone}\"'
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		self.mydb.commit()
		print('deleted!')
		return True

	def employee(self): # input(key_column_value) output(True/False)
		employee_lastname = input("\nemployees\'s last name: ")
		email = input("email: ")
		query = f'DELETE FROM employees WHERE lastName=\"{employee_lastname}\" AND email=\"{email}\"'
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		self.mydb.commit()
		print('deleted!')
		return True

	def order(self): # input(key_column_value) output(True/False)
		mycursor = self.mydb.cursor()

		# get customerNumber
		print("\nwhos order you want to delete?")
		customer_name = input("customer\'s full name: ")
		phone = input("phone: ")
		query = f'SELECT * FROM customers WHERE customerName=\"{customer_name}\" AND phone=\"{phone}\"'
		mycursor.execute(query)
		customer_record = mycursor.fetchone()
		customer_number = customer_record[0]

		# get customer's orders(orderNumbers) and choose order number
		query = f'SELECT * FROM orders WHERE customerNumber=\"{customer_number}\"'
		mycursor.execute(query)
		customer_order_records = mycursor.fetchall()
		print()
		print( tabulate(customer_order_records, headers=[
			'orderNumber', 'orderDate', 'requiredDate', 'shippedDate', 'status', '', 'customerNumber']) )
		print(f'\n # choose the order you want to DELETE for customer \"{customer_name}\" by orderNumber :')
		chosen_order_number = input('\n --> orderNumber: ')

		# detele specific order by orderNumber
		query = f'DELETE FROM orders WHERE orderNumber=\"{chosen_order_number}\"'
		mycursor.execute(query)
		self.mydb.commit()
		print('deleted!')
		return True

	def product(self): # input(key_column_value) output(True/False)
		product_name = input("\nproduct name: ")
		query = f'DELETE FROM products WHERE productName=\"{product_name}\"'
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		self.mydb.commit()
		print('deleted!')
		return True


