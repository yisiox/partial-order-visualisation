"""
Main program of partial order relations visualisation.

@author yisiox
@version September 2022
"""

from helper import *

Z_plus = list(range(1, 11))
divides = lambda x, y: y % x == 0
less_than_eq = lambda x, y: x <= y

def main():
    
    G = generate_graph(Z_plus, less_than_eq)

    if check_partial_order(G):
        G = generate_hasse_diagram(G)
        print_info(G)
        display_hasse_diagram(G)

if __name__ == "__main__":
    main()
