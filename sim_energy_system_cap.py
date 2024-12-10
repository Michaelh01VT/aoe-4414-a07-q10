# sim_energy_system_cap.py
#
# Usage: python3 sim_energy_system_cap.py sa_m2 eff voc c_f r_esr q0_c p_on_w v_thresh dt_s dur_s
#
# Simulates a capacitor-based energy system
#
# Parameters:
# sa_m2: Area of the solar array m^2
# eff: Efficiency of solar array 
# voc: Open-circuit voltage V
# c_f: Capacitance F
# r_esr: Equivalent series resistance of the capacitor Ohm
# q0_c: Initial charge on the capacitor Coulombs
# p_on_w: Power consumption W
# v_thresh: Voltage threshold V
# dt_s: Simulation time step s
# dur_s: Total simulation duration seconds
#
# Output:
# Logs each (time, voltage) pair to a CSV file.
# Written by Michael Hoffman
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

import sys  # For command-line arguments
import csv  # For CSV output

# Helper function to calculate solar power input
def solar_power_input(sa_m2, eff, voc):
    return sa_m2 * eff * voc  

def simulate(sa_m2, eff, voc, c_f, r_esr, q0_c, p_on_w, v_thresh, dt_s, dur_s):
    time = 0.0  
    voltage = q0_c / c_f  
    log = []

    total_steps = int(dur_s / dt_s)

    # Run the simulation loop
    for step in range(total_steps):
        solar_input = solar_power_input(sa_m2, eff, voc)  

        net_power = solar_input - p_on_w

        charge_change = net_power * dt_s  
        q0_c += charge_change
        voltage = q0_c / c_f  

        if voltage < v_thresh:
            voltage = 0.0
            print(f"Voltage dropped below threshold at {time} seconds")
            break

        time += dt_s
        log.append((time, voltage))

    with open('./log.csv', mode='w', newline='') as outfile:
        csvwriter = csv.writer(outfile)
        csvwriter.writerow(['t_s', 'volts'])
        for e in log:
            csvwriter.writerow(e)

# Parse script arguments
if len(sys.argv) == 11:
    sa_m2 = float(sys.argv[1])
    eff = float(sys.argv[2])
    voc = float(sys.argv[3])
    c_f = float(sys.argv[4])
    r_esr = float(sys.argv[5])
    q0_c = float(sys.argv[6])
    p_on_w = float(sys.argv[7])
    v_thresh = float(sys.argv[8])
    dt_s = float(sys.argv[9])
    dur_s = float(sys.argv[10])

    simulate(sa_m2, eff, voc, c_f, r_esr, q0_c, p_on_w, v_thresh, dt_s, dur_s)
