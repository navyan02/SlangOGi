class SlangOGi:
    def __init__(self):
        # Define states
        self.states = ["Start", "Middle", "Emoji", "Accept"]
        self.current_state = "Start"
      
        # Define transitions
        self.transitions = {
            "Start": {"LOL": "Middle", "OMG": "Middle", "SMH": "Middle", "IDK": "Middle"},
            "Middle": {"LOL": "Middle", "OMG": "Middle", "SMH": "Middle", "IDK": "Middle",
                       "😱": "Emoji", "😂": "Emoji", "🤷": "Emoji", "🙄": "Emoji"},
            "Emoji": {}
        }

        # Define abbreviation-emoji mapping
        self.valid_pairs = {
            "LOL": "😂",
            "OMG": "😱",
            "SMH": "🙄",
            "IDK": "🤷"
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

    def accept_with_path(self, input_sequence):
        """ Returns acceptance status and path taken through states, or just reject. """
        self.reset()
        path = ["Start"]  # Start tracking path

        for i, symbol in enumerate(input_sequence):
            # Check if the symbol is valid for the current state
            if symbol in self.transitions[self.current_state]:
                self.current_state = self.transitions[self.current_state][symbol]
                path.append(self.current_state)  # Record the state transition
                if self.current_state == "Middle":  # Record the abbreviation
                    self.abbreviations.add(symbol)
                elif self.current_state == "Emoji":  # Verify emoji match
                    if i != len(input_sequence) - 1:  # Emoji not at the end
                        return "reject",  # Return only "reject" without path
                    # Check if emoji matches any abbreviation
                    if not any(self.valid_pairs[abbr] == symbol for abbr in self.abbreviations):
                        return "reject",  # Return only "reject" without path
            else:
                return "reject",  # Return only "reject" without path
      
        # Final validation: Accept only if in the Emoji state
        if self.current_state == "Emoji":
            return "accept", path  # Return acceptance and path
        else:
            return "reject",  # Return only "reject" without path

# Testing function
def test_dfa(dfa, test_cases):
    results = {}
    for sequence in test_cases:
        result = dfa.accept_with_path(sequence)
        results[" ".join(sequence)] = result  # Join input sequence for display
    return results

# Define test cases for processing
test_cases = [
    ["LOL", "😂"],                  # Valid: Single abbreviation, correct emoji
    ["IDK", "🤷"],                  # Valid: Single abbreviation, correct emoji
    ["LOL", "OMG", "😂"],           # Valid: Emoji matches one abbreviation (LOL)
    ["OMG", "LOL", "🙄"],           # Invalid
    ["OMG", "LOL", "😱"],           # Valid: Emoji matches one abbreviation (OMG)
    ["LOL", "IDK", "🤷"],           # Valid: Emoji matches one abbreviation (IDK)
    ["LOL", "🤷"],                  # Invalid: Emoji does not match abbreviation
    ["SMH", "😂"],                  # Invalid: Emoji does not match abbreviation
    ["OMG", "😱", "LOL"],           # Invalid: Emoji not at end
    ["😂"],                         # Invalid: No abbreviation
    ["LOL", "OMG", "😱"],           # Valid: Emoji matches one abbreviation (OMG)
]

# Initialize DFA
dfa = SlangOGi()

# Test all cases and print results with paths
test_results = test_dfa(dfa, test_cases)

for sequence, result in test_results.items():
    if result[0] == "accept":
        print(f"Input: {sequence} -> Result: {result[0]}, Path: {result[1]}")
    else:
        print(f"Input: {sequence} -> Result: {result}")
