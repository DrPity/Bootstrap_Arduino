## Bootstrap Arduino

Simple and quick Python script to set up an Arduino project with Platformio.

### Core Features:
- Adding common helper classes
- MAPPING file for global #defines
- Debug print for easy on/off debug logging
- Checks for Platformio as dependency and if necessary installs it via Homebrew.

---

### Optional Features:
- Add serial communication
- Set up Neopixel library and custom wrapper for quick light prototypes. [currently mainly used for LED-strips]
- Setting up custom timers
- Make it a Git project

---

## Getting started
- Get the repository: `git clone https://github.com/DrPity/`
- Run script: `python bootstrap.py -d path/to/your/directory`

## Optional arguments:
- `-h, --help` show this help message and exit
- `--directory DIRECTORY, -d DIRECTORY` path to directory [default = dist]
