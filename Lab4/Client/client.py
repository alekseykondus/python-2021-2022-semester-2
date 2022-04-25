import Pyro4
from colorprint import PrintGREEN, PrintRED, PrintCYAN, PrintYELLOW
from commands import Command, PrintCommands, CategoryOrProduct

def PrintResult (result) :
	if result[0] == 'G':
		PrintGREEN(result[1])
	elif result[0] == 'Y':
		PrintYELLOW(result[1])
	elif result[0] == 'R':
		PrintRED(result[1])
	elif result[0] == 'C':
		PrintCYAN(result[1])
	else:
		print("Помилка під час передачі даних")


if __name__ == '__main__':

	ns = Pyro4.locateNS()
	uri = ns.lookup('shop')
	shop = Pyro4.Proxy(uri)

	while True:
		doWeNeedCatch = True
		PrintCommands()
		PrintGREEN("Введите команду:")
		command = int(input())
		query = str(command)

		if command == Command.LoadData.value:
			result = shop.LoadData()

		elif command == Command.NewCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите название категории: ")
				categoryName = input()
				result = shop.CreateCategory(categoryName)
			else:
				PrintYELLOW("Введите id категории, в которую нужно добавить продукт: ")
				categoryId = int(input())
				result = shop.SearchCategory(categoryId, False)
				if result == "":
					PrintYELLOW("Введите название продукта: ")
					productName = input()
					PrintYELLOW("Введите цену продукта " + productName + ": ")
					productPrice = float(input())
					PrintYELLOW("Введите количество продукта " + productName + ": ")
					productAmount = int(input())
					result = shop.CreateProduct(categoryId, productName, productPrice, productAmount)
		elif command == Command.EditCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории, которую нужно изменить: ")
				сategoryId = int(input())
				result = shop.SearchCategory(сategoryId, False)
				if result == "":
					PrintYELLOW("Введите новое имя категории (categoryName): ")
					newCategoryName = input()
					result = shop.EditCategory(сategoryId, newCategoryName)
			else:
				PrintYELLOW("Введите id продукта, который нужно изменить: ")
				productId = int(input())
				result = shop.SearchProduct(productId, False)
				if result == "":
					PrintYELLOW("Чтобы бы вы хотели изменить? \n" +
								"1 - название продукта \n" +
								"2 - цену продукта \n" +
								"3 - количество продукта на складе")
					commandEditProduct = int(input())
					if commandEditProduct == 1:
						PrintYELLOW("Введите новое имя продукта: ")
						productName = input()
						result 	= shop.EditProduct(productId, commandEditProduct, productName)
					elif commandEditProduct == 2:
						PrintYELLOW("Введите новую цену продукта: ")
						productPrice = input()
						result 	= shop.EditProduct(productId, commandEditProduct, productPrice)
					elif commandEditProduct == 3:
						PrintYELLOW("Введите новое количество продукта на складе: ")
						productAmount = input()
						result 	= shop.EditProduct(productId, commandEditProduct, productAmount)
					else:
						PrintRED("Unknown command")
		elif command == Command.DeleteCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно удалить: ")
				сategoryId = int(input())
				result = shop.DeleteCategory(сategoryId)
			else:
				PrintYELLOW("Введите id продукта, который нужно удалить: ")
				productId = int(input())
				result = shop.DeleteProduct(productId)
		elif command == Command.SearchCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно найти: ")
				categoryId = int(input())
				result = shop.SearchCategory(categoryId, True)
			else:
				PrintYELLOW("Введите id продукта, который нужно найти: ")
				productId = int(input())
				result = shop.SearchProduct(productId, True)
		elif command == Command.ListOfCategoriesOrProducts.value:
			if CategoryOrProduct():
				result = shop.PrintListOfCategories()
			else:
				PrintYELLOW("Введите id категории: ")
				categoryId = int(input())
				result = shop.PrintListOfProductsInCategory(categoryId)
		elif command == Command.Exit.value:
			exit()

		PrintResult(result.split('|'))