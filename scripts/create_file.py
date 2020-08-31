import ezdxf


doc = ezdxf.new('R2000')
msp = doc.modelspace()

#msp.add_circle((8, 5), radius=4)

points = [
    (0, 10, 0, 0, 0),
    (0, 320, 0, 0, 0),
    (10, 0, 0, 0, 0),
    (10, 10, 0, 0, 0),
    (10, 320, 0, 0, 0),
    (10, 330, 0, 0, 0),
    (20, 20, 0, 0, 0),
    (20, 310, 0, 0, 0),
    (57.66, 25.3, 0, 0, 0),
    (780, 20, 0, 0, 0),
    (780, 310, 0, 0, 0),
    (790, 0, 0, 0, 0),
    (790, 10, 0, 0, 0),
    (790, 320, 0, 0, 0),
    (790, 330, 0, 0, 0),
    (800, 10, 0, 0, 0),
    (800, 320, 0, 0, 0)
]
msp.add_lwpolyline(points)


"""
msp.add_text("Text Style Example: Liberation Serif",
             dxfattribs={
                 'style': 'LiberationSerif',
                 'height': 0.35}
             ).set_pos((2, 6), align='LEFT')
"""


doc.saveas("complex_polyline.dxf")