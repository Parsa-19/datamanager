from tabulate import tabulate
import itemTools
import customizedSQLConnector as classicDB

class Find(itemTools.itemFinder): # SELECT
	
	def __init__(self):
		super().__init__()
		self.mydb = classicDB.connect_sql()
	
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
		statistics_result = '\nall sells in this date:\n------------------------'
		sell_date_record = '{record}'
		mycursor = self.mydb.cursor()
		input_date = input("\ntype the date you want to get statistics from e.g. \'2004-04-14\': ")
		
		query = f"SELECT * FROM payments WHERE paymentDate=\"{input_date}\"" 
		mycursor.execute(query)
		all_records = mycursor.fetchall()
		for index, record in enumerate(all_records):
			statistics_result += ('\n' + f'{index+1}\tdate : {record[2]}\tamount : {record[3]} (price)')

		statistics_result += '\n\nmost expensive sell:\n---------------------\n'
		query = f"SELECT MAX(amount) FROM payments WHERE paymentDate=\"{input_date}\""
		mycursor.execute(query)
		highest_price = mycursor.fetchall()
		statistics_result += ( f'amount : {str(highest_price[0][0])} (price)\n' )

		"most popular product bought this day: {}"

		return statistics_result
