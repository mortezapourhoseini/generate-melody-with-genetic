import numpy as np
from midiutil import MIDIFile
from genetic_algorithm import GeneticAlgorithm

# Musical configuration
NOTES_IN_SCALE = [60, 62, 64, 65, 67, 69, 71, 72]  # C Major scale (MIDI numbers)
DURATIONS = [0.25, 0.5, 1.0]  # Quarter, half, whole notes
MELODY_LENGTH = 8  # 8-note phrases

class MusicGA(GeneticAlgorithm):
    def __init__(self, *args, **kwargs):
        custom_bounds = []
        for i in range(MELODY_LENGTH * 2):
            if i % 2 == 0:
                custom_bounds.append((min(NOTES_IN_SCALE), max(NOTES_IN_SCALE)))
            else:
                custom_bounds.append((min(DURATIONS), max(DURATIONS)))
        super().__init__(*args, bounds=custom_bounds, **kwargs)

    def mutate(self, individual):
        mutated = individual.copy()
        for i in range(0, len(mutated), 2):
            if np.random.rand() < self.mutation_rate:
                mutated[i] = np.random.choice(NOTES_IN_SCALE)
            if np.random.rand() < self.mutation_rate and i+1 < len(mutated):
                mutated[i+1] = np.random.choice(DURATIONS)
        return mutated

    def crossover(self, parent1, parent2):
        if self.crossover_method == 'musical':
            crossover_point = np.random.choice([4, 8, 12])
            return (
                parent1[:crossover_point] + parent2[crossover_point:],
                parent2[:crossover_point] + parent1[crossover_point:]
            )
        return super().crossover(parent1, parent2)

def melody_fitness(individual):
    score = 0
    
    # Validate note sequence
    notes = individual[::2]
    durations = individual[1::2]
    
    # Scale alignment
    valid_notes = sum(n in NOTES_IN_SCALE for n in notes)
    score += valid_notes * 2
    
    # Interval analysis
    intervals = np.abs(np.diff(notes))
    smooth_intervals = sum(1 for i in intervals if i <= 2)
    score += smooth_intervals * 3
    
    # Rhythm diversity
    unique_durations = len(set(durations))
    score += unique_durations * 2
    
    # Motif penalty
    motifs = [tuple(individual[i:i+4]) for i in range(0, len(individual), 4)]
    motif_penalty = (len(motifs) - len(set(motifs))) * 3
    score -= motif_penalty
    
    return max(score, 0)

def create_midi(melody, filename="output.mid"):
    midi = MIDIFile(1)
    midi.addTempo(0, 0, 120)
    
    time = 0
    for i in range(0, len(melody), 2):
        note = int(round(melody[i]))
        duration = melody[i+1]
        midi.addNote(0, 0, note, time, duration, 100)
        time += duration
    
    with open(filename, "wb") as f:
        midi.writeFile(f)

if __name__ == "__main__":
    ga = MusicGA(
        population_size=100,
        chromosome_length=MELODY_LENGTH*2,
        gene_type='real',
        fitness_func=melody_fitness,
        selection_method='tournament',
        crossover_method='musical',
        mutation_rate=0.15,
        elitism_ratio=0.1,
        termination_condition={'max_generations': 50}
    )

    best_melody, fitness_history = ga.run()
    create_midi(best_melody)
    
    print(f"Best melody MIDI notes: {best_melody[::2]}")
    print(f"Rhythm durations: {best_melody[1::2]}")
