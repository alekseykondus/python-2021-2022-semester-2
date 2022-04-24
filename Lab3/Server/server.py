import socket
from commands import Command
from productcategory import ProductCategory
from product import Product
from shop import Shop

if __name__ == '__main__':
	s = socket.socket()
	host = socket.gethostname()
	port = 12345
	s.bind((host, port))

	s.listen(5)
	print('Waiting for a client')
	conn, addr = s.accept()
	print('Got connection from ', addr)

	shop = Shop()
	while True:
		returnReply = ""
		receivedFromClient = conn.recv(1024).decode().split('|')
		command = int(receivedFromClient[0])
		#print("Получил команду: ", receivedFromClient)

		if command == Command.LoadData.value:
			returnReply = returnReply + shop.LoadData()
		elif command == Command.NewCategoryOrProduct.value:
			if receivedFromClient[1] == '1':
				categoryName = receivedFromClient[2]
				productCategory = ProductCategory(0, categoryName)
				returnReply = returnReply + shop.CreateCategory(productCategory)
			else:
				categoryId = int(receivedFromClient[2])
				searchCat = shop.SearchCategory(categoryId, False)
				if searchCat == "":
					retres = "True"
					conn.send(retres.encode())
					receivedNewProduct = conn.recv(1024).decode().split('|')
					categoryId = int(receivedNewProduct[2])
					productName = receivedNewProduct[3]
					productPrice = float(receivedNewProduct[4])
					productAmount = int(receivedNewProduct[5])
					newProduct = Product(0, categoryId, productName, productPrice, productAmount)
					returnReply = returnReply + shop.CreateProduct(newProduct)
				else:
					conn.send(searchCat.encode())
		elif command == Command.EditCategoryOrProduct.value:
			if receivedFromClient[1] == '1':
				categoryId = int(receivedFromClient[2])
				searchCat = shop.SearchCategory(categoryId, False)
				if searchCat == "":
					retres = "True"
					conn.send(retres.encode())
					receivedEditCategoryOrProduct = conn.recv(1024).decode().split('|')
					categoryName = receivedEditCategoryOrProduct[3]
					returnReply = returnReply + shop.EditCategory(categoryId, categoryName)
				else:
					conn.send(searchCat.encode())
			else:
				productId = int(receivedFromClient[2])
				searchProd = shop.SearchProduct(productId, False)
				if searchProd == "":
					retres = "True"
					conn.send(retres.encode())
					receivedEditCategoryOrProduct = conn.recv(1024).decode().split('|')
					commandEditProduct = int(receivedEditCategoryOrProduct[3])
					newCharacteristic = receivedEditCategoryOrProduct[4]
					returnReply = returnReply + shop.EditProduct(productId, commandEditProduct, newCharacteristic)
				else:
					conn.send(searchProd.encode())
		elif command == Command.DeleteCategoryOrProduct.value:
			if receivedFromClient[1] == '1':
				categoryId = int(receivedFromClient[2])
				returnReply = returnReply + shop.DeleteCategory(categoryId)
			else:
				productId = int(receivedFromClient[2])
				returnReply = returnReply + shop.DeleteProduct(productId)
		elif command == Command.SearchCategoryOrProduct.value:
			if receivedFromClient[1] == '1':
				categoryId = int(receivedFromClient[2])
				returnReply = returnReply + str(shop.SearchCategory(categoryId, True))
			else:
				productId = int(receivedFromClient[2])
				returnReply = returnReply + shop.SearchProduct(productId, True)
		elif command == Command.ListOfCategoriesOrProducts.value:
			if receivedFromClient[1] == '1':
				returnReply = returnReply + shop.PrintListOfCategories()
			else:
				categoryId = int(receivedFromClient[2])
				returnReply = returnReply + shop.PrintListOfProductsInCategory(categoryId)
		elif command == Command.Exit.value:
			exit()
		else:
			returnReply = returnReply + "Unknown command"
		#print(returnReply)
		conn.send(returnReply.encode())