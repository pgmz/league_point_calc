# League Point Calculator

This is a cli Python application, that recieves game results and returns the leaderboard


## Usage

```bash

# input form a file
python leaguepointcalc -f matchEntries.txt
python leaguepointcalc --file matchEntries.txt

# input from named parameters
python leaguepointcalc -m "Lions 3, Snakes 3" -m "Tarantulas 1, FC Awesome 0"
python leaguepointcalc --match "Lions 3, Snakes 3" --match "Tarantulas 1, FC Awesome 0"

# input from parameters
python leaguepointcalc "Lions 3, Snakes 3" "Tarantulas 1, FC Awesome 0"

#input from stdin
python leaguepointcalc
Please enter game entries in format 'team name points, team name points' (Example: Lions 3, Snakes 3)
Write done, to finish game input
Lions 3, Snakes 3
Tarantulas 1, FC Awesome 0
```

## Example

```bash

python leaguepointcalc "Lions 3, Snakes 3" "Tarantulas 1, FC Awesome 0" "Lions 1, FC Awesome 1" "Tarantulas 3, Snakes 1" "Lions 4, Grouches 0"
1. Tarantulas, 6  pts
2. Lions, 5  pts
3. FC Awesome, 1  pts
3. Snakes, 1  pts
5. Grouches, 0  pts
```