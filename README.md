# Pokémon Pokédex

A Python-based interactive Pokémon Pokédex built using PokéAPI and Tkinter.

## About

Pokémon Pokédex is an interactive desktop application that lets users search for Pokémon and explore detailed information about them through a graphical user interface.

The Pokédex displays information such as:
- Pokémon number and name
- Type and abilities
- Base stats
- Height and weight
- Gender information
- Growth rate
- Catch rate and hatch information
- Pokémon description
- Evolution chains and evolution requirements
- Moves
- Weaknesses, resistances, and immunities
- Normal and shiny sprites
- Random Pokémon

The interface is inspired by the classic Pokémon Pokédex.

## How I Made It

I built this project using Python.

I used:

- Tkinter for the graphical user interface
- PokéAPI for Pokémon data
- Requests to communicate with the API
- Pillow to display Pokémon sprites
- PyInstaller to create the Windows executable

The main challenge was working with the API data and connecting it to the graphical interface. I also had to handle evolution chains, different Pokémon information, shiny sprites, and make the different features work together without breaking each other.

I spent time testing and debugging the application to make sure the different features worked correctly.

## How to Download and Run

### Windows Executable

The easiest way to run the Pokédex is to download the Windows executable.

1. Go to the Releases section of this repository.
2. Open the latest release.
3. Download `pokedex.exe`.
4. Run `pokedex.exe`.
5. Search for a Pokémon by name or Pokédex number.

No Python installation is required when using the executable.

### Run From Source

If you want to run the project from the source code:

1. Install Python.
2. Clone or download this repository.
3. Install the required dependencies:

```bash
pip install requests pillow
```

4. Run the program:

```bash
python pokedex.py
```

## Features

- Interactive Pokémon Pokédex
- Pokémon search
- Random Pokémon
- Detailed Pokémon information
- Evolution chains
- Evolution requirements
- Moves
- Type information
- Weaknesses, resistances, and immunities
- Normal and shiny sprites
- Graphical user interface

## Built With

- Python
- Tkinter
- PokéAPI
- Requests
- Pillow
- PyInstaller
