## Chess-Data-Clean-up-and-Format-Tool
A tool designed to format and clean data downloaded from Kaggle (https://www.kaggle.com/ronakbadhe/chess-evaluations).
Data downloaded comprises of two parts, a set of chessboard layouts in FEN format (https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
and secondly a numerical evaluation for how good the boards positioning is for the current player. Board evaluation completed by Stockfish (One of the world's leading chess agents)
Formating breaks the FEN format into 6 channels, each representative of a 8x8 chess board for each respective piece type.
Allows for use within a convolutional neural network input format.
