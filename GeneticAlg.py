#! /usr/bin/python

from colorama import Fore, Back, Style

import math
import copy
import random

class GeneticAlg(object):
	"""docstring for GeneticAlg"""
	def __init__(self, problem, mp=0.001, n=4, d=100):
		self._population = n
		self._curGeneration=list()
		for i in range(0, self._population):
			self._curGeneration.append(problem.initialState())
		self._mutationProb= mp
		self._time=1
		self._deadLine=d
		#self.printGeneration(self._curGeneration)
		self._solver( problem.mutate, problem.cross )

	def _solver(self,  mutate, cross):
		self.printGeneration(self._curGeneration)
		while 1:
			self._curGeneration= sorted(self._curGeneration, key=lambda state: state.score, reverse= True )
			# The best half
			newGeneration=list( copy.copy(self._curGeneration[i]) for i in range(math.floor(self._population/2))) 
			# The worst half
			juckIndividuals=list( copy.copy(self._curGeneration[i]) for i in range(math.floor(self._population/2), self._population)) 
			
			while len(juckIndividuals) >1:
				individual1 = random.choice(juckIndividuals)
				juckIndividuals.remove(individual1)
				individual2 = random.choice(juckIndividuals)
				juckIndividuals.remove(individual2)

				newMember1, newMember2 = cross(individual1, individual2)
				
				if random.uniform(0.0, 1.0) < self._mutationProb :
					mutate(newMember1)	
				if random.uniform(0.0, 1.0) < self._mutationProb:
					mutate(newMember2)

				newGeneration.append(newMember1)
				newGeneration.append(newMember2)
	
			#self.printGeneration(self._curGeneration)
			#self.printGeneration(newGeneration)
			#self.printGeneration(juckIndividuals)
			
			self._curGeneration= newGeneration

			self._time+=1			
			if self._time >= self._deadLine:
				print(Fore.RED + "TIME OUT" + Style.RESET_ALL)
				self._result = max(self._curGeneration, key= lambda state: state.score)
				break

		self._curGeneration= sorted(self._curGeneration, key=lambda state: state.score, reverse= True )
		self.printGeneration(self._curGeneration)

		return self._result
			


	def printGeneration(self, generation):
		print(Fore.YELLOW + "Current Generation:" + Style.RESET_ALL)
		for g in generation:
			print(g)

	@property
	def population(self):
		return self._population

	@property
	def curGeneration(self):
		return self._curGeneration

	@property
	def mutationProb(self):
		return self._mutationProb