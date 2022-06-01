import colorama
from colorama import Fore

def PrintGREEN(message):
	print(Fore.GREEN + message)

def PrintRED(message):
	print(Fore.RED + message)

def PrintCYAN(message):
	print(Fore.CYAN + message)

def PrintYELLOW(message):
	print(Fore.YELLOW + message)

class Author:
	def __init__(self, id, name):
		self.id = id
		self.name = name

	def PrintAuthor(self):
		PrintYELLOW("	Author id: " + str(self.id) + ", name: " + self.name)


class Publication:
	def __init__(self, id, title, idAuthors, linksToOtherPublications, keywords):
		self.id = id
		self.title = title
		self.idAuthors = idAuthors
		self.linksToOtherPublications = linksToOtherPublications
		self.keywords = keywords
		self.rating = 0

	def PrintPublication(self):
		PrintYELLOW(
			"	Publication id: " + str(self.id) + ", title: " + self.title +
			", idAuthors: " + str(self.idAuthors) + ", linksToOtherPublications: " + str(self.linksToOtherPublications))

	def IncreaseRating(self):
		self.rating+=1

class Library:
	def __init__(self):
		self.mAuthors = dict()
		self.mPublications = dict()

	def AddAuthor(self, nameAuthor):
		if len(self.mAuthors) == 0:
			idAuthor = 0
		else:
			idAuthor = max(self.mAuthors.keys()) + 1
		newAuthor = Author(idAuthor, nameAuthor)
		self.mAuthors[idAuthor] = newAuthor
		PrintGREEN("Author " + nameAuthor +" successfully added")


	def AddPublication(self, title, idAuthorsList, linksToOtherPublicationsList, keywords):
		if len(self.mPublications) == 0:
			idPublication = 0
		else:
			idPublication = max(self.mPublications.keys()) + 1

		if idAuthorsList and len(self.mAuthors) < max(idAuthorsList):
			PrintRED("Error: Author with id " + max(idAuthorsList) + " does not exist")
			PrintYELLOW("Publication not created, please try again")
			return
		if linksToOtherPublicationsList and len(self.mPublications) < max(linksToOtherPublicationsList):
			PrintRED("Error: A link to a non-existent post has been added")
			PrintYELLOW("Publication not created, please try again")
			return

		newPublication = Publication(idPublication, title, idAuthorsList, linksToOtherPublicationsList, keywords)
		self.mPublications[idPublication] = newPublication
		PrintGREEN("Publication " + title +" successfully added")


	def PrintAllAuthors(self):
		PrintGREEN("All Authors: ")
		for idAuthor in self.mAuthors:
			self.mAuthors[idAuthor].PrintAuthor()

	def PrintAllPublications(self):
		PrintGREEN("All Publications: ")
		for idPublication in self.mPublications:
			self.mPublications[idPublication].PrintPublication()

	def PrintLinksToOtherPublications(self, idPublication):
		if len(self.mPublications) < idPublication:
			PrintRED("Error: publication " + str(idPublication) + " not found, please try again")
			return

		PrintGREEN("Links To Other Publications in publication: " + str(idPublication))
		for id in self.mPublications[idPublication].linksToOtherPublications:
			self.mPublications[id].PrintPublication()

	def KeywordSearch(self, listOfKeywords):
		PrintGREEN("KeywordSearch: " + str(listOfKeywords))
		for idPublication in self.mPublications:
			if str(listOfKeywords).strip('[]') in str(self.mPublications[idPublication].keywords).strip('[]'):
				self.mPublications[idPublication].PrintPublication()
				self.mPublications[idPublication].IncreaseRating()

	def SearchByAuthors(self, idAuthorsList):
		PrintGREEN("SearchByAuthors id = : "+ str(idAuthorsList))
		for idPublication in self.mPublications:
			if str(idAuthorsList).strip('[]') in str(self.mPublications[idPublication].idAuthors).strip('[]'):
				self.mPublications[idPublication].PrintPublication()
				self.mPublications[idPublication].IncreaseRating()


if __name__ == '__main__':

	library = Library()

	library.AddAuthor("name1")
	library.AddAuthor("name2")
	library.AddAuthor("name3")
	library.AddAuthor("name4")
	library.AddPublication("publication1", [0, 2], [], ["keyword1", "keyword2"])
	library.AddPublication("publication2", [0, 4], [1], ["keyword3", "keyword4"])
	library.AddPublication("publication3", [2], [], ["keyword1", "keyword4"])
	library.AddPublication("publication4", [3], [1, 2, 3], ["keyword3", "keyword2"])
	library.AddPublication("publication5", [], [1, 2, 3, 4, 5], ["keyword5", "keyword2"])
	library.AddPublication("publication5", [1, 2], [1, 2, 3, 4], ["keyword1"])
	library.AddPublication("publication6", [], [1, 2, 3, 4, 5], ["keyword6", "keyword7"])

	library.PrintAllAuthors()
	library.PrintAllPublications()

	library.PrintLinksToOtherPublications(1)
	library.PrintLinksToOtherPublications(18)
	library.PrintLinksToOtherPublications(5)

	library.SearchByAuthors(2)
	library.KeywordSearch(["keyword1"])
	library.KeywordSearch(["keyword3"])
