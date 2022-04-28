class Product:
	def __init__(self, id, idCategory, name, price, amount):
		self.id = int(id)
		self.idCategory = int(idCategory)
		self.name = name
		self.price = float(price)
		self.amount = int(amount)