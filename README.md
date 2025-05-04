# Kastegris statistics
With this repository I hope to find the optimial playing strategy for the game **<i>Kastegris</i>** also known as **<i>Pass the pigs</i>**.
Currently this repository does not take into account the extended rules of the game.

## Symbols in the datasets
- **\-----** (5 dashes) = instant loss<br>
- **\---** (3 dashes) = reset score to 0<br>
- **\-** (1 dash) = lost round<br>
- Anything else is a point increase

## Format of the datasets
- Each new symbol must be on a seperate line
- All whitespace ignored (including empty lines)
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