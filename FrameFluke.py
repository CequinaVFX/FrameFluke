__author__ = 'Luciano Cequinel'
__contact__ = 'lucianocequinel@gmail.com'
__version__ = '2.0.4'
__release_date__ = 'November, 02 2023'
__license__ = 'MIT'


import nuke
import json
from os import path, walk, mkdir


def get_settings():
    """
    A simple function to collect custom settings from JSON file.
    I decided to use a JSON file to make it easy to edit the values without having to close and reopen Nuke.
    Feel free to edit these values to suit your requirements.
    More details in README.md

    :return:
        channels : str
            Specify the channels to be rendered (options: all, rgb)
        premult : bool
            Choose whether to premultiply the render (options: True, False)
        crop : bool
            Enable or disable cropping the render to the input format (options: True, False)
        extension: str
            Specify the file extension for the rendered frames
            must be an image extension (e.g., png, exr, tga, jpg)
        name_pattern : str
            Define the filename pattern for the rendered frames using placeholders
            {counter:03} > it's an integer counter, forcing to print 3 digits
            {node_name}  > it's the name of the selected node, that will be rendered
            {frame:04}   > current frame, forcing to print 4 digits
            {extension}  > file extension
    """

    _dirPath = path.dirname(__file__)
    saved_file = '/'.join([_dirPath, 'FrameFluke_settings.json'])

    if path.isfile(saved_file) :
        with open(saved_file, 'r') as openFile :
            settings = json.load(openFile)

        return (settings['channels'],
                settings['premult'],
                settings['crop'],
                settings['extension'],
                settings['name_pattern'])

    else :
        channels = "all"  # options: all, rgb
        premult = False  # options: True (case sensitive), to premult correctly, channels must be rgba or all
        crop = False  # options: True (case sensitive)
        extension = 'exr'  # options: png, tga, tiff, jpg
        name_pattern = "{counter:03}_{node_name}_{frame:04}.{extension}"

        return channels, premult, crop, extension, name_pattern


def validate_script():
    """
    Function to check:
    1) if Nuke Script is saved
    2) if user selected a node
    If Nuke Script == True and sel_node == True call main function,
    break the script otherwise.

        :return: None
    """

    if nuke.root().name() == 'Root':
        nuke.alert('Save your script first!')
        return
    else:
        sel_node = get_selection()
        if sel_node:
            frame_fluke(sel_node)

    return


def get_selection():
    """
    Function to get and validate the selected node

    :return:
        sel_node : Nuke class Node() > nuke.selectedNode()
    """
    sel_nodes = nuke.selectedNodes()

    if len(sel_nodes) == 1:
        sel_node = nuke.selectedNode()
        if sel_node.Class() != 'Viewer':
            return sel_node
        else:
            nuke.message('Selection cannot be an Viewer')
            return

    else:
        nuke.message("Select one node!")
        return


def frame_fluke(sel_node):
    """
    This is the main function.
    It will create nodes, set up, and render them according to the options specified in the JSON file.

    :param:
        sel_node: Nuke class Node() > nuke.selectedNode()
    :return:
        None
    """
    print('Starting render to {}'.format(sel_node.name()))

    # get settings from JSON
    channels, premult, crop, extension, name_pattern = get_settings()

    # Create a copy of the selected node to use when needed
    input_node = sel_node

    # Get current frame
    current_frame = (nuke.frame())

    # Get current script folder and create a folder called 'frames'
    script_dir = path.dirname(nuke.root().name())

    # Set sub-folder name
    folder_name = 'breakdown_frame_{:04}'.format(current_frame)

    # Set render folder path
    breakdown_dir = '/'.join([script_dir, folder_name])

    # Creates folder if it does not exist
    if not path.isdir(breakdown_dir):
        mkdir(breakdown_dir)

    # Get file list from breakdown dir and count it
    __, ___, files = next(walk(breakdown_dir))
    file_count = len(files) + 1

    # Create a filename to save
    name_dict = {'counter'   : file_count,
                 'frame'     : current_frame,
                 'node_name' : sel_node.name(),
                 'extension' : str(extension)
                 }

    filename = name_pattern.format(**name_dict)

    # Set breakdown file path
    save_breakdown = '/'.join([breakdown_dir, filename])

    # Get original state of Proxy Mode in Project Settings
    orig_proxy_mode = nuke.root().proxy()

    # Set Proxy Mode to Off for render purpose
    nuke.root()['proxy'].setValue(False)

    # Create a Premult Node
    if premult:
        new_premult = nuke.createNode('Premult', inpanel=False)
        # new_premult.setInput(0, input_node)
        new_premult.setSelected(True)

    # Create a Crop node
    if crop:
        new_crop = nuke.createNode('Crop', inpanel=False)
        new_crop['box'].setExpression('0', 0)
        new_crop['box'].setExpression('0', 1)
        new_crop['box'].setExpression('input.width', 2)
        new_crop['box'].setExpression('input.height', 3)
        new_crop.setSelected(True)

    # Create a Write node
    new_write = nuke.createNode('Write',
                                'name WriteFrame_{} file {} file_type {} channels {} create_directories True'
                                .format(input_node.name(),
                                        save_breakdown,
                                        extension,
                                        channels),
                                inpanel=True)
    new_write.setSelected(True)

    # Execute Write Node
    nuke.execute(new_write, current_frame, current_frame)

    # Delete temporary nodes
    if premult: nuke.delete(new_premult)
    if crop: nuke.delete(new_crop)
    nuke.delete(new_write)

    # Create Dot do mark where you render a frame
    new_dot = nuke.createNode('Dot', inpanel=False)
    new_dot['label'].setValue(folder_name)
    new_dot['tile_color'].setValue(4278190335)
    new_dot['note_font_size'].setValue(15)
    new_dot['note_font_color'].setValue(15)

    new_dot.setInput(0, input_node)
    next_node = input_node.dependent()[0]
    next_node.setInput(0, new_dot)

    input_x_pos, input_y_pos = sel_node.xpos(), sel_node.ypos()
    next_x_pos, next_y_pos = next_node.xpos(), next_node.ypos()

    mid_point_x = (input_x_pos + next_x_pos) / 3
    mid_point_y = (input_y_pos + next_y_pos) / 3

    if input_node.Class() == 'Dot':
        new_dot.setXpos(mid_point_x)
        new_dot.setYpos(mid_point_y)
    elif next_node.Class() == 'Dot':
        new_dot.setXpos(mid_point_x)
        new_dot.setYpos(mid_point_y)
    else:
        new_dot.setXpos(mid_point_x + 34)
        new_dot.setYpos(mid_point_y)

    # Set Proxy Mode to original state
    nuke.root()['proxy'].setValue(orig_proxy_mode)

    print('Render done!')
    print('{}'.format(filename))


if __name__ == '__main__':
    """ Run it without installation """
    validate_script()
