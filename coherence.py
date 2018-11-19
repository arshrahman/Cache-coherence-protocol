import sys
from simulation import Simulation

if len(sys.argv) != 6:
    print("Wrong number of arguments, usage:")
    print("python coherence.py 'protocol' 'input_file' 'cache_size' 'associativity' 'block_size'")
    sys.exit(2)

protocol, input_file, cache_size, associativity, block_size = sys.argv[1:]
print('protocol:', protocol, 'input_file:', input_file, 'cache_size:', cache_size, 'associativity:', associativity, 'block_size:', block_size)

simulation = Simulation(protocol, input_file, int(cache_size), int(associativity), int(block_size))
simulation.execute()
simulation.results()
