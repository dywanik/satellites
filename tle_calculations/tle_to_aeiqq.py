import math
import sys

MU = 398600.4418  # km^3/s^2, standard gravitational parameter for Earth

def parse_tle(lines):
    line1 = lines[0].strip()
    line2 = lines[1].strip()
    
    inclination = float(line2[8:16])  # degrees
    eccentricity = float(f"0.{line2[26:33]}")
    mean_motion = float(line2[52:63])  # revs per day

    return {
        'i_deg': inclination,
        'e': eccentricity,
        'n': mean_motion
    }

def calc_orbital_elements(n, e):
    # convert n from rev/day to rad/s
    n_rad_s = n * 2 * math.pi / 86400
    a = (MU / (n_rad_s ** 2)) ** (1/3)
    q = a * (1 - e)
    Q = a * (1 + e)
    return a, q, Q

def process_tle_file(tle_file, output_file):
    with open(tle_file, 'r') as f:
        lines = [line for line in f if line.strip()]

    results = []

    for i in range(0, len(lines), 2):
        if i + 1 >= len(lines):
            break
        tle = parse_tle(lines[i:i+2])
        a, q, Q = calc_orbital_elements(tle['n'], tle['e'])
        results.append({
            'a': a,
            'e': tle['e'],
            'i': tle['i_deg'],
            'q': q,
            'Q': Q
        })

    with open(output_file, 'w') as f:
        for r in results:
            f.write(f"{r['a']:10.3f} {r['e']:10.7f} {r['i']:10.4f} {r['q']:10.3f} {r['Q']:10.3f}\n")

# --- Usage ---
# python tle_calc.py tle_clean.txt
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python tle_calc.py tle_clean.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = "aeiqq_from_tle_2013.txt"
    process_tle_file(input_file, output_file)
