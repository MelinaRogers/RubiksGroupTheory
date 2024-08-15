# Rubik's Cube Group Theory Analysis

This project analyzes the group-theoretic properties of the Rubik's Cube using computational methods. It focuses on examining the distribution of permutation orders, cycle types, and orientation sums after applying random moves to a solved cube.

## Features

- Simulates a Rubik's Cube and applies random moves
- Analyzes permutation orders of scrambled cube states
- Examines corner and edge cycle type distributions
- Verifies orientation sum properties
- Generates visualizations of the results

## Requirements

- Python 3.7+
- Libraries: matplotlib, sympy

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/rubiks-cube-analysis.git
   cd rubiks-cube-analysis
   ```

2. Install required libraries:
   ```
   pip install matplotlib sympy
   ```

## Usage

Run the main analysis script:

```
python rubiks_corner_analyzer.py
```

This will perform the analysis and generate both console output and a visualization saved as `permutation_orders.png`.

## Output

The script produces:
1. Console output with detailed statistics on permutation orders, cycle types, and orientation sums
2. A bar chart (`permutation_orders.png`) showing the distribution of permutation orders
