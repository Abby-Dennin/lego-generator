from maya import cmds


class LegoBrick(object):
    def __init__(self):
        self.brick = None

    def create_brick(self, length, width, color, plate=False):
        size_y = 0.32 if plate else 0.96
        size_x = width * 0.8
        size_z = length * 0.8

        brick = cmds.polyCube(h=size_y, w=size_x, d=size_z, sx=width, sz=length)

        for i in range(width):
            for j in range(length):
                nub = cmds.polyCylinder(r=0.25, h=0.2)
                cmds.move(size_y / 2.0 + 0.1, moveY=True, a=True)
                cmds.move((-size_x / 2.0 + (i + 0.5) * 0.8), moveX=True, a=True)
                cmds.move((-size_z / 2.0 + (j + 0.5) * 0.8), moveZ=True, a=True)

                brick = cmds.polyCBoolOp(brick, nub, op=1, ch=False)

        brick_hole = cmds.polyCube(h=size_y, w=size_x - 0.12 * 2, d=size_z - 0.12 * 2, sx=1, sz=1)
        cmds.move(-0.1, moveY=True)

        brick = cmds.polyCBoolOp(brick, brick_hole, op=2, ch=False)

        for i in range(width - 1):
            for j in range(length - 1):
                inner_nub = cmds.polyCylinder(r=0.3255, h=size_y - 0.2, sx=10)
                inner_nub_hole = cmds.polyCylinder(r=0.25, h=size_y, sx=10)
                inner_nub = cmds.polyCBoolOp(inner_nub, inner_nub_hole, op=2, ch=False)

                cmds.move(-0.05, moveY=True, a=True)
                cmds.move((-size_x / 2.0 + (i + 1) * 0.8), moveX=True, a=True)
                cmds.move((-size_z / 2.0 + (j + 1) * 0.8), moveZ=True, a=True)

                brick = cmds.polyCBoolOp(brick, inner_nub, op=1, ch=False)

        print(brick)
        self.apply_material(color)
        self.brick = brick

    def apply_material(self, color):
        if cmds.objExists(self.brick[0]):
            shd_node = cmds.shadingNode('lambert', name="%s_lambert" % self.brick[0], asShader=True)
            shd_sg = cmds.sets(name="%sSG" % shd_node, empty=True, renderable=True, noSurfaceShader=True)
            cmds.connectAttr("%s.outColor" % shd_node, "%s.surfaceShader" % shd_sg)
            cmds.setAttr(shd_node + ".color", color[0], color[1], color[2], type="double3")
            cmds.sets(self.brick[0], e=True, forceElement=shd_sg)


