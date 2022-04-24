from colorprint import PrintGREEN, PrintRED, PrintCYAN, PrintYELLOW
from productcategory import ProductCategory
from product import Product
from commands import Command, PrintCommands, CategoryOrProduct
from shop import Shop

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

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