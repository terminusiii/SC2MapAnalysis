# SC2MapAnalysis

* [Changelog](https://github.com/spudde123/SC2MapAnalysis/blob/master/CHANGELOG.md)
* ![](https://img.shields.io/badge/Documentation-latest-green?style=plastic&logo=appveyor)
   [Documentation](https://eladyaniv01.github.io/SC2MapAnalysis/)
   
## Summary

A plugin for Python SC2 API [BurnySc2](https://github.com/BurnySc2/python-sc2/)


## Why Do we need this ? 


This module is inspired by plays like this one [TY map positioning](https://www.youtube.com/watch?v=NUQsAWIBTSk&start=458)
(notice how the army splits into groups, covering different areas,  tanks are tucked in corners, and so on) 

Hopefully with the interface provided here, you will be able to build plays like that one!

Thanks A lot to [DrInfy](https://github.com/DrInfy) for solving one of the biggest challenges,  finding rare choke points.

Check out his work 

* [Sharpy](https://github.com/DrInfy/sharpy-sc2) for rapid bot development.

* [sc2pathlib](https://github.com/DrInfy/sc2-pathlib)  a high performance rust module with python interface for pathfinding 


More Examples reside in the [Documentation](https://eladyaniv01.github.io/SC2MapAnalysis/)

See [here](./examples/MassReaper/README.md) for an example `map_analyzer` reaper bot showing pathing and influence in action.

Example:
```python
import pickle
import lzma
from map_analyzer import MapData
from map_analyzer.utils import import_bot_instance

#if its from BurnySc2 it is compressed
# https://github.com/BurnySc2/python-sc2/tree/develop/test/pickle_data
YOUR_FILE_PATH = 'some_directory/map_file'
with lzma.open(YOUR_FILE_PATH, "rb") as f:
    raw_game_data, raw_game_info, raw_observation = pickle.load(f)

# mocking a bot object to initalize the map,  this is for when you want to do this while not in a game,  
# if you want to use it in a game just pass in the bot object like shown below 

bot = import_bot_instance(raw_game_data, raw_game_info, raw_observation)


# And then you can instantiate a MapData Object like so
map_data = MapData(bot)


# plot the entire labeled map
map_data.plot_map()

# red dots or X are vision blockers,
# ramps are marked with white dots 
# ramp top center is marked with '^'
# gas geysers are yellow spades 
# MDRampss are marked with R<region_label>
# height span is with respect to :   light = high , dark = low
# ChokeArea is marked with green heart suites
# Corners are marked with a red 'V' 
```
<img src="https://user-images.githubusercontent.com/40754127/88463402-3fa1dc80-cebb-11ea-9da9-f80a219f1083.png"/>


Tested Maps ( [AiArena](https://www.sc2ai.com/) ) : See `map_analyzer/pickle_game_info` for all tested maps.

# Getting Started

## Bot Authors

If you already have a [BurnySc2](https://github.com/BurnySc2/python-sc2/) development environment setup, you're likely 
equipped with all the necessary dependencies Therefore, integrating map_analyzer into your existing bot is a 
straightforward process requiring just a few simple steps.

If you're a new bot author, please set up a new [BurnySc2](https://github.com/BurnySc2/python-sc2/) bot development 
environment before installing `map_analyzer`.

### Installation

1. Clone or download this repo
2. Copy the `map_analyzer` directory and place it in the root of your bot directory:

```
MyBot
├── map_analyzer
│ ├── … dependencies for map_analyzer
│ … your other bot files and folders here
```

3. map_analyzer relies on a pathing extension written in C, this can be built locally or downloaded from github actions.
If you're on a debian based OS you may be able to skip this step as the repo contains a linux binary already included
in the `map_analyzer` folder. <br><br>
<b>Method 1: Without needing C++ build tools</b> <br><br>
Check the most recent [BuildCExtension](https://github.com/spudde123/SC2MapAnalysis/actions/workflows/build_c_extension.yml)
Github Action workflow. Then scroll to the bottom to download the artifact for your OS:
![c_workflow](https://github.com/spudde123/SC2MapAnalysis/assets/63355562/65e08208-8f82-44ee-bf84-3b79d1271d76)
<br>
Download the artifact and copy the binary to `MyBot/map_analyzer/cext/` <br><br>
<b>Method 2: Build the project locally</b><br>
If you're on Windows, make sure [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) 
are installed before proceeding, then:
- Install [Poetry](https://python-poetry.org/) for example: `pip install poetry`
- In the root folder of this repo run the following:
`poetry install`
<br><br>
If successful this will compile a binary in the build directory, for example:
`SC2MapAnalysis\build\lib.win-amd64-cpython-311\mapanalyzerext.cp311-win_amd64.pyd`
<br>
Copy this binary to `MyBot/map_analyzer/cext/mapanalyzerext.cp311-win_amd64.pyd`


4. In your bot initiate the `map_analyzer` module:
```python
from map_analyzer import MapData
from sc2.bot_ai import BotAI

class MyBot(BotAI):
    map_data: MapData

    async def on_start(self) -> None:
        self.map_data = MapData(self)

    async def on_step(self, iteration: int):
        pass
```

5. Uploading to [AiArena](https://ai-arena.net/) and tournaments - <br>
No further setup is required, just include the `map_analyzer` folder in your bot zip.


## Contributors or to run examples

If you're interested in contributing or would like to run tests then the full dev environment should be setup:
1. Install [Poetry](https://python-poetry.org/) for example: `pip install poetry`
2. `poetry install --with dev` - This will install all development dependencies, build the C extension 
and create a new environment. 
Useful poetry environment commands: <br>
`poetry env list --full-path -` - Use this to configure your IDE to recognise the environment <br>
`poetry env remove <env_name>` <br>
`poetry shell`
3. Check your environment is working by running the example bot: <br>
`poetry run examples/MassReaper/run.py`

### Run tests
(github workflow to check this on PR)

`poetry run pytest`

### Autoformatters and linting
(github workflow to check these on PR)

`poetry run black .`

`poetry run isort .`

`poetry run flake8 .`

### Contributing
To faciliatate automated releases, [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) guideline should be followed.
Example git commits:

Feature:
`feat: find path with multiple grids`

Bugfix:
`fix: correct weight cost on cliff`

Pull request titles should follow these guidelines too, this enables the automatic release and changelogs to work.
There is a github workflow to enforce this. 

Example PR title:

`feat: find path with multiple grids`





