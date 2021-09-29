# How to use AoE2ScenarioStringEditor

AoE2ScenarioStringEditor is a ready-to-use application and doesn't need you to install any kind of additional software
in order to run.

## File Menu

- Open [Ctrl+O]: Opens and reads an `aoe2scenario` scenario file
- Reload [Ctrl+R]: Discards the changes made by the user and reloads the strings from the scenario file
- Save [Ctrl+S]: Writes the changes to the scenario file
- Save as [Ctrl+Alt+S]: Writes the scenario file to a desired location
- Exit [Ctrl+Q]: Quits the program

## General tab

In the General tab you can edit the internal file name of the scenario. It will be displayed in the in-game scenario
editor interface as well as on the scenario selection screen when there is no explicit scenario name in *_layout.json.

## Players tab

Here you can change the names of the players (civilizations) which will be displayed on the in-game overlay.

## Messages tab

Just like in the in-game editor you can select and change the "Messages" of the scenario (Scenario Instructions, Hints,
Victory, Loss, History, Scout).

## Triggers tab

On the left side there is a list of all triggers that contain texts (objectives, rename unit effects, display
instructions effects, etc.). You can edit those texts by selecting them in the list and changing the content in the
textfield on the right side.

## Raw tab

This is probably the most useful of all tabs. It contains all the text displayed on the previous tabs. Each individual
line represents one entry.

- line 1-8 player names
- line 9-14 messages (Scenario Instructions, Hints, Victory, Loss, History, Scout)
- line 15-End triggers

With the "Apply" button the content of the textfield will be loaded in the respective entries on the other tabs. This is
especially useful if you want to translate the scenario. It is very important to keep empty lines as well as the new
line characters (\n) in order to apply the text content correctly!