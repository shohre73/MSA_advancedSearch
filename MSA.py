#! /usr/bin/python3

from colorama import Fore, Back, Style

from Bio      import SeqIO
import random
import copy

from Problem  import *
from PAM      import PAM250
from MsaState import *

class MSA(Problem):
	"""docstring for MSA"""
	def __init__(self, seqAdd, p, m=100):
		#super(Problem).__init__()
		Problem.__init__(self)
		self._seq={}
		for rec in SeqIO.parse( seqAdd, "fasta"):
			self._seq[rec.id]= str(rec.seq)
		
		if p >= 1 or p<=0:
			print(Fore.RED + "Initial alignment gap probability is not acceptable\nEXITING... " + Style.RESET_ALL )
			exit()
		else:
			self._inAlgnGapProb=p

		self._maxStepNum=m
		self._seqLength= len( list(self._seq.values())[0])

	def initialState(self):
		print(Fore.WHITE + "creating new initial State" + Style.RESET_ALL)
		al =list(self._seq.values())
		for i in range(len(al)):
			for j in range(1, len(al[i])-1):
				if( random.uniform(0.0, 1.0) < self.inAlgnGapProb):
					al[i]= al[i][:j-1]+'-'+al[i][j-1:]
		return MsaState(al)

	def result(self, state, action):
		newState=MsaState(state.aln)
		if action[0] == 'i':
			newState.insertGap(*action)
		elif action[0] == 'd':
			newState.deleteGap(*action)
		else:
			print(Fore.RED + "UNEXPECTED CONDITION 102! exiting()" + Style.RESET_ALL)
			exit()

		return newState 

	def bestNeighbor(self, state):
		actions= state.getActions()
		bestAction=None
		bestNeighbor= copy.copy(state)
		for a in actions:
			temp= self.result(state, a)
			if temp.score > bestNeighbor.score :
				bestAction= a
				bestNeighbor = temp
		return bestAction, bestNeighbor

	def bestOrSimilarNeighbor(self, state):
		actions= state.getActions()
		bestAction=None
		bestNeighbor= copy.copy(state)
		similarActions= list()
		similarNeighbors=list()
		for a in actions:
			temp= self.result(state, a)
			if temp.score > bestNeighbor.score :
				bestAction= a
				bestNeighbor = temp
			elif temp.score == state.score:
				similarActions.append(a)
				similarNeighbors.append(temp)

		if bestAction is None:
			if similarActions:
				randIndex= random.randint(0, len(similarActions)-1)
				randomSimilarAction= similarActions[randIndex]
				randomSimilarNeigbor= similarNeighbors[randIndex]
				return randomSimilarAction, randomSimilarNeigbor

		return bestAction, bestNeighbor

	def bestFirstNeighbor(self, state):
		actions= state.getActions()
		bestFirstAction=None
		bestFirstNeighbor= copy.copy(state)
		for a in actions:
			temp= self.result(state, a)
			if temp.score > bestFirstNeighbor.score :
				bestFirstAction= a
				bestFirstNeighbor = temp
				break
		return bestFirstAction, bestFirstNeighbor

	def bestFirstOrSimilarNeighbor(self, state):
		actions= state.getActions()
		bestFirstAction=None
		bestFirstNeighbor= copy.copy(state)
		similarActions= list()
		similarNeighbors=list()
		for a in actions:
			temp= self.result(state, a)
			if temp.score > bestFirstNeighbor.score :
				bestFirstAction= a
				bestFirstNeighbor = temp
				break
			elif temp.score == state.score:
				similarActions.append(a)
				similarNeighbors.append(temp)

		if bestFirstAction is None:
			if similarActions:
				randIndex= random.randint(0, len(similarActions)-1)
				randomSimilarAction= similarActions[randIndex]
				randomSimilarNeigbor= similarNeighbors[randIndex]
				return randomSimilarAction, randomSimilarNeigbor

		return bestFirstAction, bestFirstNeighbor

	def bestRandomNeighbor(self, state):
		actions= state.getActions()
		bestRandomAction=None
		bestRandomNeighbor= copy.copy(state)
		for a in actions:
			temp= self.result(state, a)
			if temp.score > bestRandomNeighbor.score :
				bestRandomAction= a
				bestRandomNeighbor = temp
				break
		return bestRandomAction, bestRandomNeighbor
	
	def bestRandomOrSimilarNeighbor(self, state):
		actions= state.getActions()
		bestRandomAction=None
		bestRandomNeighbor= copy.copy(state)
		similarActions= list()
		similarNeighbors=list()
		for a in actions:
			temp= self.result(state, a)
			if temp.score > bestRandomNeighbor.score :
				bestRandomAction= a
				bestRandomNeighbor = temp
				break
			elif temp.score == state.score:
				similarActions.append(a)
				similarNeighbors.append(temp)

		if bestRandomAction is None:
			if similarActions:
				randIndex= random.randint(0, len(similarActions)-1)
				randomSimilarAction= similarActions[randIndex]
				randomSimilarNeigbor= similarNeighbors[randIndex]
				return randomSimilarAction, randomSimilarNeigbor

		return bestRandomAction, bestRandomNeighbor

	def randomNeighbor(self, state):
		actions= state.getActions()
		randomAction = random.choice(actions)
		randomNeighbor = self.result(state, randomAction) 
		return randomAction, randomNeighbor

	def mutate(self, state):
		for i in range(len(state.aln)):
			j = random.randint(1, len(state.aln[i])-1)
			if state.aln[i][j] is not '-':
				state.insertGap( 'i', i, j)
			else:
				state.deleteGap( 'd', i, j)
		return state

	def cross(self, st1, st2):
		alphabet= random.randint(1, self._seqLength-1)
		breakPoint1=0
		ac=0
		for c in st1.aln[0]:
			if c is not '-' :
				ac+=1
			breakPoint1+=1
			if ac == alphabet:
				break
		breakPoint2=0
		ac=0
		for c in st2.aln[0]:
			if c is not '-' :
				ac+=1
			breakPoint2+=1
			if ac == alphabet:
				break
		
		newAln1= list()
		newAln2= list()
		for i in range(0, len(st1.aln)):
			seq1= ''
			seq2= ''
			leftSeq1  = st1.aln[i][ : breakPoint1]
			rightSeq1 = st2.aln[i][ breakPoint2 :]
			leftSeq2  = st2.aln[i][ : breakPoint2]
			rightSeq2 = st1.aln[i][ breakPoint1 :]
			seq1 = leftSeq1 + rightSeq1
			seq2 = leftSeq2 + rightSeq2
			
			newAln1.append(seq1)
			newAln2.append(seq2)
	
		self._trimeAlignment(newAln1)
		newSt1= MsaState(newAln1)
		self._trimeAlignment(newAln2)
		newSt2= MsaState(newAln2)

		#print(Fore.YELLOW + 'newSt1' + Style.RESET_ALL)
		#print(newSt1)
		#print(Fore.YELLOW + 'newSt2' + Style.RESET_ALL)
		#print(newSt2)

		return newSt1, newSt2
			
	def _scoreAlignment(self, al):
		# Paire wise scoring
		self._trimeAlignment(al)

		perm=[(p,q) for p in range(0,len(al)) for q in range (0,len(al)) if p<q ]
		totalScore=0
		colScore=0
		for j in range(len(al[0])):
			colScore=0
			for c in range(len(perm)):
				a,b = perm[c]
				colScore= colScore + PAM250[al[a][j]][al[b][j]]
			totalScore= totalScore + colScore
			
		return totalScore

	def _trimeAlignment(self, aln):
		maxLen = len(max(aln, key=len))
		for i in range(len(aln)):
			while aln[i][-1]=='-':
				aln[i]= aln[i][:-1]

		for i in range(len(aln)):
			if len(aln[i]) < maxLen:
				for c in range(maxLen-len(aln[i])):
					aln[i]= aln[i]+ '-'
		return aln

	@property
	def seq(self):
		return self._seq

	@property
	def inAlgnGapProb(self):
		return self._inAlgnGapProb
		
	@property
	def maxStepNum(self):
		return self._maxStepNum
	@property
	def seqLength(self):
		return self._seqLength

