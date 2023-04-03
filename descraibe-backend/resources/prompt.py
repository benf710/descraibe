import string 

letter_rarity_dict = {'A':1,'B':3,'C':3,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':8,'K':5,'L':1,'M':3,'N':1,'O':1,'P':3,'Q':10,'R':1,'S':1,'T':1,'U':1,'V':4,'W':4,'X':8,'Y':4,'Z':10}

class Prompt:
    def __init__(self,prompt_text) -> None:
        # Remove punctuation and make all letters uppercase
        self.text = prompt_text.upper().translate(str.maketrans('', '', string.punctuation)).replace('\n','')
        # Calculate the sum of each letter's rarity
        self.prompt_rarity_sum = sum([letter_rarity_dict[letter] if letter in letter_rarity_dict else 0 for letter in self.text])
        # Calculate the number of letters in the prompt
        self.letter_count = sum([1 if letter in letter_rarity_dict else 0 for letter in self.text])
        # Calculate the mean letter-rarity of the prompt
        self.difficulty = self.prompt_rarity_sum / self.letter_count
        pass

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text
