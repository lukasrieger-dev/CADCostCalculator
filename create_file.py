import ezdxf


doc = ezdxf.new('R2000')
msp = doc.modelspace()

#msp.add_circle((8, 5), radius=4)

points = [
    (0, 0, 0, 0, 0),
    (0, 5, 0, 0, 0),
    (2, 5, 0, 0, 1.0),
    (0, 5, 0, 0, -1.0),
    (0, 10, 0, 0, 0)
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