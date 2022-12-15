from maya import cmds
from LegoGenerator import LegoBrick

class LegoWindow(object):
    """
    This class builds a window for the lego generator.
    """

    def __init__(self):
        self.window_name = "LegoWindow"
        self.length_slider = None
        self.width_slider = None
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
        self.width_slider = cmds.intSliderGrp("brickWidth", label="Brick Width", field=True, min=1, max=10, v=4)
        self.length_slider = cmds.intSliderGrp("brickLength", label="Brick Length", field=True, min=1, max=10, v=2)

        cmds.separator(h=10, style='none')

        frame = cmds.frameLayout(labelVisible=0, width=400, height=25)
        self.get_color_palette()

        cmds.setParent(column)

        cmds.separator(h=10, style='none')

        self.create_btn = cmds.button(label="Create Brick", c=self.create_brick)

    def create_brick(self, *args):
        brick_length = cmds.intSliderGrp(self.length_slider, q=True, v=True)
        brick_width = cmds.intSliderGrp(self.width_slider, q=True, v=True)
        brick_color = self.get_color()
        brick = LegoBrick().create_brick(brick_length, brick_width, brick_color)

    def get_color_palette(self):
        palette = cmds.palettePort('palette', dim=(8, 1), cc=self.get_color)
        cmds.palettePort('palette', edit=True, rgb=(0, 0.79, 0.10, 0.04))
        cmds.palettePort('palette', edit=True, rgb=(1, 0.99, 0.54, 0.10))
        cmds.palettePort('palette', edit=True, rgb=(2, 0.95, 0.80, 0.22))
        cmds.palettePort('palette', edit=True, rgb=(3, 0.14, 0.47, 0.25))
        cmds.palettePort('palette', edit=True, rgb=(4, 0.0, 0.33, 0.75))
        cmds.palettePort('palette', edit=True, rgb=(5, 0.51, 0.0, 0.48))
        cmds.palettePort('palette', edit=True, rgb=(6, 1.0, 1.0, 1.0))
        cmds.palettePort('palette', edit=True, rgb=(7, 0.02, 0.07, 0.11))
        cmds.palettePort('palette', edit=True, redraw=True)
        self.palette = palette

    def get_color(self):
        if self.palette:
            return cmds.palettePort(self.palette, query=True, rgb=True)

    def close(self, *args):
        cmds.deleteUI(self.window_name)
