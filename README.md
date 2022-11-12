# BostonHacks 2022

Alex Miller, Jared Pincus, Ruihang Liu


# Project

SMS-based game AI

Uses Twilio to communicate between player and AI.

Uses CockroachDB to store persistent game state for all players.

# Dependencies

Python: `stockfish`, `parse`


# Immediate goals

Read FEN-format user move input

Get it running locally

`help` text gives possible user commands

Choose at start of game to be white or black


# Optional goals

Display possible moves to user

More natural-ish language user commands

Prettier unicode/ascii boards
 - chess piece unicode symbols
 - display ranks/files
 - box around board

Get it running server-side

Change visuals based on if user is white or black

User chooses certain game settings
 - ELO rating

Deliberately add a delay to text response