# 🛰️ Starlink Orbit Animator

This Python script visualizes **Starlink satellite orbits around Earth** in **3D**, based on real TLE (Two-Line Element) orbital data. It simulates **satellite motion**, **ground tracks**, and **Earth's rotation**, giving you a dynamic view of orbital coverage and constellation behavior.

---

## 🎥 Features

- 🌍 Realistic 3D Earth with animated Starlink satellite orbits  
- 🛰️ Accurate satellite motion based on orbital elements (TLEs)  
- 🟠 Dynamic ground tracks showing sub-satellite points  
- 🔁 Earth rotation (sidereal day) synced to satellite movement  
- 🎛️ Interactive keyboard controls:
  - `T` – toggle ground trails on/off  
  - `↑` – increase animation speed  
  - `↓` – decrease animation speed  

---

## 📦 Requirements

- Python 3.7+
- `matplotlib`
- `numpy`

Install with:

```bash
pip install matplotlib numpy
```

---

## 📂 Usage

1. Download Starlink TLE data from [Celestrak](https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle)
2. Save it as `tle.txt` in the same directory
3. Run the script:

```bash
python animate_starlink_orbits.py
```

---

## 🎯 Roadmap

Future ideas:
- Add ground stations and visibility simulation  
- Export animations as GIF or MP4  
- 2D map projection of ground tracks  
- User-defined satellite filtering  

---

## 📸 Preview

_(Insert screenshot or GIF of animation here)_
