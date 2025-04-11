# 🛰️ TLE Orbital Element Processing & Visualization

This project provides a set of Python scripts to:
- Clean and parse Two-Line Element (TLE) satellite data
- Calculate key orbital elements: semi-major axis `a`, eccentricity `e`, inclination `i`, perigee `q`, and apogee `Q`
- Save orbital data to file in raw text format
- Generate histograms for each orbital element with optional filtering and interactivity

NOTE:
It is advisable to use Python's venv when installing and ussing the tools:
```
source venv/bin/activate
```
---

## 📂 Components

### 1. `tle_calc.py`
Processes a cleaned TLE file and outputs calculated orbital elements.

#### 🧮 What it does:
- Parses TLE lines to extract mean motion, eccentricity, and inclination
- Computes:
  - Semi-major axis `a`
  - Perigee `q`
  - Apogee `Q`
- Outputs raw data in space-separated text format.

#### ✅ Usage:
```bash
python tle_calc.py tle_clean.txt
```
Output: `aeiqq_from_tle_2013.txt`

---

### 2. `plot_histograms.py`
Plots histograms from the output file of orbital elements.

#### 📊 Features:
- Plots all or individual elements: `a`, `e`, `i`, `q`, or `Q`
- Optional filters for min/max value and number of bins
- Interactive: press `q` while viewing any plot to quit the script

#### ✅ Usage:
```bash
python plot_histograms.py              # Plot all
python plot_histograms.py a            # Plot 'a'
python plot_histograms.py e 0.01 0.03  # Plot 'e' between 0.01 and 0.03
python plot_histograms.py q 300        # Plot perigee > 300 km
```

---

### 3. `clean_tle_file()`
Utility function to extract only line 1 and 2 of each TLE set (discarding names). Also, cleans up empty and erroneous lines.

```python
clean_tle_file('tle_2013.txt', 'tle_2013_clean.txt')
```

---

## 🔧 Requirements

- Python 3.7+
- `matplotlib`

Install with:

```bash
pip install matplotlib
```

---

## 📁 Input/Output Format

### Input TLE Format:
```
1 25544U 98067A   ...
2 25544  51.6416  ...
```

### Output file format (space-separated):
```
a        e         i       q       Q
6782.451 0.0002170 51.6420 6781.972 6782.930
...
```

---

## 📌 Notes
- TLE file must be pre-cleaned to contain only lines starting with `1` or `2`
- This tool is ideal for visualizing historical or simulated orbital catalogs

