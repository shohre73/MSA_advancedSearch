#! /usr/bin/python3

from abc import ABC, abstractmethod

class Problem(ABC):
	"""ABSTRACT CLASS"""
	def __init__(self):
		#super().__init__()
		pass

	@abstractmethod	
	def initialState(self):
		pass

	@abstractmethod
	def bestNeighbor(self):
		pass

	@abstractmethod
	def bestOrSimilarNeighbor(self):
		pass

	@abstractmethod
	def bestFirstNeighbor(self):
		pass

	@abstractmethod
	def bestFirstOrSimilarNeighbor(self):
		pass

	@abstractmethod
	def bestRandomNeighbor(self):
		pass

	@abstractmethod
	def bestRandomOrSimilarNeighbor(self):
		pass

	@abstractmethod
	def randomNeighbor(self):
		pass

	@abstractmethod
	def mutate(self, x):
		pass

	@abstractmethod
	def result(self, s, a):
		pass
	