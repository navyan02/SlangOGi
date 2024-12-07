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


   def reset(self):
       self.current_state = "Start"
       self.last_abbreviation = None


   def process_input(self, input_sequence):
       self.reset()
       for i, symbol in enumerate(input_sequence):
           # Check if the symbol is valid for the current state
           if symbol in self.transitions[self.current_state]:
               self.current_state = self.transitions[self.current_state][symbol]
               if self.current_state == "Middle":
                   self.last_abbreviation = symbol  # Track the last abbreviation
               elif self.current_state == "Emoji":
                   if i != len(input_sequence) - 1:  # Emoji not at the end
                       return "reject"
                   # Validate emoji matches the last abbreviation
                   if self.valid_pairs.get(self.last_abbreviation) != symbol:
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
   ["LOL", "😂"],                  # Valid: Last abbreviation matches emoji
   ["IDK", "🤷‍♀️"],              # Valid: Last abbreviation matches emoji
   ["LOL", "OMG", "😱"],          # Valid: Last abbreviation matches emoji
   ["SMH", "OMG", "🙄"],          # Invalid: Last abbreviation is OMG, emoji does not match
   ["LOL", "IDK", "🤷‍♀️"],       # Valid: Last abbreviation matches emoji
   ["LOL", "🤷‍♀️"],              # Invalid: Emoji does not match last abbreviation
   ["SMH", "😂"],                 # Invalid: Emoji does not match last abbreviation
   ["OMG", "😱", "LOL"],          # Invalid: Emoji not at end
   ["😂"],                        # Invalid: No abbreviation
   ["😱", "OMG", "LOL"],          # Invalid: Emoji not at end
]


# Initialize DFA and run tests
dfa = SlangOGi()
test_results = test_dfa(dfa, test_cases)


# Print test results
for sequence, result in test_results.items():
   print(f"Input: {sequence} -> Result: {result}")



