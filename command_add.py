from tabulate import tabulate
import itemTools
import customizedSQLConnector as classicDB
import datetime
from datetime import timedelta, date
from mysql.connector import IntegrityError

class Add(itemTools.itemFinder): # CREATE 

	def __init__(self):
		super().__init__()
		self.mydb = classicDB.connect_sql()
	
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
		mycursor = self.mydb.cursor()

		print('[1] \nfirst tell us whos ordering? \nlog in to account: \n------------------')
		customer_name = input("full name e.g. \"Suominen Souveniers\": ")
		phone = input("phone e.g. \"+358 9 8045 555\": ")
		query = f"SELECT * FROM customers WHERE customerName=\"{customer_name}\" AND phone=\"{phone}\""
		mycursor.execute(query)
		customer_record = mycursor.fetchone()
		customer_number = customer_record[0]
		
		print('\n[2] \nEnter the name of product you want to order and type \"done\" whenever you ready!')
		basket = []
		done_ordering = ''
		while done_ordering.lower() != 'done':
			input_name = input('product\'s full name: ')
			done_ordering = input_name
			query = f'SELECT * FROM products WHERE productName=\"{input_name}\"'
			mycursor.execute(query)
			product_record = mycursor.fetchone()
			if product_record:
				product_record = list(product_record)
				product_description = product_record.pop(5)
				basket.append(product_record)
		
		# [3]
		order_number = None
		order_date = datetime.datetime.now()
		required_date = order_date + timedelta(days=5)
		try:
			query = f'''INSERT INTO orders (orderDate, requiredDate, status, customerNumber)
	VALUES (\"{order_date}\", \"{required_date}\", \"Shipped\", \"{customer_number}\")'''
			mycursor.execute(query)
			self.mydb.commit()
			print(f'\n==> {mycursor.rowcount} order record submitted')
			order_number = mycursor.lastrowid

		except IntegrityError as e:
			print(f'''\n*******************
<< order failed >>
probably the custumer number doesnt exists in customer table. CHECK THE YOUR ACCOUNT INFO OR RECREATE IT:
THE ERROR:
{e}
''')
			return None

		# [4]
		for product in basket:
			product_code = product[0]
			quantity_ordered = '1' 
			price_each = product[-2]
			orderLine_number = '1'
			try:
				query = f'''INSERT INTO orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
VALUES (\"{order_number}\", \"{product_code}\", \"{quantity_ordered}\", \"{price_each}\", \"{orderLine_number}\")'''
				mycursor.execute(query)
				self.mydb.commit()
				print(f'--> {mycursor.rowcount} product record added to orderDetails')
			except IntegrityError as e:
				print(f'''****************
<< order failed >>
you probably entered product {product[1]} more than one time. try again. error:
{e}
''')
				return None

		print(f'\n(REPORT THE ORDER)\nINSIDE YOUR BASKET:')
		print( tabulate(basket, headers=[
			'productCode', 'productName', 'productLine', 'productScale', 'productVendor', 'quantityInStock', 'buyPrice', 'MSRP']
			))
		print(f'''
order is submitted on = {order_date}
you'll get the order on = {required_date}
			''')
		return 'FINISH addin order!'


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
		
		product_code = input("a unique product code like S99-010101: ")
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
		
		try:
			query = f'''INSERT INTO products (productCode, productName, productLine, productScale, productVendor, productDescription, quantityInStock, buyPrice, MSRP)
VALUES (\"{product_code}\", \"{product_name}\", \"{product_line}\", \"{product_scale}\", \"{product_vendor}\", \"{product_description}\", \"{quantity_in_stock}\", \"{buyPrice}\", \"{MSRP}\")'''
			mycursor.execute(query)
			self.mydb.commit()
			print(mycursor.rowcount, "Record inserted successfully into employees table")
			return True
		except Exception as e:
			print(f"\n*******************\ncouldnt add this product due to:\n{e}\ntry again..")

