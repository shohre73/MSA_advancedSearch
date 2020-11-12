#! /usr/bin/python

import sys
from Bio import SeqIO

from MSA import MSA
from MsaState import MsaState
from colorama import Fore, Back, Style


if __name__ == "__main__":

	seqAddress = sys.argv[1]
	prob = float(sys.argv[2])
	
	localSearch=['hillClimbing']
	strategies=['bestNeighbor', 'bestFirstNeighbor', 'bestRandomNeighbor']
	#print("RUN: Python3 hillClimbing.py " +  Fore.WHITE + "input.fasta strategy initial-alignment-gap-probability" + Style.RESET_ALL)
	#print("Provided Strategies: \n\tbestNeighbor\n\tbestFirstNeighbor\n\tbestRandomNeighbor\n\tALL -> for all strategies ")
	#exit(1)
	
	inputSeq=list()
	for seqRec in SeqIO.parse( seqAddress, "fasta"):
		inputSeq.append(str(seqRec.seq))
	
	
	msa=MSA(inputSeq, prob, sys.argv)
	
	#initialState = msa.initialState()
	#print( "Initial State: ")
	#print(initialState)	
	
	#msa.simulatedAnnealing(initialState)

	print( Fore.YELLOW + "Genetic Algorithm: " + Style.RESET_ALL)
	inStNum = 2
	msa.geneticAlg( inStNum)
	
	'''
	for l in localSearch:
		for s in strategies:
			getattr(msa, l)(initialState, s )
			#msa.hillClimbing(initialState, s)
	'''

	print(Fore.RED + "FINIHED SUCCESSFULLY" + Style.RESET_ALL)
