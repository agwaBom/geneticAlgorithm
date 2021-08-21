import random
from numpy import exp

# complete the genetic algorithm
# 1. generate initial 100 individuals
# 2. reproduce(x, y) for 100 individuals (create child from the parent x, y)
# 3. mutate within a small probabilty
# 4. repeat N generations of until the target string is generated.

geneSet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,!?~ "
target = "MinJun is babo"

def softmax(vector):
	e = exp(vector)
	return e / e.sum()

def gen_individual(length):
    gene = []
    while len(gene) < length:
        sampleSize = min(length-len(gene), len(geneSet))
        gene.extend(random.sample(geneSet, sampleSize))
    return ''.join(gene)

def get_population(length, population_length):
    gene_list = []
    for _ in range(population_length):
        gene_list.append(gen_individual(length))
    return gene_list

def reproduce(x, y):
    # input two string and slice them to make a new child string
    string_length = len(x)
    c = random.randint(0, string_length)
    child_1 = x[0:c]+y[c:string_length]
    child_2 = y[0:c]+x[c:string_length]
    return child_1, child_2

def get_fitness(guess, target):
    return sum(1 for expected, actual in zip(target, guess) if expected==actual)

def mutate(parent):
    index = random.randrange(0, len(parent))
    childGenes = list(parent)
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    return "".join(childGenes)

def randomSelection(population, target):
    fitness_list = [get_fitness(gene, target) for gene in population]
    probability = softmax(fitness_list)*100
    random_selected = random.choices(population, weights=probability, k=len(population)//2)
    return random_selected

population_length = 50
initial_population = get_population(len(target), population_length)

def genetic_algorithm(population, target):
    count = 0 
    n_correct = 0
    while True:
        print(f"\n### {count} Attempt ###")
        new_population = []
        parent_x = randomSelection(population, target)
        parent_y = randomSelection(population, target)
        for x, y in zip(parent_x, parent_y):
            child_1, child_2 = reproduce(x, y) # crossover
            # 2% chance to mutation
            if 1 == random.randint(0, 50): child_1 = mutate(child_1)
            if 1 == random.randint(0, 50): child_2 = mutate(child_2)

            new_population.append(child_1)
            new_population.append(child_2)
        print(new_population)
        if count == 20000:
            break
        for pop in new_population:
            if pop == target:
                n_correct +=1
            if n_correct >= 50:
                return new_population
        
        count += 1
        population = new_population

genetic_algorithm(initial_population, target)