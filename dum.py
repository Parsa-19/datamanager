list_ = [
	(10136, '111111', '111111', '111111', 'Shipped', 'Customer is interested in buying more Ferrari models', 242),
	(10178, '222222', '222222', '222222', 'Shipped', 'Custom shipping instructions sent to warehouse', 242), 
	(10397, '333333', '333333', '333333', 'Shipped', None, 242)
]
for row_index, orderNumber in enumerate(list_):
	print(orderNumber[0])
