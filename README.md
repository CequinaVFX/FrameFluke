# Frame Fluke
> <p>FrameFluke is a Python tool for Nuke that simplifies the process of rendering frames from any part of your script based on custom settings. It provides an easy way to create render breakdowns for your Nuke projects.</p>

## Features
+ Render frames from a selected node in Nuke.
+ Customizable settings using a JSON file.
+ Automatically creates folders and filenames based on frame number and node name.
+ Supports various image file formats (e.g., PNG, EXR, TGA, TIFF, JPG).
+ Integrates into the Nuke interface with a custom menu and shortcut.

## installation
Download the FrameFluke repository, rename the downloaded folder to ***FrameFluke*** and move it into your .nuke folder.

Add the following line to your init.py file, which is typically located in your .nuke folder:
```bash
nuke.pluginAddPath('./FrameFluke')
```
[Locating the default .nuke directory](https://support.foundry.com/hc/en-us/articles/207271649-Q100048-Nuke-Directory-Locations)

## Usage
1. Ensure your Nuke script is saved.
2. Select a single node (excluding Viewer nodes) in your Nuke script.
3. Run the script using the assigned shortcut.

## Custom Settings
FrameFluke uses a JSON file (FrameFluke_settings.json) to store custom settings. You can edit the following options in the JSON file:

+ Channels: Specify the channels to be rendered (options: all, rgb).
+ Premult: Choose whether to premultiply the render (options: True, False).
+ Crop: Enable or disable cropping the render to the input format (options: True, False).
+ Extension: Specify the file extension for the rendered frames (e.g., png, exr, tga, jpg).
+ Name Pattern: Define the filename pattern for the rendered frames using placeholders like {counter:03}, {node_name}, {frame:04}, {extension}.

Feel free to modify these settings in the provided JSON file to suit your requirements.

## Author
Created by [Luciano Cequinel](https://www.cequinavfx.com).

To provide feedback, report bugs, or share your suggestions, reach out to me at [lucianocequinel@gmail.com]().

## Version Information
+ Version: 2.0.4
+ Release Date: November 02, 2023

## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/)License - see the LICENSE file for details.
