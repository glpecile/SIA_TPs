import random
from typing import List

from population.Element import Element
from population.Bag import Bag
from utils.Config import Config
# Selection algorithms

from selection.boltzmann import boltzmann
from selection.elite import elite
from selection.rank import rank
from selection.roulette import roulette
from selection.tournament import tournament
from selection.truncated import truncated

# Cross Over algorithms

from cross_over.multiple import multiple
from cross_over.simple import simple
from cross_over.uniform import uniform

from mutations.mutation import mutation

import sys

selection = {
    "boltzmann": boltzmann,
    "elite": elite,
    "rank": rank,
    "roulette": roulette,
    "tournament": tournament,
    "truncated": truncated
}

cross_over = {
    "multiple": multiple,
    "simple": simple,
    "uniform": uniform,
}

print('Argument List:', str(sys.argv))
assert len(sys.argv) == 3, 'Missing arguments'

config_file = open(sys.argv[2], 'r')
config: Config = Config(config_file.read())
config_file.close()

max_weight: int
total_items: int
elements: List[Element] = []

with open(sys.argv[1], 'r') as f:
    line = f.readline()
    count: int = 0

    while line:
        aux: List[str] = line.split()

        if count == 0:
            total_items = int(aux[0])
            max_weight = int(aux[1])
        else:
            aux: List[str] = line.split()
            element: Element = Element(int(aux[1]), int(aux[0]))
            elements.append(element)
        count += 1
        line = f.readline()

    f.close()

bag: Bag = Bag(max_weight, total_items, int(config.population), elements)

while True:  # TODO setear condiciones de corte
    new_gen: dict = dict()
    while len(new_gen) < bag.population:
        selected = random.sample([*bag.chromosomes.keys()], 2)
        uniform(selected)
        mutation(selected[0])
