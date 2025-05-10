import mysql.connector
from tabulate import tabulate

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
		customer_name = input('Enter custumer\'s full name e.g. Mini Caravy : ')
		phone = input('Enter his/her phone number e.g. 88.60.1555 : ')
		query = f"SELECT * FROM customers WHERE customerName=\"{customer_name}\" AND phone=\"{phone}\""
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		return mycursor.fetchall()

	def employee(self): # input(lastName OR officeCode) output(employee record)
		employee_name = input('Enter employee\'s last name e.g. Patterson : ')
		officeCode = input('Enter his/her office code e.g.(1) : ')
		query = f"SELECT * FROM employees WHERE lastName=\"{employee_name}\" AND officeCode=\"{officeCode}\""
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		return mycursor.fetchall()
	
	def order(self): # input(customerName AND phone) output(order_detailes records)
		total_orders_result = '''
orders for customer = \"{customerName}\" with phone = [{customerPhone}]:\n
index\t\torder Date\t\trequired Date\t\tshipped Date\t\tstatus
-----------------------------------------------------------------------------------------------
'''
		order_row_str = '{orderNumber}\t\t{orderDate}\t\t{requiredDate}\t\t{shippedDate}\t\t{status}'

		customer_name = input('Enter custumer\'s full name who ordered e.g. Alpha Cognac : ')
		phone = input('Enter his/her phone number e.g. 61.77.6555 : ')
		total_orders_result = total_orders_result.format(customerName=customer_name, customerPhone=phone)
		mycursor = self.mydb.cursor()

		# get customerNumber
		query = f"SELECT * FROM customers WHERE customerName=\"{customer_name}\" AND phone=\"{phone}\""
		mycursor.execute(query)
		records = mycursor.fetchall()
		cusrtomer_number = records[0][0]

		# get orderNumbers
		query = f"SELECT * FROM orders WHERE customerNumber=\"{cusrtomer_number}\""
		mycursor.execute(query)
		order_table_records = mycursor.fetchall() # first item in in each value is orderNumber

		# display orders data
		for row_index, row in enumerate(order_table_records):
			total_orders_result += ( order_row_str.format(
				orderNumber=row_index, orderDate=row[1], requiredDate=row[2], shippedDate=row[3], status=row[4]
				)
			) + '\n'
		print(total_orders_result + '\n\n')
		
		# ask for more details
		see_products_details = input("want to see products details too (y/n)? ")
		see_products_details = True if see_products_details.lower() == 'y' else False
		if not see_products_details:
			return "ORDER REPORTS DONE!"

		print()
		tabulate_rows = []
		# display detailes of each order
		for row_index, row in enumerate(order_table_records):
			orderNumber = row[0] 
			query = f"SELECT * FROM orderdetails WHERE orderNumber=\"{orderNumber}\""
			mycursor.execute(query)
			one_order_products_records = mycursor.fetchall()

			for product_row in one_order_products_records:
				query = f"SELECT * FROM products WHERE productCode=\"{product_row[1]}\""
				mycursor.execute(query)
				product_record = mycursor.fetchone()
				tabulate_rows.append([row_index, product_record[1], product_row[2], product_row[3]])

		print(tabulate(tabulate_rows, headers=['index', 'product Name', 'quantity Ordered', 'price Each']))
		print()
		return "DETAILED ORDER REPORT DONE!" 
	
	def product(self): # input(productName) output(product record)
		product_name = input('Enter productName : ')
		query = f"SELECT * FROM products WHERE productName=\"{product_name}\""
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		return mycursor.fetchall()

	def statistics(self): 
		statistics_result = '\nall sells in this date:'
		sell_date_record = '{record}'
		mycursor = self.mydb.cursor()
		input_date = input("\ntype the date you want to get statistics from e.g. \'2004-01-31\': ")
		
		query = f"SELECT * FROM payments WHERE paymentDate=\"{input_date}\"" 
		mycursor.execute(query)
		all_records = mycursor.fetchall()
		for index, record in enumerate(all_records):
			statistics_result += ('\n' + f'{index+1}\tdate= {record[2]}\tamount= {record[3]}')

		statistics_result += '\n\n--------\n\nmost expensive sell: '
		query = f"SELECT MAX(amount) FROM payments WHERE paymentDate=\"{input_date}\""
		mycursor.execute(query)
		highest_price = mycursor.fetchall()
		statistics_result += str(highest_price[0][0]) + '\n'

		"most popular product bought this day: {}"

		return statistics_result



class Add(itemFinder): # CREATE 

	def __init__(self):
		super().__init__()
		self.mydb = connect_sql()
	
	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(all_columns) output(True/False)
		print('fill each info by typing anything you like:')
		customer_name = input('full name: ')
		contactLast_name = input('contact last name: ')
		contactFirst_name = input('contact first name : ')
		phone = input('phone number : ')
		address_line1 = input('address : ')
		city = input('city : ')
		country = input('country : ')
		
		query = f'''INSERT INTO customers (customerName, contactLastName, contactFirstName, phone, addressLine1, city, country)
VALUES (\"{customer_name}\", \"{contactLast_name}\", \"{contactFirst_name}\", \"{phone}\", \"{address_line1}\", \"{city}\", \"{country}\")'''
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		self.mydb.commit()
		print(mycursor.rowcount, "Record inserted successfully into customers table")
		return True

	def employee(self): # input(all_columns) output(True/False)
		print('fill each info by typing anything you like:')
		last_name = input('last name: ')
		first_name = input('first name: ')
		extension = 'x102'
		email = input('email: ')
		office_code = input('office code (1-7): ')
		job_title = input('job title: ')
		
		query = f'''INSERT INTO employees (lastName, firstName, extension, email, officeCode, jobTitle)
VALUES (\"{last_name}\", \"{first_name}\", \"{extension}\", \"{email}\", \"{office_code}\", \"{job_title}\")'''
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		self.mydb.commit()
		print(mycursor.rowcount, "Record inserted successfully into employees table")
		return True

	def order(self): # input(all_columns) output(True/False)
		pass

	def product(self): # input(all_columns) output(True/False)
		mycursor = self.mydb.cursor()
		choose_productline = {
			1: 'Classic Cars',
			2: 'Motorcycles',
			3: 'Planes',
			4: 'Ships',
			5: 'Trains',
			6: 'Trucks and Buses',
			7: 'Vintage Cars'
		}
		print('fill each info by typing anything you like:')
		
		# product_code = input("product code: ")
		product_name = input('product name: ')

		for key, value in choose_productline.items():
			print(f'{key}- {value}')
		product_line_num = int(input('choose relating product line number (1-7): '))
		product_line = choose_productline[product_line_num]
		
		product_scale = input('product scale (example 1:18) : ')
		product_vendor = input('product vendor (example Motor City Art Classics) : ')
		product_description = input('product description: ')
		quantity_in_stock = input('quantity in stock: ')
		buyPrice = input('buy price: ')
		MSRP = '0'
		
		query = f'''INSERT INTO products (productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
VALUES (\"{product_name}\", \"{product_line}\", \"{product_scale}\", \"{product_vendor}\", \"{product_description}\", \"{quantity_in_stock}\", \"{buyPrice}\", \"{MSRP}\")'''
		mycursor.execute(query)
		self.mydb.commit()
		print(mycursor.rowcount, "Record inserted successfully into employees table")
		return True		



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







Add()