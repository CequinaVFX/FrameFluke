import nuke
import FrameFluke

# you can change the shortcut here; use 'None' if you do not want a shortcut
SHORTCUT = 'F12'
# Set an icon; use 'None' if you do not want a one
ICON = 'FrameFluke.png'

toolbar = nuke.menu('Nodes')
customTools = toolbar.addMenu('CustomTools', 'Write.png')
customTools.addCommand('Frame Fluke', 'FrameFluke.validate_script()', SHORTCUT, icon='FrameFluke.png')
