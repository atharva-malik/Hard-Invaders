# Hard Invaders

This is a clone of the popular arcade game Space Invaders, but with a modern twist. Made using PyGame, this project's heavy focus on the object-oriented programming paradigm really sets this project apart, making sure that it is easy to modify and reuse blocks of code.

## Features

- Multiple enemies:
  - Rare (Green): Dies in one shot and shoots dull yellow bullets
  - Epic (Yellow): Dies in two shots and shoots bright orange bullets
  - Mythic (Red): Dies in three shots and shoots bright red bullets
  - Legendary (Blue): Dies in one shot and shoots three bright blue bullets
- Thoroughly commented and easily editable python code 
- Comes with an executable file (Tested for Windows 11, 64 bit processor)
- Comes with basic menu, victory, and defeat screens
- Procedural enemy generation, getting harder over time
- Fully random enemy generation, ensuring a fun, new experience every time
- Ensures that enemies generate in formation, with rarer enemies generating higher up, and closer to the middle.
- Background music to help you concentrate in-game
- Background sound effects

## Technologies Used

This PyGame application uses 2 main technologies on the front end, [Python 3.10] and the [PyGame] module, but uses lots of different technologies in the background like the random module (to generate enemies and choose which enemy shoots) and [PyInstaller] module (to create a fully functioning executable)


## Installation

Install the repository and the following packages and you are good to go!
```sh
pip install pygame==2.5.2
```

## Execution
To run the script, navigate to the directory of installation and open the directory in the terminal. Then type:
```sh
py -3 main.py
```
## Controls
[A] / [Left Arrow]: Move Left

[D] / [Right Arrow]: Move Right

[Space]: To shoot

Click on the text in the menus to navigate

## Development


Want to contribute? Great! Pull requests and issues are welcome! [Here] is an excellent guide on how to create pull requests and forks to request changes. I suggest using the addon "Better Comments" on Visual Studio Code as it makes the comments more readable and I have used it throughout the code.

## Credits
Music and Sprites from [OpenGameArt]

Button.py code from [BaralTech]

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job.)

   [PyGame]: <https://www.pygame.org/>
   [OpenGameArt]: <https://opengameart.org/>
   [BaralTech]: <https://github.com/baraltech/>
   [PyInstaller]: <https://pyinstaller.org/>
   [Python 3.10]: <https://www.python.org/downloads/release/python-3109/>
   [Here]: <https://www.dataschool.io/how-to-contribute-on-github/>
