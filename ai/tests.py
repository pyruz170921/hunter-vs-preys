from ai.simulation import SimulationEngine

sim = SimulationEngine(
    8,
    "DIJKSTRA"
)

for turn in range(100):

    print(f"\n=== TURNO {turn+1} ===")

    sim.print_board()

    result = sim.step()

    alive = sum(
        1
        for prey in sim.preys
        if prey["alive"]
    )

    print(
        "Hunter:",
        sim.hunter
    )

    print(
        "Presas vivas:",
        alive
    )

    if not result:
        break
    
    print("\nESTADÍSTICAS")

print(
    "Tiempo:",
    sim.time_elapsed
)

print(
    "Movimientos cazador:",
    sim.hunter_moves
)

for prey in sim.preys:

    print(
        prey["id"],
        prey["alive"],
        prey["moves"],
        prey["survival_time"]
    )

print(
    "Movimientos cazador:",
    sim.hunter_moves
)

print()

for prey in sim.preys:

    print(
        prey
    )

sim.print_ranking()