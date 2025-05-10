import sys
from commands import * # find, add, edit, delete
import keyboard

class display:
	def __init__(self):
		self.help = '''
\tthere is 4 operations known as commands and 4 targets known as items:
\t
\t[commands]	[description]
\t-----------------------------
\t-find\t\t\"finds/searches the database and display selected record(s). you can use item \'statistics\' with find to search more advanced!\"
\t-add\t\t\"create new record of the item\"
\t-edit\t\t\"update on desired record\"
\t-delete\t\t\"delete unwanted record\"
\t
\t[items]
\t-----------------------------
\t-customer
\t-employee
\t-order
\t-product
\t
\tyou can use the combination of \"command item\" to reach what you are looking for!
\tfor example type \"find product\" and hit enter. then you'll be prompt to what ever needed then..	
\tnotice that there is one extra item just for find command like \"find statistics\" for search more advance on data.
\tpress \"ctrl + C\" to exit
		'''


def get_user_command_and_item():
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
	print(screen.help)

	while True:

		command, item = get_user_command_and_item()
		if not(command and item): # enter key pressed
			continue

		if command == 'find' and item == 'statistics':
			statistics_executor = Find()
			records = statistics_executor.statistics()
			print(records)
			continue

		if command not in valid_commands or item not in valid_items:
			print('INVALID command or item! check the word dictation ')
			continue

		command_obj = command_objects[command]
		command_method = command_obj.get_method(item)
		records = command_method()
		print(records)

		print()




