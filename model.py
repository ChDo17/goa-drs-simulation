def run_simulation(rvm_count, truck_capacity, pickup_frequency):
    bottles_per_rvm_per_day = 120
    total_bottles = rvm_count * bottles_per_rvm_per_day * pickup_frequency
    trips_required = (total_bottles // truck_capacity) + 1

    return {
        'bottles_collected': total_bottles,
        'trips_required': trips_required
    }
