import re

# Stringa di esempio
text = "RFQ Outright [CANDEAL/BOND] [1010725045000009]"

# Pattern regex come raw string
pattern = r"RFQ Outright \[CANDEAL\/BOND\] \[\d+\]"

# Verifica se la stringa corrisponde al pattern
if re.match(pattern, text):
    print("La stringa corrisponde al pattern.")
else:
    print("La stringa NON corrisponde al pattern.")