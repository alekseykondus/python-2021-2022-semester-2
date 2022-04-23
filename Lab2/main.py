
from colorama import init, Fore
import enum
import MySQLdb
from pass__ import password

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
		#self.products = set()
		self.name = name

class Product:
	def __init__(self, id, idCategory, name, price, amount):
		self.id = int(id)
		self.idCategory = int(idCategory)
		self.name = name
		self.price = float(price)
		self.amount = int(amount)

class Shop:
	def __init__(self):
		self.mProductCategories = dict()
		self.mProducts = dict()
		self.LoadDataOrNo = False

	def Clean(self):
		self.mProductCategories = dict()
		self.mProducts = dict()

	def PrintData(self):

		try:
			sql = "SELECT idCategory, nameCategory FROM ProductCategories"
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				idCategory = row[0]
				nameCategory = row[1]
				PrintYELLOW("Category id: " + str(idCategory) + ", name: " + nameCategory)

			sql = "SELECT * FROM Products"
			cursor.execute(sql)
			results = cursor.fetchall()
			for row in results:
				idProduct = row[0]
				idCategory = row[1]
				nameProduct = row[2]
				priceProduct = row[3]
				amountProduct = row[4]
				PrintYELLOW("Product id: " + str(idProduct) + ", Category id: " + str(idCategory) + ", name: " + nameProduct +
							", price: " + str(priceProduct) + ", amount: " + str(amountProduct))

		except:
			print("ПОМИЛКА при отриманні списку ")


	def LoadData(self):
		self.Clean()

		sql = "SELECT * FROM ProductCategories"
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			idCategory = row[0]
			nameCategory = row[1]
			productCategory = ProductCategory(idCategory, nameCategory)
			self.mProductCategories[idCategory] = productCategory

		sql = "SELECT * FROM Products"
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
			idProduct = row[0]
			idCategory = row[1]
			nameProduct = row[2]
			priceProduct = row[3]
			amountProduct = row[4]
			product = Product(idProduct, idCategory, nameProduct, priceProduct, amountProduct)
			self.mProducts[idProduct] = product

		self.LoadDataOrNo = True
		self.PrintData()
		return 0


	def CreateCategory(self, productCategory):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if len(self.mProductCategories) == 0:
			key = 0
		else:
			key = max(self.mProductCategories.keys()) + 1
		productCategory.id = key
		self.mProductCategories[key] = productCategory

		sql = "INSERT INTO ProductCategories (idCategory, nameCategory) VALUES (%d, '%s')" % (productCategory.id, productCategory.name)
		try:
			cursor.execute(sql)
			db.commit()
			PrintGREEN("Категорія %s успішно додана!" % productCategory.name)
			return True
		except:
			PrintRED("ПОМИЛКА! Категорія %s не додана !" % productCategory.name)
			db.rollback()
			return False


	def CreateProduct(self, product):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if len(self.mProducts) == 0:
			key = 0
		else:
			key = max(self.mProducts.keys()) + 1
		product.id = key
		self.mProducts[key] = product

		sql = "INSERT INTO Products (idProduct, idCategory, nameProduct, priceProduct, amountProduct) VALUES (%d, %d, '%s', %f, %d)" % (
		product.id, product.idCategory, product.name, product.price, product.amount)
		try:
			cursor.execute(sql)
			db.commit()
			PrintGREEN("Продукт %s успішно доданий!" % product.name)
			return True
		except:
			PrintRED("ПОМИЛКА! Продукт %s не доданий!" % product.name)
			db.rollback()
			return False

	def EditCategory(self, categoryId):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if(self.SearchCategory(categoryId, False)):
			productCategory_copy = self.mProductCategories[categoryId]
			PrintYELLOW("Введите новое имя категории (categoryName): ")
			categoryName = input()
			productCategory_copy.name = categoryName
			self.mProductCategories[categoryId] = productCategory_copy

			sql = "UPDATE ProductCategories SET nameCategory = '" + categoryName + "'"
			try:
				cursor.execute(sql)
				db.commit()
				PrintGREEN("Категорія id = %d успішно відредагована!" % categoryId)
				return True
			except:
				PrintRED("ПОМИЛКА! Категорія id = %d не відредагована!" % categoryId)
				db.rollback()
				return False


	def EditProduct(self, productId):
		if self.LoadDataOrNo == False:
			self.LoadData()
		if(self.SearchProduct(productId, False)):
			product_copy = self.mProducts[productId]
			PrintYELLOW("Чтобы бы вы хотели изменить? \n" +
						"1 - название продукта \n" +
						"2 - цену продукта \n" +
						"3 - количество продукта на складе")

			sql = "UPDATE Products SET "
			command = int(input())
			if command == 1:
				PrintYELLOW("Введите новое имя продукта: ")
				productName = input()
				product_copy.name = productName
				sql = sql + "nameProduct = '" + productName + "'"
			elif command == 2:
				PrintYELLOW("Введите новую цену продукта: ")
				productPrice = input()
				product_copy.price = productPrice
				sql = sql + "priceProduct = " + str(productPrice)
			elif command == 3:
				PrintYELLOW("Введите новое количество продукта на складе: ");
				productAmount = input()
				product_copy.amount = productAmount
				sql = sql + "amountProduct = " + str(productAmount)
			else :
				PrintRED("Unknown command")
				return
			sql = sql + " WHERE idProduct = " + str(productId)
			self.mProducts[productId] = product_copy
			try:
				cursor.execute(sql)
				db.commit()
				PrintGREEN("Продукт id = %d успішно відредагований!" % productId)
				return True
			except:
				PrintRED("ПОМИЛКА! Продукт id = %d не відредагований!" % productId)
				db.rollback()
				return False


	def DeleteCategory(self, сategoryId):
		delname = self.mProductCategories[сategoryId].name
		productsIdSet = set()
		for productId in self.mProducts:
			if self.mProducts[productId].idCategory == сategoryId:
				productsIdSet.add(productId)

		for productId in productsIdSet:
			self.DeleteProduct(self.mProducts[productId].id)
		del self.mProductCategories[сategoryId]


		if (self.SearchCategory(сategoryId, False)):
			sql = "DELETE FROM ProductCategories WHERE idCategory = %d" % сategoryId
			try:
				cursor.execute(sql)
				db.commit()
				PrintGREEN("Категорія %s успішно видалена!" % delname)
				return True
			except:
				PrintRED("ПОМИЛКА при видаленні категорії %s" % delname)
				db.rollback()
				return False


	def DeleteProduct(self, productId):
		delname = self.mProducts[productId].name

		if(self.SearchProduct(productId, False)):
			sql = "DELETE FROM Products WHERE idProduct = %d" % productId
			try:
				cursor.execute(sql)
				db.commit()
				del self.mProducts[productId]
				PrintGREEN("Продукт %s успішно видалена!" % delname)
				return True
			except:
				print("ПОМИЛКА при видаленні продукту %s" % delname)
				db.rollback()
				return False


	def SearchCategory(self, сategoryId, boolPrintOrNo):
		try:
			sql = "SELECT * FROM ProductCategories WHERE idCategory = %d" % сategoryId
			cursor.execute(sql)
			results = cursor.fetchall()
			if len(results) == 0:
				PrintRED("Немає категорії з таким id = " + str(сategoryId))
			for row in results:
				idCategory = row[0]
				nameCategory = row[1]
				if boolPrintOrNo:
					PrintYELLOW("Category id: " + str(idCategory) + ", name: " + nameCategory)
				return True
		except:
			print("ПОМИЛКА при пошуку категорії %d" % сategoryId)
			db.rollback()
			return False

	def SearchProduct(self, productId, boolPrintOrNo):
		try:
			sql = "SELECT * FROM Products WHERE idProduct = %d" % productId
			cursor.execute(sql)
			results = cursor.fetchall()
			if len(results) == 0:
				PrintRED("Немає продукту з таким id = " + str(productId))
			for row in results:
				idProduct = row[0]
				idCategory = row[1]
				nameProduct = row[2]
				priceProduct = row[3]
				amountProduct = row[4]
				if boolPrintOrNo:
					PrintYELLOW("Product id: " + str(idProduct) + ", Category id: " + str(idCategory) + ", name: " + nameProduct +
							", price: " + str(priceProduct) + ", amount: " + str(amountProduct))
				return True
		except:
			print("ПОМИЛКА при пошуку продукту %d" % productId)
			db.rollback()
			return False


	def PrintListOfCategories(self):
		sql = "SELECT idCategory, nameCategory FROM ProductCategories"
		cursor.execute(sql)
		results = cursor.fetchall()
		if len(results) == 0:
			PrintRED("Список пуст")

		for row in results:
			idCategory = row[0]
			nameCategory = row[1]
			PrintYELLOW("Category id: " + str(idCategory) + ", name: " + nameCategory)
		return True

		#for сategoryId in self.mProductCategories:
		#	PrintYELLOW("Category Id: " + str(self.mProductCategories[сategoryId].id) + ", name: " + self.mProductCategories[сategoryId].name)
		#return 0

	def PrintListOfProductsInCategory(self, categoryId):

		if self.SearchCategory(categoryId, True):
			sql = "SELECT * FROM Products WHERE idCategory = %d" % categoryId
			cursor.execute(sql)
			results = cursor.fetchall()
			if len(results) == 0:
				PrintRED("Список пуст")
			for row in results:
				idProduct = row[0]
				idCategory = row[1]
				nameProduct = row[2]
				priceProduct = row[3]
				amountProduct = row[4]
				PrintYELLOW("	Product id: " + str(idProduct) + ", Category id: " + str(idCategory) + ", name: " + nameProduct +
							", price: " + str(priceProduct) + ", amount: " + str(amountProduct))
		return True


class Command(enum.Enum):
	LoadData = 1
	NewCategoryOrProduct = 2
	EditCategoryOrProduct = 3
	DeleteCategoryOrProduct = 4
	SearchCategoryOrProduct = 5
	ListOfCategoriesOrProducts = 6
	Exit = 7

def PrintCommands():
	PrintCYAN("1 - завантаження та вивід усіх продуктів та категорій продуктів \n" +
			  "2 - додавання нової категорії або продукту \n" +
			  "3 - зміна параметрів (редагування) категорії або продукту \n" +
			  "4 - видалення категорії або продукту \n" +
			  "5 - пошук категорії або продукту \n" +
			  "6 - вивод списку категорій або продуктів за заданою категорією \n" +
			  "7 - вихід")

def CategoryOrProduct () :
	PrintGREEN("1 - Категория, 2 - Продукт. Введите команду:")
	return int(input()) == 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

	url = "localhost"
	databaseName = "shop"
	db = MySQLdb.connect(url, "root", password, databaseName)
	cursor = db.cursor()

	shop = Shop()

	while True:
		PrintCommands()
		PrintGREEN("Введите команду:")
		command = int(input())

		if command == Command.LoadData.value:
			shop.LoadData()
		elif command == Command.NewCategoryOrProduct.value:
			if CategoryOrProduct() :
				PrintYELLOW("Введите название категории: ")
				categoryName = input()
				productCategory = ProductCategory(0, categoryName)
				shop.CreateCategory(productCategory)
			else:
				PrintYELLOW("Введите id категории, в которую нужно добавить продукт: ")
				categoryId = int(input())
				if shop.SearchCategory(categoryId, False):
					PrintYELLOW("Введите название продукта: ")
					productName = input()
					PrintYELLOW("Введите цену продукта " + productName + ": ")
					productPrice = float(input())
					PrintYELLOW("Введите количество продукта " + productName + ": ")
					productAmount = int(input())
					newProduct = Product(0, categoryId, productName, productPrice, productAmount)
					shop.CreateProduct(newProduct)
		elif command == Command.EditCategoryOrProduct.value:
			if CategoryOrProduct() :
				PrintYELLOW("Введите id категории, которую нужно изменить: ")
				categoryId = int(input())
				shop.EditCategory(categoryId)
			else:
				PrintYELLOW("Введите id продукта, который нужно изменить: ")
				productId = int(input())
				shop.EditProduct(productId)
		elif command == Command.DeleteCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно удалить: ")
				categoryId = int(input())
				shop.DeleteCategory(categoryId)
			else:
				PrintYELLOW("Введите id продукта, который нужно удалить: ")
				productId = int(input())
				shop.DeleteProduct(productId)
		elif command == Command.SearchCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно найти: ")
				categoryId = int(input())
				shop.SearchCategory(categoryId, True)
			else:
				PrintYELLOW("Введите id продукта, который нужно найти: ")
				productId = int(input())
				shop.SearchProduct(productId, True)
		elif command == Command.ListOfCategoriesOrProducts.value:
			if CategoryOrProduct():
				shop.PrintListOfCategories()
			else:
				PrintYELLOW("Введите id категории: ")
				categoryId = int(input())
				shop.PrintListOfProductsInCategory(categoryId)
		elif command == Command.Exit.value:
			exit()
		else:
			PrintRED("Unknown command")