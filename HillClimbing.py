#! /usr/bin/python

from colorama import Fore, Back, Style

import matplotlib.pyplot as plt

class HillClimbing(object):
	"""docstring for HillClimbing"""
	def __init__(self, problem, inState, strategy, msn=200, fl=20):
		self._curState = inState
		self._result = None
		self._stepCounter = 1
		self._maxStepNum = msn
		self._flatLimit= fl
		self._solver(strategy)

	def _solver(self, strategy):
		print("HillClimbing by " +Fore.YELLOW +strategy.__name__ +Style.RESET_ALL)
		print("Initial State Score:\t" + Fore.GREEN + str(self._curState.score) + Style.RESET_ALL)
		chosenAction = None
		chosenNeighbor= None
		scoresList=[self._curState.score]
		flatCounter=0
		while(1):
			#print(self._curState)
			chosenAction, chosenNeighbor= strategy(self._curState)
	
			if chosenAction is None:
				print(Fore.RED + "NO action can be applied" + Style.RESET_ALL)
				self._result= self._curState
				break

			if chosenNeighbor.score == self._curState.score:
				flatCounter+=1
			else:
				flatCounter=0

			if flatCounter >= self._flatLimit:
				self._result= self._curState
				print(Fore.RED + "looped inf lat area for " + str(self._flatLimit) + " times" + Style.RESET_ALL)
				break

			print("Applied action: ", str(chosenAction), "\tSelected Score: ", chosenNeighbor.score)
			self._curState= chosenNeighbor
			self._stepCounter+=1
			scoresList.append(self._curState.score)
			
			if self._stepCounter == self._maxStepNum:
				print(Fore.RED + "Maximum number of" + str(self._maxStepNum) + "states was reached" + Style.RESET_ALL)
				break

		'''		
		plt.plot(scoresList)
		plt.ylim([ scoresList[0] , 300])
		plt.ylabel("Scores in HillClimbing by "+strategy.__name__)
		plt.show()
	    '''

		print(Fore.YELLOW + "Final Result:  "+ Style.RESET_ALL)
		print("Strategy: " + Fore.MAGENTA + strategy.__name__  + Style.RESET_ALL +" Num of Steps " + Fore.CYAN+ str(self._stepCounter) + Style.RESET_ALL)
		print(self._result)
		print()


	@property
	def curState(self):
		return self._curState
	@property
	def result(self):
		return self._result
	@property
	def stepCounter(self):
		return self._stepCounter
	@property
	def maxStepNum(self):
		return self._maxStepNum