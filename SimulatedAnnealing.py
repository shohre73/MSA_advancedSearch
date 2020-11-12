#! /usr/bin/python3

from colorama import Fore, Back, Style
from math     import exp
import random

class SimulatedAnnealing(object):
	"""docstring for HillClimbing"""
	def __init__(self, problem, inState, strategy, d=100):
		self._curState = inState
		self._result = None
		self._time = 1
		self._deadLine = d
		self._solver(strategy)

	def _solver(self, strategy):
		print("SimulatedAnnealing by " +Fore.YELLOW +strategy.__name__ +Style.RESET_ALL )
		print('initialState:')
		print(self._curState)

		chosenAction= None
		chosenNeighbor= None	
		while(1):
			#print(self._curState)
			chosenAction, chosenNeighbor= strategy(self._curState)
			
			if chosenNeighbor.score > self._curState.score:
				print("Applied action: ", str(chosenAction), "\tSelected Score: ", chosenNeighbor.score)
				self._curState= chosenNeighbor
			elif chosenNeighbor.score < self._curState.score:
				print('Worse selected score', chosenNeighbor.score )
				r = random.uniform(0.0, 1.0)
				delta= chosenNeighbor.score - self._curState.score
				#print("******************************** delta: ", delta)
				#print("******************************** pow(1.1,delta): ", pow(1.1,delta)/self._time)
				#print('******************************** r : ', r)
				if  r < pow(1.1,delta)/self._time:
					print(Fore.RED + 'Making a "bad" decition' + Style.RESET_ALL)
					print("Applied action: ", str(chosenAction), "\tSelected Score: ", chosenNeighbor.score)
					self._curState= chosenNeighbor
			else:
				if random.uniform(0.0, 1.0) < 0.5:
					print(Fore.WHITE + 'Going to a new state with the similar Score' + Style.RESET_ALL)
					self._curState = chosenNeighbor

			self._time+=1			
			if self._time >= self._deadLine:
				print(Fore.RED + "TIME OUT" + Style.RESET_ALL)
				self._result= self._curState
				break

		print(Fore.YELLOW + "Final Result:  "+ Style.RESET_ALL)
		print("Strategy: " + Fore.MAGENTA + strategy.__name__  + Style.RESET_ALL +" Time passed " + Fore.CYAN + str(self._time) + Style.RESET_ALL)
		print(self._result)
		print()


	@property
	def curState(self):
		return self._curState
	@property
	def result(self):
		return self._result
	@property
	def time(self):
		return self._time
	@property
	def deadLine(self):
		return self._deadLine