import enum
from colorprint import PrintGREEN, PrintCYAN

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
			  "4 - видалення категорії або продукту \n" +
			  "5 - пошук категорії або продукту \n" +
			  "6 - вивод списку категорій або продуктів за заданою категорією \n" +
			  "7 - вихід")

def CategoryOrProduct () :
	PrintGREEN("1 - Категория, 2 - Продукт. Введите команду:")
	return int(input()) == 1