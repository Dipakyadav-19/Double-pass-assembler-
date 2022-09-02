# Double-pass-assembler-
 Two pass assembler does two passes over the source file. In first pass, all it does is looks for label definitions and introduces them in the symbol table (a dynamic table which includes the label name and address for each label in the source program)
 
# Algorithm Design
In our design of a Two-pass assembler, we are interested in generating machine codes from a given set of assembly language codes. Tasks performed by the assembler in  pass 1 is:

# Pass 1 – Define symbols and literals.

The length of machine instructions would be determined.
The track of location counter (LC) would be kept.
Symbol values must be remembered until pass 2.
Some pseudo-ops, if present in the card, would be processed.
The literals, if present in the card, would be remembered.

# Pass 1 Database

Input source program.
A Location Counter for keeping the track of instruction’s location.
A Machine Operation Table for indicating the symbolic mnemonic for each instruction and its length.
A Pseudo-Operation table for indicating the symbolic mnemonic for each pseudo-op in Pass 1.
A Symbol Table to store label and its value.
A Literal Table to store literal and assigned location.
A copy of input source file to be used in pass 2 can be stored as a File pointer.
