import command_find, command_add, command_edit, command_delete
import sys
import keyboard
import customizedSQLConnector

class display:
	def __init__(self):
		self.help = '''
	there is 4 operations known as commands and 4 targets known as items:
	
	[commands]	[description]
	-----------------------------
	-find\t\t\"finds/searches the database and display selected record(s). you can use item \'statistics\' with find to search more advanced!\"
	-add\t\t\"create new record of the item\"
	-edit\t\t\"update on desired record\"
	-delete\t\t\"delete unwanted record\"
	
	[items]
	-----------------------------
	-customer
	-employee
	-order
	-product
	
	you can use the combination of \"command item\" to reach what you are looking for!
	for example type \"find product\" and hit enter. then you'll be prompt to what ever needed then..	
	notice that there is one extra item just for find command like \"find statistics\" for search more advance on data.
	press \"Ctrl + C\" to exit
		'''


def get_user_command_and_item():
	ask = input('/classicmodelsDB> ')
	command, item = ask.split()
	return command.lower(), item.lower()


if __name__ == '__main__':

	valid_commands = ['find', 'add', 'edit', 'delete']
	valid_items = ['customer', 'employee', 'order', 'product']

	command_objects = {
		'find': command_find.Find(),
		'add': command_add.Add(),
		'edit': command_edit.Edit(),
		'delete': command_delete.Delete() 
	}

	screen = display()
	print(screen.help)

	try:
		while True:

			command, item = get_user_command_and_item()

			if command == 'find' and item == 'statistics': # special item for command
				statistics_executor = command_find.Find()
				records_result = statistics_executor.statistics()
				print(records_result)
				continue

			elif command not in valid_commands or item not in valid_items:
				print('INVALID command or item! check the word dictation!')
				continue

			command_obj = command_objects[command]
			item_method = command_obj.get_method(item) # returns the target method(customer, employee, order, product) according to input item
			records_result = item_method()
			print(records_result)

			print()

	except KeyboardInterrupt:
		print("\n\nCtrl-C pressed!")
		sys.exit(0)



