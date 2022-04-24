import socket
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
	s = socket.socket()
	host = socket.gethostname()
	port = 12345
	s.connect((host, port))

	while True:
		doWeNeedCatch = True
		PrintCommands()
		PrintGREEN("Введите команду:")
		command = int(input())
		query = str(command)

		if command == Command.LoadData.value:
			s.send(query.encode())
		elif command == Command.NewCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите название категории: ")
				categoryName = input()
				query = query + "|1|" + categoryName
				s.send(query.encode())
			else:
				PrintYELLOW("Введите id категории, в которую нужно добавить продукт: ")
				categoryId = int(input())
				query = query + "|2|" + str(categoryId)
				s.send(query.encode())
				result = s.recv(1024).decode().split('|')
				doWeNeedCatch = False
				if result[0] == "True":
					PrintYELLOW("Введите название продукта: ")
					productName = input()
					PrintYELLOW("Введите цену продукта " + productName + ": ")
					productPrice = float(input())
					PrintYELLOW("Введите количество продукта " + productName + ": ")
					productAmount = int(input())
					query = "2|2|" + str(categoryId) + "|" + productName + "|" + str(productPrice) + "|" + str(productAmount)
					s.send(query.encode())
					doWeNeedCatch = True

		elif command == Command.EditCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории, которую нужно изменить: ")
				сategoryId = int(input())
				query = query + "|1|" + str(сategoryId)
				s.send(query.encode())
				result = s.recv(1024).decode().split('|')
				doWeNeedCatch = False
				if result[0] == "True":
					PrintYELLOW("Введите новое имя категории (categoryName): ")
					newCategoryName = input()
					query = "3|1|" + str(сategoryId) + "|" + newCategoryName
					s.send(query.encode())
					doWeNeedCatch = True
			else:
				PrintYELLOW("Введите id продукта, который нужно изменить: ")
				productId = int(input())
				query = query + "|2|" + str(productId)
				s.send(query.encode())
				result = s.recv(1024).decode().split('|')
				doWeNeedCatch = False
				if result[0] == "True":
					PrintYELLOW("Чтобы бы вы хотели изменить? \n" +
								"1 - название продукта \n" +
								"2 - цену продукта \n" +
								"3 - количество продукта на складе")
					commandEditProduct = int(input())
					isCorrectCommand = True
					query = "3|1|" + str(productId) + "|" + str(commandEditProduct) + "|"
					if commandEditProduct == 1:
						PrintYELLOW("Введите новое имя продукта: ")
						productName = input()
						query = query + productName
					elif commandEditProduct == 2:
						PrintYELLOW("Введите новую цену продукта: ")
						productPrice = input()
						query = query + productPrice
					elif commandEditProduct == 3:
						PrintYELLOW("Введите новое количество продукта на складе: ")
						productAmount = input()
						query = query + productAmount
					else:
						PrintRED("Unknown command")
						isCorrectCommand = False
					if isCorrectCommand:
						s.send(query.encode())
						doWeNeedCatch = True
						doWeNeedCatch = True
		elif command == Command.DeleteCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно удалить: ")
				сategoryId = int(input())
				query = query + "|1|" + str(сategoryId)
				s.send(query.encode())
			else:
				PrintYELLOW("Введите id продукта, который нужно удалить: ")
				productId = int(input())
				query = query + "|2|" + str(productId)
				s.send(query.encode())
		elif command == Command.SearchCategoryOrProduct.value:
			if CategoryOrProduct():
				PrintYELLOW("Введите id категории которую нужно найти: ")
				categoryId = int(input())
				query = query + "|1|" + str(categoryId)
				s.send(query.encode())
			else:
				PrintYELLOW("Введите id продукта, который нужно найти: ")
				productId = int(input())
				query = query + "|2|" + str(productId)
				s.send(query.encode())
		elif command == Command.ListOfCategoriesOrProducts.value:
			if CategoryOrProduct():
				query = query + "|1"
				s.send(query.encode())
			else:
				PrintYELLOW("Введите id категории: ")
				categoryId = int(input())
				query = query + "|2|" + str(categoryId)
				s.send(query.encode())
		elif command == Command.Exit.value:
			s.send(query.encode())
			exit()

		if doWeNeedCatch:
			result = s.recv(1024).decode().split('|')
		PrintResult(result)