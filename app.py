import sys
from commands import * # find, add, edit, delete

class display:
	def __init__(self):
		print('''
\tthere is 4 operations known as commands and 4 targets known as items:
\t
\t[commands]	[description]
\t-----------------------------
\t-find			\"finds/searches the database display selected record(s)\"
\t-add			\"create new record of the item\"
\t-edit			\"update on desired record\"
\t-delete			\"delete unwanted record\"
\t
\t[items]
\t-----------------------------
\t-customer
\t-employee
\t-order
\t-product
\t
\tyou can use the combination of \"command item\" to reach what you are looking for!
\te.g. \"find product\" and hit enter. then you'll be prompt to type what ever needed..	
\tpress \"ctrl + C\" to exit
		''')


def get_command_and_item():
	ask = input('/app> ')
	command, item = ask.split()
	return command.lower(), item.lower()


if __name__ == '__main__':

	valid_commands = ['find', 'add', 'edit', 'delete']
	valid_items = ['customer', 'employee', 'order', 'product']
	command_objects = {
		'find': Find(),
		'add': Add(),
		'edit': Edit(),
		'delete': Delete() 
	}

	screen = display()

	while True:

		command, item = get_command_and_item()

		if command not in valid_commands or item not in valid_items:
			print('INVALID command or item check the dictaion ')
			continue

		command_obj = command_objects[command]
		command_method = command_obj.get_method(item)
		record = command_method()
		print(len(record))

		print()




