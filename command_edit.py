from tabulate import tabulate
import itemTools
import customizedSQLConnector as classicDB

class Edit(itemTools.itemFinder): # UPDATE
	
	def __init__(self):
		super().__init__()
		self.mydb = classicDB.connect_sql()

	def get_method(self, item):
		return self.item_methods[item]

	def customer(self): # input(custumerName -> essential column values to change) output(True/False)
		mycursor = self.mydb.cursor()
		
		print("\n[1] which customer you want to edit?")
		old_customer_name = input("customer\'s full name (old): ")
		old_phone = input("phone (old): ")

		print('\n[2] fill each line with new value for this customer to update and\ntype nothing or hit enter to keep those you dont want to change:')
		customer_columns = {
			"customerName": input("new cusomer's full name: ") ,
			"contactLastName": input("new customer's contact last name: ") , 
			"contactFirstName": input("new customer's contact first name: ") ,
			"phone": input("new phone: ") ,
			"addressLine1": input("new address: ") ,
			"city": input("new city: ") ,
			"country": input("new country: ")
			}

		query_command = 'UPDATE customers '
		query_values = 'SET '
		query_condition = f' WHERE customerName=\"{old_customer_name}\" AND phone=\"{old_phone}\"' 
		
		for database_column_name, new_value in customer_columns.items():
			if len(new_value) == 0 or new_value.isspace():
				continue
			query_values += ( database_column_name + f'=\"{new_value}\",' )
		else: # if for didnt break and 'query_values' successfully made then remove last comma at end of string
			query_values = query_values[:-1] 

		query = query_command + query_values + query_condition
		mycursor.execute(query)
		self.mydb.commit()

		if mycursor.rowcount >= 1:
			print(mycursor.rowcount, "Record updated successfully")
			return True


	def employee(self): # input(employeeName -> essential column values to change) output(True/False)
		mycursor = self.mydb.cursor()

		print("\n[1] which employee you want to edit?")
		old_employee_name = input('employee\'s last name(old): ')
		old_office_code = input('office code(1-7) (old): ')

		print('\n[2] fill each line with new value for this employee to update and\ntype nothing or hit enter to keep those you dont want to change:')
		employee_columns = {
			"lastName": input("new employee last name: ") ,
			"firstName": input("new employee first name: ") , 
			"email": input("new email: ") ,
			"officeCode": input("new office code(1-7): ") ,
			"jobTitle": input("new job title: ")
			}

		query_command = 'UPDATE employees '
		query_values = 'SET '
		query_condition = f' WHERE lastName=\"{old_employee_name}\" AND officeCode=\"{old_office_code}\"' 
		
		for database_column_name, new_value in employee_columns.items():
			if len(new_value) == 0 or new_value.isspace(): 
				continue
			query_values += ( database_column_name + f'=\"{new_value}\",' )
		else: # if for didnt break and 'query_values' successfully made then remove last comma at end of string
			query_values = query_values[:-1]

		query = query_command + query_values + query_condition
		mycursor.execute(query)
		self.mydb.commit()

		if mycursor.rowcount >= 1:
			print(mycursor.rowcount, "Record updated successfully")
			return True


	def order(self): # input(customerName -> essential column values to change) output(True/False)
		mycursor = self.mydb.cursor()

		# get customerNumber
		print('\nwho\'s order for you want to edit?')
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
		print(f'\n # choose the order you want to edit for customer \"{customer_name}\" by orderNumber :')
		chosen_order_number = input('\n --> orderNumber: ') 

		# get order's products 
		query = f'SELECT * FROM orderdetails WHERE orderNumber=\"{chosen_order_number}\"'
		mycursor.execute(query)
		orderdetails_records = mycursor.fetchall()
		# replace all productCodes with their names
		current_order_productCodes = {} # "product_name": "product_Code "
		for i, product in enumerate(orderdetails_records):
			product = list(product)
			product_code = product[1]
			query = f'SELECT * FROM products WHERE productCode=\"{product_code}\"'
			mycursor.execute(query)
			product_record = mycursor.fetchone()
			product_name = product_record[1]
			product[1] = product_name # replace product_name in each orderdetails record 
			orderdetails_records[i] = product # gather recoreds in one "orderdetails_records"
			current_order_productCodes[product_name] = product_code 
		print()
		print('[inside this order] :')
		print( tabulate(orderdetails_records, headers=[
			'orderNumber', 'productName', 'quantityOrdered', 'priceEach', 'orderLineNumber' ]) )

		# choose any of them(products) to edit and replace new product code in orderdetails 
		print('\n # enter new product to replace, \n # type delete for each product to remove \n # and leave blank to keep that product :')
		try:
			for product_in_order in orderdetails_records:
				new_product_name = input(f"\t ** change \"{product_in_order[1]}\" to: ")
				current_product_code = current_order_productCodes[product_in_order[1]]

				if new_product_name.lower() == 'delete':
					query = f'DELETE FROM orderdetails WHERE productCode=\"{current_product_code}\" AND orderNumber=\"{chosen_order_number}\"'
					mycursor.execute(query)
					self.mydb.commit()
					print(f'\t ** {mycursor.rowcount} row deleted')
					continue

				elif len(new_product_name) == 0 or new_product_name.isspace():
					print("\t ** keeping it..")
					continue
								
				query = f'SELECT * FROM products WHERE productName=\"{new_product_name}\"'
				mycursor.execute(query)
				product_record = mycursor.fetchone()
				new_product_code = product_record[0]
				query = f'''UPDATE orderdetails
	SET productCode=\"{new_product_code}\"
	WHERE productCode=\"{current_product_code}\" AND orderNumber=\"{chosen_order_number}\"'''
				mycursor.execute(query)
				self.mydb.commit()
				print("\t ** changed!" if mycursor.rowcount >= 1 else "\t ** didnt change (failed)")
		
		except Exception as e:
			print(f"\n$$$$$$$$$$$$$$$$$\nediting each product FAILED due to :\n{e}")
		
		# ask to add any product to chosen order
		add_product_answer = input("\nyou wanna add any product to this order (y/n): ")
		add_product_answer = True if add_product_answer.lower() == 'y' else False
		if add_product_answer:
			print("enter new product name to add or type \"done\" to finish")
		while add_product_answer:
			
			adding_name = input('\t ** new product_name: ')
			if adding_name.lower() == 'done':
				break
			
			query = f'SELECT * FROM products WHERE productName=\"{adding_name}\"'
			mycursor.execute(query)
			adding_record = mycursor.fetchone()
			
			adding_code = adding_record[0]
			quantity_ordered = '1'
			price_each = adding_record[-2]
			orderLine_number = '1'

			try:
				query = f'''INSERT INTO orderdetails (orderNumber, productCode, quantityOrdered, priceEach, orderLineNumber)
VALUES (\"{chosen_order_number}\", \"{adding_code}\", \"{quantity_ordered}\", \"{price_each}\", \"{orderLine_number}\")'''
				mycursor.execute(query)
				self.mydb.commit()
				print(f'\t ** {mycursor.rowcount} product record added to orderDetails..')
			except IntegrityError as e:
				print(f'''****************
<< order failed >>
you probably entered product {product[1]} more than one time. try again. error:
{e}
''')

		# display final order:
		query = f'SELECT * FROM orderdetails WHERE orderNumber=\"{chosen_order_number}\"'
		mycursor.execute(query)
		final_orderdetails_records = mycursor.fetchall()
		for i, product in enumerate(final_orderdetails_records):
			product = list(product)
			product_code = product[1]
			query = f'SELECT * FROM products WHERE productCode=\"{product_code}\"'
			mycursor.execute(query)
			product_record = mycursor.fetchone()
			product_name = product_record[1]
			product[1] = product_name # replace product_name in each orderdetails record 
			final_orderdetails_records[i] = product # gather recoreds in one "final_orderdetails_records"
			
		print("\n[EDITED ORDER] :")
		print( tabulate(final_orderdetails_records, headers=[
			'orderNumber', 'productName', 'quantityOrdered', 'priceEach', 'orderLineNumber' ]) )



	def product(self): # input(choose between columns) output(True/False)
		mycursor = self.mydb.cursor()

		print("\n[1] which product you want to edit?")
		old_product_name = input('product name(old): ')

		print('\n[2] fill each line with new value for this product to update and\ntype nothing or hit enter to keep those you dont want to change:')
		product_columns = {
			"productName": input("new product name: ") ,
			"productScale": input("new product scale: ") , 
			"productVendor": input("new product vendor: ") ,
			"productDescription": input("new product description: ") ,
			"quantityInStock": input("new quantity in stock: "),
			"buyPrice": input("new buy price: "),
			"MSRP": input("new sell price(MSRP): ")
			}
		input_line_int = int(input('''	1- Classic Cars'
	2- Motorcycles
	3- Planes
	4- Ship
	5- Trains
	6- Trucks and Buses
	7- Vintage Cars
choose a new product line by its number: '''))
		product_lines = {
			1: 'Classic Cars',
			2: 'Motorcycles',
			3: 'Planes',
			4: 'Ships',
			5: 'Trains',
			6: 'Trucks and Buses',
			7: 'Vintage Cars',
		}
		product_columns['productLine'] = product_lines[input_line_int]

		query_command = 'UPDATE products '
		query_values = 'SET '
		query_condition = f' WHERE productName=\"{old_product_name}\"' 
		
		for database_column_name, new_value in product_columns.items():
			if len(new_value) == 0 or new_value.isspace(): 
				continue
			query_values += ( database_column_name + f'=\"{new_value}\",' )
		else: # if for didnt break and 'query_values' successfully made then remove last comma at end of string
			query_values = query_values[:-1]

		query = query_command + query_values + query_condition
		mycursor.execute(query)
		self.mydb.commit()

		if mycursor.rowcount >= 1:
			print(mycursor.rowcount, "Record updated successfully")
			return True