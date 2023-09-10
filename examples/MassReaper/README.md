# Mass Reaper SC2MapAnalyzer example bot

Using the mass reaper example in [python-sc2](https://github.com/BurnySc2/python-sc2/blob/develop/examples/terran/mass_reaper.py) as a starting point, we use the pathing module in map_analyzer to improve the reaper micro. This is achieved by adding enemy influence to pathing grids to allow reapers micro a bit more precisely.

This example should work with the [Ai-Arena ladder](https://aiarena.net/) ladder using the following steps:

1. Choose a new name and give your bot some character!
2. Rename `MassReaper` references in this example to `YourBotName`
3. Copy `SC2MapAnalysis/map_analyzer` folder inside this folder since aiarena environment does not have MA installed
4. Copy the `sc2` folder from the [python-sc2](https://github.com/BurnySc2/python-sc2) repo and put it inside this folder. This step may be optional but ensures our bot ships with the latest version of `python-sc2`
5. Zip the entire folder, make sure all files are in the root folder
6. Create an account on https://aiarena.net/ and create a new bot
7. Upload the zip to aiarena and join competitions or request matches

See the ai-arena wiki for more information https://aiarena.net/wiki/bot-development/getting-started/#wiki-toc-python
