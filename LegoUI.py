from maya import cmds
from LegoGenerator import LegoBrick

LEGO_COLORS = [
    {"r": 0.79, "g": 0.10, "b": 0.04}, # red
    {"r": 0.99, "g": 0.54, "b": 0.10}, # orange
    {"r": 0.95, "g": 0.80, "b": 0.22}, # yellow
    {"r": 0.14, "g": 0.47, "b": 0.25}, # green
    {"r": 0.0, "g": 0.33, "b": 0.75}, # blue
    {"r": 0.51, "g": 0.0, "b": 0.48}, #purple
    {"r": 0.89, "g": 0.80, "b": 0.62}, # tan 
    {"r": 0.58, "g": 0.54, "b": 0.45}, # dark tan
    {"r": 0.35, "g": 0.16, "b": 0.07}, # brown
    {"r": 1.0, "g": 1.0, "b": 1.0}, # white
    {"r": 0.61, "g": 0.63, "b": 0.62}, # light grey
    {"r": 0.34, "g": 0.35, "b": 0.34}, # dark grey
    {"r": 0.02, "g": 0.07, "b": 0.11} # black
]


class LegoWindow(object):
    """
    This class builds a window for the lego generator.
    """

    def __init__(self):
        self.window_name = "LegoWindow"
        self.length_slider = None
        self.width_slider = None
        self.plate_check = None
        self.smooth_check = None
        self.create_btn = None
        self.palette = None

    def show(self):
        if cmds.window(self.window_name, q=True, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name, title="Lego Generator", menuBar=True, width=300)
        self.build()
        cmds.showWindow()

    def build(self):
        column = cmds.columnLayout("Brick")
        self.width_slider = cmds.intSliderGrp("brickWidth", label="Brick Width", field=True, min=1, max=16, v=4)
        self.length_slider = cmds.intSliderGrp("brickLength", label="Brick Length", field=True, min=1, max=16, v=2)

        cmds.separator(h=10, style='none')

        frame = cmds.frameLayout(labelVisible=0, width=400, height=25)
        self.get_color_palette()

        cmds.setParent(column)

        self.plate_check = cmds.checkBox(label='Plate')
        self.smooth_check = cmds.checkBox(label='Smooth')

        cmds.separator(h=10, style='none')

        self.create_btn = cmds.button(label="Create Brick", c=self.create_brick)

    def create_brick(self, *args):
        # brick_length = cmds.intSliderGrp(self.length_slider, q=True, v=True)
        # brick_width = cmds.intSliderGrp(self.width_slider, q=True, v=True)
        # brick_color = cmds.palettePort(self.palette, q=True, rgb=True)
        # brick_plate = cmds.checkBox(self.plate_check, q=True, v=True)
        # brick_smooth = cmds.checkBox(self.smooth_check, q=True, v=True)

        brick_data = {
            "length": cmds.intSliderGrp(self.length_slider, q=True, v=True),
            "width": cmds.intSliderGrp(self.width_slider, q=True, v=True),
            "color": cmds.palettePort(self.palette, q=True, rgb=True),
            "plate": cmds.checkBox(self.plate_check, q=True, v=True),
            "smooth": cmds.checkBox(self.smooth_check, q=True, v=True),
        }

        brick = LegoBrick().create_brick(brick_data)

    def get_color_palette(self):
        palette = cmds.palettePort('palette', dim=(13, 1))
        c = 0
        for color in LEGO_COLORS:
            cmds.palettePort('palette', edit=True, rgb=(c, color["r"], color["g"], color["b"]))
            c = c + 1
     
        cmds.palettePort('palette', edit=True, redraw=True)
        self.palette = palette

    def close(self, *args):
        cmds.deleteUI(self.window_name)
