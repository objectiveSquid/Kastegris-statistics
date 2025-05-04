# Kastegris statistics
With this repository I hope to find the optimial playing strategy for the game **<i>Kastegris</i>** also known as **<i>Pass the pigs</i>**.
So far I've come to the conclusion that you should when after getting over around 25 points in a round for optimal results.

## Symbols in the datasets
- **\---** (3 dashes) = reset score to 0<br>
- **\-** (1 dash) = lost round<br>
- Anything else is a point increase

## Format of the datasets
- Each new symbol must be on a seperate line
- All whitespace ignored (including empty lines)
- If a line starts with #, it will be ignored.
**Example dataset:**
```
5
20
1
-
5
---
1
10
```