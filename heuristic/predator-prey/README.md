# Lotka-Volterra Model

**Lotka-Volterra Model** or a **Wolves and Sheep** simulation. In this case, we would model the interactions between three entities:

- Wolves (predators)
- Sheep (prey)
= Pasture (resource for sheep to graze)

The basic idea is that wolves hunt sheep, and sheep graze on the pasture. Over time, populations of both wolves and sheep evolve based on their interaction, and the pasture regenerates as sheep eat it.

Here's a basic outline of how the simulation works:

- Sheep consume resources from the pasture and grow in population.
- Wolves consume sheep and grow in population.
- Pastures regenerate over time as sheep consume the grass.
- There are dynamics of birth, death, and eating that balance the populations.

Basic Rules:

- **Wolves** increase in number by consuming **sheep**, but they die if they don't find enough sheep to eat.
- **Sheep** increase in number by consuming the **pasture** (grass), but they die if there's no grass left.
- **Pasture** regenerates over time, providing food for the **sheep**.