

#     Linha 1: alfabeto de entrada
#    Linha 2: alfabeto da fita
#    Linha 3: simbolo que representa um espaco em branco na fita
#    Linha 4: estado inicial
#    Linha 5, coloquem uma linha indicando o conjunto de estados de aceitacao
#    Linhas 6 em diante: transicoes, uma por linha, no formato estado atual, simbolo atual,  novo estado, novo simbolo, direcao para mover a cabeca

from xml.etree import ElementTree as ET
import csv
import sys

class Production(object):
	def __init__(self, head, body):
		self.head = head
		self.body = body

	def __lt__(self, other):
		if self.head != other.head:
			return self.head < other.head
		if self.body != other.body:
			return self.body < other.body
		return 0


class Jflap2Utfpr(object):
	def __init__(self):
		self.alphabet = set()
		self.variables = set()
		self.initialVariable = None
		self.productions = set()
		self.blankSymbol = 'B'

	def convert(self, inputFile, outputFile, blankSymbol = 'B', alphabet = None):
		self.blankSymbol = blankSymbol
		if alphabet is not None:
			self.alphabet = alphabet

		xmldoc = ET.parse(inputFile)
		root = xmldoc.getroot()

		for s in root.findall('production'):
			head = s.find('left').text
			body = s.find('right').text
			if body == None:
				body = self.blankSymbol
			if len(self.variables) == 0:
				self.initialVariable = head
			self.variables.add(head)
			self.productions.add(Production(head, body))

		for t in self.productions:
			if t.body != self.blankSymbol:
				for symbol in t.body:
					self.alphabet.add(symbol)
		self.alphabet = self.alphabet.difference(self.variables)
			
	
		with open(outputFile, 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=' ')
			writer.writerow(list(self.alphabet))
			writer.writerow(list(self.variables))
			writer.writerow(self.initialVariable)
			for t in self.productions:
				writer.writerow([t.head, t.body])



if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "Parametros insuficientes. Informe o nome de arquivo de entrada e o nome do arquivo de saida"
		sys.exit(1)
	converter = Jflap2Utfpr()
	converter.convert(sys.argv[1], sys.argv[2], "epsilon")

