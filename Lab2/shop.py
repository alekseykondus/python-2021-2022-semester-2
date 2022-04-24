import MySQLdb
from pass__ import password
from productcategory import ProductCategory
from product import Product
from colorprint import PrintGREEN, PrintRED, PrintCYAN, PrintYELLOW

class Shop:
	def __init__(self):
		self.mProductCategories = dict()
		self.mProducts = dict()
		self.LoadDataOrNo = False

		#Connect to DB
		url = "localhost"
		databaseName = "shop"
		self.db = MySQLdb.connect(url, "root", password, databaseName)
		self.cursor = self.db.cursor()

	def Clean(self):
		self.mProductCategories = dict()
		self.mProducts = dict()

	def PrintData(self):

		try:
			sql = "SELECT idCategory, nameCategory FROM ProductCategories"
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			for row in results:
				idCategory = row[0]
				nameCategory = row[1]
				PrintYELLOW("Category id: " + str(idCategory) + ", name: " + nameCategory)

			sql = "SELECT * FROM Products"
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
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
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		for row in results:
			idCategory = row[0]
			nameCategory = row[1]
			productCategory = ProductCategory(idCategory, nameCategory)
			self.mProductCategories[idCategory] = productCategory

		sql = "SELECT * FROM Products"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
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
			self.cursor.execute(sql)
			self.db.commit()
			PrintGREEN("Категорія %s успішно додана!" % productCategory.name)
			return True
		except:
			PrintRED("ПОМИЛКА! Категорія %s не додана !" % productCategory.name)
			self.db.rollback()
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
			self.cursor.execute(sql)
			self.db.commit()
			PrintGREEN("Продукт %s успішно доданий!" % product.name)
			return True
		except:
			PrintRED("ПОМИЛКА! Продукт %s не доданий!" % product.name)
			self.db.rollback()
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

			sql = "UPDATE ProductCategories SET nameCategory = '" + categoryName + "'"+ \
				  " WHERE idCategory = " + str(categoryId)
			try:
				self.cursor.execute(sql)
				self.db.commit()
				PrintGREEN("Категорія id = %d успішно відредагована!" % categoryId)
				return True
			except:
				PrintRED("ПОМИЛКА! Категорія id = %d не відредагована!" % categoryId)
				self.db.rollback()
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
				self.cursor.execute(sql)
				self.db.commit()
				PrintGREEN("Продукт id = %d успішно відредагований!" % productId)
				return True
			except:
				PrintRED("ПОМИЛКА! Продукт id = %d не відредагований!" % productId)
				self.db.rollback()
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
				self.cursor.execute(sql)
				self.db.commit()
				PrintGREEN("Категорія %s успішно видалена!" % delname)
				return True
			except:
				PrintRED("ПОМИЛКА при видаленні категорії %s" % delname)
				self.db.rollback()
				return False


	def DeleteProduct(self, productId):
		delname = self.mProducts[productId].name

		if(self.SearchProduct(productId, False)):
			sql = "DELETE FROM Products WHERE idProduct = %d" % productId
			try:
				self.cursor.execute(sql)
				self.db.commit()
				del self.mProducts[productId]
				PrintGREEN("Продукт %s успішно видалена!" % delname)
				return True
			except:
				print("ПОМИЛКА при видаленні продукту %s" % delname)
				self.db.rollback()
				return False


	def SearchCategory(self, сategoryId, boolPrintOrNo):
		try:
			sql = "SELECT * FROM ProductCategories WHERE idCategory = %d" % сategoryId
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
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
			self.db.rollback()
			return False

	def SearchProduct(self, productId, boolPrintOrNo):
		try:
			sql = "SELECT * FROM Products WHERE idProduct = %d" % productId
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
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
			self.db.rollback()
			return False


	def PrintListOfCategories(self):
		sql = "SELECT idCategory, nameCategory FROM ProductCategories"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		if len(results) == 0:
			PrintRED("Список пуст")

		for row in results:
			idCategory = row[0]
			nameCategory = row[1]
			PrintYELLOW("Category id: " + str(idCategory) + ", name: " + nameCategory)
		return True

	def PrintListOfProductsInCategory(self, categoryId):

		if self.SearchCategory(categoryId, True):
			sql = "SELECT * FROM Products WHERE idCategory = %d" % categoryId
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
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
