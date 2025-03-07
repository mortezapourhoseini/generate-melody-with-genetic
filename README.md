# MelodyGen 🎵

MelodyGen is a Python-based melody generation system using Genetic Algorithms. It creates musical phrases by evolving populations of melodies based on musical fitness criteria.

## Features

- 🎼 **Musical Encoding**: Represents melodies as sequences of MIDI notes and durations
- 🧬 **Evolutionary Operators**: Custom crossover and mutation for musical phrases
- 🎹 **Scale Awareness**: Generates melodies in specified musical scales (default: C Major)
- 🎧 **MIDI Output**: Exports generated melodies as playable MIDI files
- 📊 **Fitness Evaluation**: Scores melodies based on musicality, smoothness, and rhythm

## Dependencies

- [NumPy](https://numpy.org/)
- [MIDIUtil](https://midiutil.readthedocs.io/)
- [Genetic Algorithm Framework](https://github.com/mortezapourhoseini/genetic-algorithm)

## Installation


1. Clone genetic-algorithm repository:
   ```bash
   git clone https://github.com/mortezapourhoseini/genetic-algorithm.git
   cd genetic-algorithm
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/mortezapourhoseini/melodygen.git
   cd melodygen
   ```
   
3. Run the melody generator:
   ```bash
   python melodygen.py
   ```

## Usage

### Basic Example
```python
from melodygen import MusicGA, create_midi

ga = MusicGA(
    population_size=100,
    chromosome_length=16,  # 8-note phrases
    gene_type='real',
    fitness_func=melody_fitness,
    mutation_rate=0.15,
    termination_condition={'max_generations': 50}
)

best_melody, _ = ga.run()
create_midi(best_melody, "my_melody.mid")
```

### Customization
- **Change Scale**: Modify `NOTES_IN_SCALE` in `melodygen.py`
- **Adjust Fitness**: Edit `melody_fitness` function
- **Output Format**: MIDI files can be imported into any DAW



