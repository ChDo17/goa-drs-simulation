from config import load_assumptions

assumptions = load_assumptions()

def run_simulation(rvm_count, truck_capacity=None, pickup_frequency=1):
    # Load assumptions
    bottles_per_rvm_per_day = 120  # You could also move this to assumptions.json later
    vehicle_config = assumptions['vehicle']

    # If truck_capacity not passed, use default from config
    if not truck_capacity:
        truck_capacity = vehicle_config['capacity_kg'] * (vehicle_config['utilization_percent'] / 100)

    total_bottles = rvm_count * bottles_per_rvm_per_day * pickup_frequency

    trips_required = int(total_bottles // truck_capacity) + 1

    # Cost per km = diesel_price / mileage
    cost_per_km = vehicle_config['diesel_cost_per_litre'] / vehicle_config['mileage_kmpl']

    return {
        'bottles_collected': int(total_bottles),
        'trips_required': trips_required,
        'truck_capacity_effective': int(truck_capacity),
        'cost_per_km': round(cost_per_km, 2)
    }
