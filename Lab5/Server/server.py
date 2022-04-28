import socket
from commands import Command
from productcategory import ProductCategory
from product import Product
from shop import Shop
import pika, time


def RunServer (receivedFromClient, shop):
	returnReply = ""
	command = int(receivedFromClient[0])
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
					categoryId = int(receivedFromClient[2])
					productName = receivedFromClient[3]
					productPrice = float(receivedFromClient[4])
					productAmount = int(receivedFromClient[5])
					newProduct = Product(0, categoryId, productName, productPrice, productAmount)
					returnReply = returnReply + shop.CreateProduct(newProduct)
				else:
					returnReply = searchCat
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
		returnReply = "7"
	else:
		returnReply = returnReply + "Unknown command"
	return returnReply


def callback(ch, method, properties, body):
	print('Receive query', body.decode())
	shop = Shop()
	response = RunServer(body.decode().split('|'), shop)
	channel.basic_publish(exchange='', routing_key='client_queue', body=response)
	if response == "7":
		exit()

if __name__ == '__main__':
	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='server_queue')
	channel.queue_declare(queue='client_queue')
	print('Server started...')

	try:
		#time.sleep(15)
		channel.basic_consume(queue='server_queue', on_message_callback=callback, auto_ack=True)
		channel.start_consuming()
	except KeyboardInterrupt:
		print('Server stopped')
		connection.close()
	'''
	while True:
		#print("Получил команду: ", receivedFromClient)

		#print(returnReply)
	'''
