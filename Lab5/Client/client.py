import socket
from colorprint import PrintGREEN, PrintRED, PrintCYAN, PrintYELLOW
from commands import Command, PrintCommands, CategoryOrProduct
import pika
import threading


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


def startConsumer():
	def callback(ch, method, properties, body):
		if body.decode() == "7":
			exit()
		result = body.decode().split('|')
		PrintResult(result)

	channel.basic_consume(queue='client_queue', on_message_callback=callback, auto_ack=True)
	channel.start_consuming()

if __name__ == '__main__':

	connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
	channel = connection.channel()
	channel.queue_declare(queue='client_queue')
	channel.queue_declare(queue='server_queue')


	PrintGREEN("1 - получить информацию с сервера \n" +
			   "2 - отправить запросы на сервер")
	PrintGREEN("Введите команду:")
	command = int(input())
	if(command == 1):
		startConsumer()
	elif command == 2:
		while True:
			doWeNeedCatch = True
			PrintCommands()
			PrintGREEN("Введите команду:")
			command = int(input())
			query = str(command)

			if command == Command.LoadData.value:
				channel.basic_publish(exchange='', routing_key='server_queue', body=query)
			elif command == Command.NewCategoryOrProduct.value:
				if CategoryOrProduct():
					PrintYELLOW("Введите название категории: ")
					categoryName = input()
					query = query + "|1|" + categoryName
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
				else:
					PrintYELLOW("Введите id категории, в которую нужно добавить продукт: ")
					categoryId = int(input())
					query = query + "|2|" + str(categoryId)

					PrintYELLOW("Введите название продукта: ")
					productName = input()
					PrintYELLOW("Введите цену продукта " + productName + ": ")
					productPrice = float(input())
					PrintYELLOW("Введите количество продукта " + productName + ": ")
					productAmount = int(input())
					query = query + "|" + productName + "|" + str(productPrice) + "|" + str(productAmount)
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
			elif command == Command.DeleteCategoryOrProduct.value:
				if CategoryOrProduct():
					PrintYELLOW("Введите id категории которую нужно удалить: ")
					сategoryId = int(input())
					query = query + "|1|" + str(сategoryId)
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
				else:
					PrintYELLOW("Введите id продукта, который нужно удалить: ")
					productId = int(input())
					query = query + "|2|" + str(productId)
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
			elif command == Command.SearchCategoryOrProduct.value:
				if CategoryOrProduct():
					PrintYELLOW("Введите id категории которую нужно найти: ")
					categoryId = int(input())
					query = query + "|1|" + str(categoryId)
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
				else:
					PrintYELLOW("Введите id продукта, который нужно найти: ")
					productId = int(input())
					query = query + "|2|" + str(productId)
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
			elif command == Command.ListOfCategoriesOrProducts.value:
				if CategoryOrProduct():
					query = query + "|1"
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
				else:
					PrintYELLOW("Введите id категории: ")
					categoryId = int(input())
					query = query + "|2|" + str(categoryId)
					channel.basic_publish(exchange='', routing_key='server_queue', body=query)
			elif command == Command.Exit.value:
				channel.basic_publish(exchange='', routing_key='server_queue', body=query)
				exit()
			else:
				PrintRED("Unknown command")

			'''
			if doWeNeedCatch:
				result = s.recv(1024).decode().split('|')
			PrintResult(result)'''