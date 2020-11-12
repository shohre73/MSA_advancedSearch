#! /usr/bin/python3

from colorama import Fore, Back, Style

import sys

from MSA      import *
from Problem  import *
from MsaState import *

from HillClimbing       import *
from SimulatedAnnealing import *
from GeneticAlg         import *
#from AntColony          import *

def localSearch(msa):
	
	strategies=[msa.bestNeighbor, 
				msa.bestFirstNeighbor, 
				msa.bestRandomNeighbor,
				msa.bestOrSimilarNeighbor,  
				msa.bestFirstOrSimilarNeighbor, 
				msa.bestRandomOrSimilarNeighbor]
	initialState=msa.initialState()

	for s in strategies:
		print('Calculating average final Score for HillClimbing')
		print("Strategy: " + Fore.YELLOW + s.__name__ + Style.RESET_ALL)
		print('Running Algorithm on 10 random initial States')
		print()
		avResScore=0
		avStepCounter=0
		for i in range(10):
			inSt=msa.initialState()
			hc= HillClimbing(msa, inSt, s)
			avResScore+= hc.result.score
			avStepCounter+=hc.stepCounter
	
		print( "Average result Score on 10 attempts: " + Fore.GREEN + str(avResScore/10) + Style.RESET_ALL)
		print( "Average result Steps on 10 attempts: " + Fore.GREEN + str(avStepCounter/10) + Style.RESET_ALL)
		input("Press Enter to continue...")
	

	#HillClimbing(msa, initialState, msa.bestFirstNeighbor)
	#HillClimbing(msa, initialState, msa.bestRandomNeighbor)
	#SimulatedAnnealing(msa, initialState, msa.randomNeighbor)
	#GeneticAlg(msa, 0.001, 4, 100)
	#AntColony(msa, 2, 100)
    

if __name__ == "__main__":

	seqAddress = sys.argv[1]
	prob = float(sys.argv[2])
	
	msa=MSA(seqAddress, prob)

	'''
	print('Calculating average initialScore withi Different inGapProb')
	print('Running Algorithm for 10 random initial States')
	print()
	probList=[0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001]
	for p in probList:
		avInScore=0
		for i in range(20):
			tempMsa = MSA(seqAddress, p)
			inScore = tempMsa.initialState().score
			print("inScore: ", inScore)
			avInScore+= inScore
		
		print( "Average initialScore in 10 attemps with " + Fore.YELLOW + str(p) + " : " + Fore.GREEN + str(avInScore/20) + Style.RESET_ALL)
		input("Press Enter to continue...")

	exit()
	'''


	'''
	seq1='--GKGDPKKPRGKMSSYAFFVQTSREEHKKKHPDASVNFSEFSKKCSERWKTMSAKEKGKFEDMAKADKARYEREMKTYIPPKGE----------'
	seq2='------MQDRVKRPMNAFIVWSRDQRRKMALENP--RMRNSEISKQLGYQWKMLTEAEKWPFFQEAQKLQAMHREKYPNYKYRPRRKAKMLPK---'
	seq3='MKKLKKHPDFPKKPLTPYFRFFMEKRAKYAKLHP--EMSNLDLTKILSKKYKELPEKKKMKYIQDFQREKQEFERNLARFREDHPDLIQNAKK---'
	seq4='--------MHIKKPLNAFMLYMKEMRANVVAEST--LKESAAINQILGRRWHALSREEQAKYYELARKERQLHMQLYPGWSARDNYGKKKKRKREK'

	seqList=[seq1, seq2, seq2, seq3]

	tempState= MsaState(seqList)
	print(tempState.score)
	'''
	localSearch(msa)

	print(Fore.GREEN + "FINIHED SUCCESSFULLY" + Style.RESET_ALL)




    