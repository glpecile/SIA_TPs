from datetime import datetime
import os
import random
import sys
from typing import List

import matplotlib.pyplot as plt

# Cross Over algorithms
from cross_over.multiple import multiple
from cross_over.simple import simple
from cross_over.uniform import uniform
from mutations.mutation import mutation
from population.Bag import Bag
from population.Element import Element
# Selection algorithms
from selection.boltzmann import boltzmann
from selection.elite import elite
from selection.rank import rank
from selection.roulette import roulette
from selection.tournament import tournament
from selection.truncated import truncated
from utils.Config_ga import Config
from utils.Criteria import Criteria
from utils.Results_ga import Results
from utils.fitness import get_fitness
from utils.selection_parameters import SelectionParameter

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
assert len(sys.argv) == 4, 'Missing arguments'

output_dir = sys.argv[3]
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

initial_time = datetime.now()
config_file = open(sys.argv[2], 'r')
config: Config = Config(config_file.read())
config_file.close()
bag: Bag = Bag(max_weight, total_items, int(config.population), elements)

criteria: Criteria = Criteria(config, bag.chromosomes)
selection_parameters: SelectionParameter = SelectionParameter(config)

while not criteria.is_completed():
    new_gen: dict = dict()

    while len(new_gen) < bag.population:
        selected = random.sample([*bag.chromosomes.keys()], 2)
        children = cross_over[config.cross_over_algorithm](selected, config)

        for child in children:
            child = mutation(child, config.mutation_probability)
            if child not in new_gen and child not in bag.chromosomes:
                new_gen[child] = get_fitness(child, bag.elements, bag.max_weight)
            if len(new_gen) == bag.population:
                break

    union = new_gen | bag.chromosomes
    bag.chromosomes = selection[config.selection_algorithm](union, selection_parameters)
    selection_parameters.current_gen += 1
    bag.evolution[selection_parameters.current_gen] = max(bag.chromosomes.values())
    criteria.update_criteria(bag.chromosomes)

bag.chromosomes = dict(sorted(bag.chromosomes.items(), key=lambda item: item[1], reverse=True))
result: Results = Results(bag, config, initial_time)
# for chromosome in bag.chromosomes:
#     weight = 0
#     benefit = 0
#     for i, value in enumerate(chromosome):
#         weight += int(value) * elements[i].weight  # x_i * w_i
#         benefit += int(value) * elements[i].value  # x_i * b_i
#     print('Weight ' + weight.__str__() +
#           ' | Benefit ' + benefit.__str__())
weight = 0
benefit = 0
for i, value in enumerate(list(bag.chromosomes.keys())[0]):
    weight += int(value) * elements[i].weight  # x_i * w_i
    benefit += int(value) * elements[i].value  # x_i * b_i
print('+-------------------------------------------------------------+')
print('Population size: ' + result.config.population.__str__())
print('Generations quantity: ' + result.config.generations_quantity.__str__())
print('Time limit: ' + result.config.limit_time.__str__() + 's')
print('Mutation probability: ' + result.config.mutation_probability.__str__())
print('Algorithms: ' + result.config.__str__())
print('---------------------------------------------------------------')
print('Results:')
print('Time: ' + str(result.time))
print('Generation:' + selection_parameters.current_gen.__str__())
print('Weight: ' + weight.__str__())
print('Benefit: ' + benefit.__str__())
print('+-------------------------------------------------------------+')

plt.figure(figsize=(7, 7), layout='constrained', dpi=200)
plt.plot(bag.evolution.keys(), bag.evolution.values(), label=config.__str__())
plt.xlabel('Generación')
plt.ylabel('Fitness')
plt.title("Evolución en cada generación")
plt.grid(True)
plt.legend()
plt.savefig(output_dir + '/' + config.selection_algorithm + '_' + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png')
