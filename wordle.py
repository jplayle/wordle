from english_words import english_words_set


class wordle_solver():

	def __init__(self):
		self.words  = [word.lower() for word in english_words_set if len(word) == 5]
		self.posns  = {}
		self.chars  = []
		self.ignore = []
		self.n_posn = 0
		self.n_char = 0
		
		
	def get_initial_guess(self):
		
		char_freq = {}
		
		for word in self.words:
			for c in word:
				if c not in char_freq:
					char_freq[c] = 1
				else:
					char_freq[c] += 1
		
		word_rank = {}
					
		for word in self.words:
			skip = False
			
			for c in word:
				if word.count(c) > 1:
					skip = True
					break
					
			if skip:
				continue
			
			freq_sum = sum([char_freq[char] for char in word])
			
			if freq_sum not in word_rank:
				word_rank[freq_sum] = [word]
			else:
				word_rank[freq_sum] += [word]
				
		sorted_fs = sorted([wr for wr in word_rank])
		for fs in sorted_fs:
			print(fs, word_rank[fs])
			
		return word_rank[sorted_fs[-1]]
	
	
	def get_guess(self):
		self.guess = ""
		
		while len(self.guess) != 5:
			self.guess = input("Enter guessed word: ")
		try:
			self.words.remove(self.guess)
		except ValueError:
			pass
	
	
	def get_result(self):
		
		print("Enter results - 0 for not present, 1 for present and 2 for in position.")
		
		for i in range(5):
			c = self.guess[i]
			r = '-1'
			
			while r not in ['0', '1', '2']:
				r = input("Result for %s (0/1/2): " % c.upper())
			
			if r == '0' and c not in self.ignore:
				self.ignore += [c]
				
			elif r == '1' and c not in self.chars:
				self.chars  += [c]
				self.n_char += 1
			
			elif r == '2' and i not in self.posns:
				self.posns[i] = c
				self.n_posn  += 1
	
	
	def get_next_guess(self):
		
		if len(self.posns) == 5:
			print("Word found!")
			return 1
		
		next_guesses = []
		
		for word in self.words:
			remove = False
			n_posn = 0
			n_char = 0
			
			for i in range(5):
				char = word[i]
				
				if char in self.ignore:
					remove = True
					break
					
				if char in self.chars:
					n_char += 1
				
				if i in self.posns:
					if char == self.posns[i]:
						n_posn += 1
						
			if n_posn != self.n_posn:
				remove = True
					
			if not remove:
				next_guesses += [word]
				
		chance = 100 / len(next_guesses)

		print("Next guess: ", next_guesses[0].upper(), ("(chance: %.1f%%)" % chance), '\n')
		
		if chance == 100.0:
			return 1
		else:
			return 0
				
				
	def solve(self):
		
		print("Best initial guess: ", self.get_initial_guess(), '\n')
		
		self.get_guess()
		self.get_result()
		
		n = 0
		while not self.get_next_guess():
			n += 1
			if n == 5:
				break
			self.get_guess()
			self.get_result()			
				


def main():
	
	ws = wordle_solver()
	
	ws.solve()
	
	
if __name__ == '__main__':
		main()