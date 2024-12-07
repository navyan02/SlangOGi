class SlangOGi:
   def __init__(self):
       # Define states
       self.states = ["Start", "Middle", "Emoji", "Accept"]
       self.current_state = "Start"
      
       # Define transitions
       self.transitions = {
           "Start": {"LOL": "Middle", "OMG": "Middle", "SMH": "Middle", "IDK": "Middle"},
           "Middle": {"LOL": "Middle", "OMG": "Middle", "SMH": "Middle", "IDK": "Middle",
                      "😱": "Emoji", "😂": "Emoji", "🤷‍♀️": "Emoji", "🙄": "Emoji"},
           "Emoji": {}
       }


       # Define abbreviation-emoji mapping
       self.valid_pairs = {
           "LOL": "😂",
           "OMG": "😱",
           "SMH": "🙄",
           "IDK": "🤷‍♀️"
       }
      
       # Track all encountered abbreviations
       self.abbreviations = set()


   def reset(self):
       self.current_state = "Start"
       self.abbreviations = set()


   def process_input(self, input_sequence):
       self.reset()
       for i, symbol in enumerate(input_sequence):
           # Check if the symbol is valid for the current state
           if symbol in self.transitions[self.current_state]:
               self.current_state = self.transitions[self.current_state][symbol]
               if self.current_state == "Middle":  # Record the abbreviation
                   self.abbreviations.add(symbol)
               elif self.current_state == "Emoji":  # Verify emoji match
                   if i != len(input_sequence) - 1:  # Emoji not at the end
                       return "reject"
                   # Check if emoji matches any abbreviation
                   if not any(self.valid_pairs[abbr] == symbol for abbr in self.abbreviations):
                       return "reject"
           else:
               return "reject"
      
       # Final validation: Accept only if in the Emoji state
       return "accept" if self.current_state == "Emoji" else "reject"


# Testing function
def test_dfa(dfa, test_cases):
   results = {}
   for sequence in test_cases:
       result = dfa.process_input(sequence)
       results[" ".join(sequence)] = result
   return results


# Define test cases
test_cases = [
   ["LOL", "😂"],                  # Valid: Single abbreviation, correct emoji
   ["IDK", "🤷‍♀️"],              # Valid: Single abbreviation, correct emoji
   ["LOL", "OMG", "😂"],          # Valid: Emoji matches one abbreviation (LOL)
   ["OMG", "LOL", "🙄"],          # Valid: Emoji matches one abbreviation (SMH)
   ["OMG", "LOL", "😱"],          # Valid: Emoji matches one abbreviation (OMG)
   ["LOL", "IDK", "🤷‍♀️"],       # Valid: Emoji matches one abbreviation (IDK)
   ["LOL", "🤷‍♀️"],              # Invalid: Emoji does not match abbreviation
   ["SMH", "😂"],                 # Invalid: Emoji does not match abbreviation
   ["OMG", "😱", "LOL"],          # Invalid: Emoji not at end
   ["😂"],                        # Invalid: No abbreviation
   ["LOL", "OMG", "😱"],          # Valid: Emoji matches one abbreviation (OMG)
]


# Initialize DFA and run tests
dfa = SlangOGi()
test_results = test_dfa(dfa, test_cases)


# Print test results
for sequence, result in test_results.items():
   print(f"Input: {sequence} -> Result: {result}")


