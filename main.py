class ChatSlangDFA:
    def __init__(self):
        # Define states
        self.states = ["Start", "Middle", "Emoji", "Accept"]
        self.current_state = "Start"
        
        # Define transitions: {"state": {"input_symbol": "next_state"}}
        self.transitions = {
            "Start": {"LOL": "Middle", "OMG": "Middle", "SMH": "Middle", "IDK": "Middle"},
            "Middle": {"LOL": "Middle", "BRB": "Middle", "SMH": "Middle", "IDK": "Middle",
                       "😱": "Emoji", "😂": "Emoji", "🤷‍♀️": "Emoji", "🙄": "Emoji"},
            "Emoji": {"😱": "Accept", "😂": "Accept", "🤷‍♀️": "Accept", "🙄": "Accept"}
        }
        
        # Define accepting state
        self.accepting_state = "Accept"

    def reset(self):
        self.current_state = "Start"

    def process_input(self, input_sequence):
        self.reset()
        for symbol in input_sequence:
            # Move to next state based on input symbol
            if symbol in self.transitions[self.current_state]:
                self.current_state = self.transitions[self.current_state][symbol]
            else:
                return "reject"
        # Final state check
        if self.current_state == self.accepting_state:
            return "accept"
        return "reject"
# Testing function
def test_dfa(dfa, test_cases):
    results = {}
    for sequence in test_cases:
        result = dfa.process_input(sequence)
        results[" ".join(sequence)] = result
    return results

# Define test cases
test_cases = [
    ["LOL", "😂"],
    ["BRB", "🤷‍♀️"],
    ["LOL", "BRB", "SMH", "🙄"],
    ["LOL", "😱", "LOL"],  # Invalid sequence
    ["SMH", "😂", "BRB"],  # Invalid sequence
]

# Initialize DFA and run tests
dfa = ChatSlangDFA()
test_results = test_dfa(dfa, test_cases)

# Print test results
for sequence, result in test_results.items():
    print(f"Input: {sequence} -> Result: {result}")
