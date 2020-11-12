#! /usr/bin/python3

from colorama import Fore, Back, Style

#from PAM   import PAM250
from Bio.SubsMat import MatrixInfo
#from State import *


class MsaState():
	"""docstring for State"""
	def __init__(self, sequences):
		self._aln = list(sequences)
		self._setScore()

	def getActions(self):
		actions=[('i', i, j) for i in range(len(self._aln)) for j in range(len(self._aln[i])-1)]
		for i in range(len(self._aln)):
			for j in range(len(self._aln[i])):
				if self._aln[i][j] == '-':
					actions.append(( 'd', i, j))
		return actions 

	def insertGap(self, _, i, j):
		self._aln[i]= self._aln[i][:j]+'-'+ self._aln[i][j:]
		if self._aln[i][-1] == '-':
			self._aln[i]= self._aln[i][:-1]	
		self._setScore()
		return True

	def deleteGap(self, _, i, j):
		if self.aln[i][j] == '-':
			self._aln[i]= self._aln[i][:j]+ self._aln[i][j+1:]
		self.aln[i]= self.aln[i] + '-'
			
	def _setScore(self, matrix=MatrixInfo.blosum62, gap_s=-5, gap_e=0):
		self._trimeAlignment()
		perm=[(p,q) for p in range(0,len(self._aln)) for q in range (0,len(self._aln)) if p<q ]
		totalScore=0
		for c in range(len(perm)):
			s1, s2= perm[c]
			totalScore+= self._score_pairwise(self._aln[s1],self._aln[s2],matrix, gap_s, gap_e)

		self._score= totalScore
		return totalScore

	def _score_pairwise(self, seq1, seq2, matrix, gap_s, gap_e):
		# Using bioPython library 
		score = 0
		gap = False
		for i in range(len(seq1)):
			pair = (seq1[i], seq2[i])
			if not gap:
				if '-' in pair:
					gap = True
					score += gap_s
				else:
					score += self._score_match(pair, matrix)
			else:
				if '-' not in pair:
					gap = False
					score += self._score_match(pair, matrix)
				else:
					score += gap_e
		return score

	def _score_match(self, pair, matrix):
		if pair not in matrix:
			return matrix[(tuple(reversed(pair)))]
		else:
			return matrix[pair]

	def _setScore_v2(self):
		# Paire wise scoring
		self._trimeAlignment()
		perm=[(p,q) for p in range(0,len(self._aln)) for q in range (0,len(self._aln)) if p<q ]
		totalScore=0
		for j in range(len(self._aln[0])):
			colScore=0
			for c in range(len(perm)):
				a,b = perm[c]
				colScore= colScore + PAM250[self._aln[a][j]][self._aln[b][j]]
			totalScore= totalScore + colScore
			
		self._score= totalScore
		return totalScore

	def _trimeAlignment(self):
		maxLen = len(max(self._aln, key=len))
		for i in range(len(self._aln)):
			if len(self._aln[i]) < maxLen:
				self._aln[i]= self._aln[i] +  ('-' * (maxLen - len(self._aln[i])))

	@property
	def aln(self):
		return self._aln

	@property
	def score(self):
		return self._score

	def __str__(self):
		return (Fore.WHITE+ 'Alignment:'  + Fore.GREEN +'  Score: ' + str(self._score) + '\n' + Style.RESET_ALL) + '\n'.join(self._aln) +'\n'
		
		
