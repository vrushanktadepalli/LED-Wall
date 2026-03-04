# Raspberry Pi Zero 2 W LED Wall

A Python-based LED wall controller for the **Raspberry Pi Zero 2 W** using **WS2811 LEDs**.
This project allows a 32×16 LED matrix to display **images, GIFs, videos, and scrolling text**.

The system is designed to be simple: place media files in the appropriate folder and call the corresponding function.

---

## Features

* Display **images**
* Play **GIF animations**
* Play **videos**
* Show **text / scrolling patterns**
* Adjustable LED brightness
* Easily changeable **matrix size**

---

## Hardware

Controller:

* Raspberry Pi Zero 2 W

LED Matrix:

* WS2811 compatible LEDs
* Default size: **32 × 16** (configurable)

GPIO:

* **GPIO 12** used for LED data

Power:

* External 5V power supply recommended for the LED matrix

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/vrushanktadepalli/LED-Wall.git
cd LED-Wall
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

## Project Structure

```
assets/
  gifs/
  images/
  videos/

utils/
  gifs_show.py
  images_show.py
  videos_show.py

env.py
main.py
```

### Folder purpose

**assets/**
Contains all media files displayed on the LED wall.

```
assets/gifs    → GIF animations
assets/images  → Static images
assets/videos  → Video files
```

**utils/**
Contains rendering logic for displaying media on the LED matrix.

**env.py**
Hardware configuration and helper functions.

**main.py**
Example script showing how to use the display functions.

---

## Usage

1. Place your media files in the correct folder:

```
assets/images/
assets/gifs/
assets/videos/
```

2. Call the appropriate function in your Python script.

Example:

```python
from utils.gifs_show import display_gif

display_gif("example.gif")
```

The program will render the content directly onto the LED wall.

---

## Configuration

Matrix size and hardware settings can be changed in:

```
env.py
```

Example settings:

```
WIDTH = 32
HEIGHT = 16
LED_PIN = 12
```

Adjust these values if using a different matrix size.

---
## Running the Project

Because the LED driver uses low-level Raspberry Pi hardware access, the program must be run with **sudo**.

Example:

```bash
sudo python main.py
```

Running without `sudo` may result in the LED strip failing to initialize.

This requirement comes from the `rpi_ws281x` library which uses PWM/DMA hardware on the Raspberry Pi to generate precise LED timing.

---
## Notes

* Ensure the LED matrix has a **stable external power supply**.
* Large video files may reduce performance on lower-end hardware.

---

## Future Improvements

Possible future additions:

* Web interface for control
* Faster Video/Gif rendering
* Additional animation patterns

---

## Author

Project created for controlling a Raspberry Pi based LED wall display.
