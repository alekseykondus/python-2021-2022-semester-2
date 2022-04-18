
import colorama
from colorama import init, Fore
import enum
import os.path
from lxml import etree as ET
import sys

def PrintGREEN(message):
	print(Fore.GREEN + message)

def PrintRED(message):
	print(Fore.RED + message)

def PrintCYAN(message):
	print(Fore.CYAN + message)

def PrintYELLOW(message):
	print(Fore.YELLOW + message)


class ProductCategory:
	def __init__(self, id, name):
		self.id = id
		self.products = set()
		self.name = name

class Product:
	def __init__(self, id, name, price, amount):
		self.id = id
		self.name = name
		self.price = price
		self.amount = amount

class Shop:
	def __init__(self):
		self.mProductCategories = dict()
		self.mProducts = dict()

	def Clean(self):
		self.mProductCategories = dict()
		self.mProducts = dict()

	def PrintData(self):
		for сategoryId in self.mProductCategories:
			PrintYELLOW("Parse category. Id: " + str(self.mProductCategories[сategoryId].id) + ", name: " + self.mProductCategories[сategoryId].name)
			for productIterator in self.mProductCategories[сategoryId].products:
				PrintYELLOW("	Product id: " + str(productIterator.id) + ", name: " + productIterator.name + ", price: " +
							str(productIterator.price) + ", amount: " + str(productIterator.amount))

	def LoadData(self,  file):
		#self.SaveToFile()
		self.Clean()
		if not os.path.isfile(file):
			PrintRED("incorrect path")
			return
		f = open(file, "r")
		try:
			xmlDoc = ET.fromstring(f.read())
			dtd = ET.DTD(open(dtdPath))
			#if not dtd.validate(xmlDoc):
			#	PrintRED("Dtd validation not passed")
			#	return
		except:
			PrintRED("Error while parsing. Invalid document")
			return

		for xmlCategory in xmlDoc.findall("ProductCategories/ProductCategory"):
			categoryId = int(xmlCategory.get('categoryId'))
			categoryName = xmlCategory.get('categoryName')
			productCategory = ProductCategory(categoryId, categoryName)
			for xmlProduct in xmlCategory.findall("Products/Product"):
				productId = int(xmlProduct.get('id'))
				productName = xmlProduct.get('name')
				productPrice = float(xmlProduct.get('price'))
				productAmount = int(xmlProduct.get('amount'))
				product = Product(productId, productName, productPrice, productAmount)
				productCategory.products.add(product)
				self.mProducts[productId] = product

			self.mProductCategories[categoryId] = productCategory

		self.PrintData()
		return 0

	def SaveToFile(self, file):
		root = ET.Element('Shop')
		tree = ET.ElementTree(root)
		productCategories = ET.SubElement(root, "ProductCategories")
		for key, value in self.mProductCategories.items():
			productCategory = ET.SubElement(productCategories, "ProductCategory")
			productCategory.set("categoryId", str(key))
			productCategory.set("categoryName", str(value.name))
			products = ET.SubElement(productCategory, "Products")
			for productIter in value.products:
				product = ET.SubElement(products, "Product")
				product.set("id", str(productIter.id))
				product.set("name", str(productIter.name))
				product.set("price", str(productIter.price))
				product.set("amount", str(productIter.amount))

		with open(file, 'wb') as f:
			tree.write(f, pretty_print=True, encoding='utf-8')
		PrintGREEN("save_to_file")
		return 0

	def CreateCategory(self, productCategory):
		if len(self.mProductCategories) == 0:
			key = 0
		else:
			key = max(self.mProductCategories.keys()) + 1
		productCategory.id = key
		self.mProductCategories[key] = productCategory
		return key

	def CreateProduct(self, categoryId, product):
		if len(self.mProducts) == 0:
			key = 0
		else:
			key = max(self.mProducts.keys()) + 1
		product.id = key
		self.mProducts[key] = product
		self.mProductCategories[categoryId].products.add(product)
		PrintGREEN("new Product added")
		return key

	def EditCategory(self, categoryId):
		if not categoryId in self.mProductCategories:
			PrintRED("Incorrect id")
			return
		productCategory_copy = self.mProductCategories[categoryId]
		PrintYELLOW("Введите новое имя категории (categoryName): ")
		categoryName = input()
		productCategory_copy.name = categoryName
		self.mProductCategories[categoryId] = productCategory_copy
		return categoryId

	def EditProduct(self, categoryId, productId):
		if not categoryId in self.mProductCategories or not productId in self.mProducts:
			PrintRED("Incorrect id")
			return
		product_copy = self.mProducts[productId]
		PrintYELLOW("Чтобы бы вы хотели изменить? \n" +
					"1 - название продукта \n" +
					"2 - цену продукта \n" +
					"3 - количество продукта на складе")
		command = int(input())
		if command == 1:
			PrintYELLOW("Введите новое имя продукта: ")
			productName = input()
			product_copy.name = productName
		elif command == 2:
			PrintYELLOW("Введите новую цену продукта: ")
			productPrice = input()
			product_copy.price = productPrice
		elif command == 3:
			PrintYELLOW("Введите новое количество продукта на складе: ");
			productAmount = input()
			product_copy.amount = productAmount
		else :
			PrintRED("Unknown command")
			return
		self.mProducts[productId] = product_copy
		for product in self.mProductCategories[categoryId].products:
			if product.id == product_copy.id:
				product = product_copy
		return productId

	def DeleteCategory(self, сategoryId):
		if not сategoryId in self.mProductCategories:
			PrintRED("Incorrect id")
			return
		for product in self.mProductCategories[сategoryId].products:
			del self.mProducts[product.id]
		del self.mProductCategories[сategoryId]

		print("Delete_category")
		return 0

	def DeleteProduct(self, сategoryId, productId):
		if not categoryId in self.mProductCategories or not productId in self.mProducts:
			PrintRED("Incorrect id")
			return
		del self.mProducts[productId]
		#self.mProductCategories[сategoryId].products.remove(productId)
		print("Delete_product")
		return 0

	def SearchCategory(self, сategoryId):
		if not сategoryId in self.mProductCategories:
			PrintRED("Incorrect id")
			return
		PrintYELLOW("	Category Id: " + str(self.mProductCategories[сategoryId].id) + ", name: " + self.mProductCategories[
				сategoryId].name)
		return 0

	def SearchProduct(self, productId):
		if not productId in self.mProducts:
			PrintRED("Incorrect id")
			return
		product = self.mProducts[productId]
		PrintYELLOW("	Product id: " + str(product.id) + ", name: " + product.name + ", price: " +
					str(product.price) + ", amount: " + str(product.amount))
		return 0

	def PrintListOfCategories(self):
		for сategoryId in self.mProductCategories:
			PrintYELLOW("Category Id: " + str(self.mProductCategories[сategoryId].id) + ", name: " + self.mProductCategories[сategoryId].name)
		return 0

	def PrintListOfProductsInCategory(self, categoryId):
		if not categoryId in self.mProductCategories:
			PrintRED("Incorrect id")
			return
		PrintYELLOW("Список продуктов, который принадлежит " + self.mProductCategories[categoryId].name + ": ")
		for product in self.mProductCategories[categoryId].products:
			PrintYELLOW("	Product id: " + str(product.id) + ", name: " + product.name + ", price: " +
						str(product.price) + ", amount: " + str(product.amount))
		return 0


class Command(enum.Enum):
	LoadData = 1
	SaveToFile = 2
	NewCategoryOrProduct = 3
	EditCategoryOrProduct = 4
	DeleteCategoryOrProduct = 5
	SearchCategoryOrProduct = 6
	ListOfCategoriesOrProducts = 7
	Exit = 8

def PrintCommands():
	PrintCYAN("1 - завантаження даних про продукты та категории продуктов \n" +
			  "2 - збереження даних про категорії і продукти в файл \n" +
			  "3 - додавання нової категорії або продукту \n" +
			  "4 - зміна параметрів (редагування) категорії або продукту \n" +
			  "5 - видалення категорії або продукту \n" +
			  "6 - пошук категорії або продукту \n" +
			  "7 - вивод списку категорій або продуктів за заданою категорією \n" +
			  "8 - Вихід")

def CategoryOrProduct () :
	PrintGREEN("1 - Категория, 2 - Продукт. Введите команду:")
	return int(input()) == 1
def parseOptions(args):
	options = dict()
	for arg in args:
		if arg.startswith('-'):
			options[arg[1]] = arg[2:]
	return options



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	opts = parseOptions(sys.argv)
	dtdPath = opts.get("s", "schema.dtd")
	filePath = opts.get("s", "data.xml")

	shop = Shop()

	while True:
		PrintCommands()
		PrintGREEN("Введите команду:")
		command = int(input())

		if command == Command.LoadData.value:
			shop.LoadData(filePath)
		elif command == Command.SaveToFile.value:
			shop.SaveToFile(filePath)
		elif command == Command.NewCategoryOrProduct.value:
			if CategoryOrProduct() :
				PrintYELLOW("Введите название категории: ")
				categoryName = input()
				productCategory = ProductCategory(0, categoryName)
				shop.CreateCategory(productCategory)
			else:
				PrintYELLOW("Введите id категории, в которую нужно добавить продукт: ")
				categoryId = int(input())
				PrintYELLOW("Введите название продукта: ")
				productName = input()
				PrintYELLOW("Введите цену продукта " + productName + ": ")
				productPrice = float(input())
				PrintYELLOW("Введите количество продукта " + productName + ": ")
				productAmount = int(input())

				newProduct = Product(0, productName, productPrice, productAmount)
				shop.CreateProduct(categoryId, newProduct)
		elif command == Command.EditCategoryOrProduct.value:
			if CategoryOrProduct() :
				PrintYELLOW("Введите id категории, которую нужно изменить: ")
				categoryId = int(input())
				shop.EditCategory(categoryId)
			else:
				PrintYELLOW("Введите id категории, в которой находится нужный продукт: ")
				categoryId = int(input())
				PrintYELLOW("Введите id продукта, который нужно изменить: ")
				productId = int(input())
				shop.EditProduct(categoryId, productId)
		elif command == Command.DeleteCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно удалить: ")
				categoryId = int(input())
				shop.DeleteCategory(categoryId)
			else:
				PrintYELLOW("Введите id категории, в которой нужно удалить продукт: ")
				categoryId = int(input())
				PrintYELLOW("Введите id продукта, который нужно удалить: ")
				productId = int(input())
				shop.DeleteProduct(categoryId, productId)
		elif command == Command.SearchCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно найти: ")
				categoryId = int(input())
				shop.SearchCategory(categoryId)
			else:
				PrintYELLOW("Введите id продукта, который нужно найти: ")
				productId = int(input())
				shop.SearchProduct(productId)
		elif command == Command.ListOfCategoriesOrProducts.value:
			if CategoryOrProduct():
				shop.PrintListOfCategories()
			else:
				PrintYELLOW("Введите id категории: ")
				categoryId = int(input())
				shop.PrintListOfProductsInCategory(categoryId)
		elif command == Command.Exit.value:
			exit()
		else :
			PrintRED("Unknown command")