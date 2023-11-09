# pygame-chess
A simple interactive Chess game written using pygame and python-chess. 

# Usage
- It is precisely recommended to install all necessary libraries: `pip3 install chess pygame stockfish`
- The game is powered by [Stockfish](https://stockfishchess.org/). In the source file, initialize the path to the Stockfish binary file. 
```python
# Initialize Stockfish
try:
   stockfish = Stockfish(path="PATH TO STOCKFISH BINARY")
   stockfish_elo = 800
   stockfish_elo = input("Input Stockfish ELO (Default is 800): ")
   # stockfish.update_engine_parameters({"Minimum Thinking Time": 0})
   stockfish.set_elo_rating(stockfish_elo)
except: 
   print("Stockfish path is incorrect")
```
- To run the game: ```python3 pygame-chess.py```

