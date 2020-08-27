import ezdxf


doc = ezdxf.new('R2000')
msp = doc.modelspace()

msp.add_circle((8, 5), radius=4)

points = [(0, 5, 0, 0, 0), (5, 0, 0, 0, 0), (10, 5, 0, 0, 0), (5, 10, 0, 0, 0), (0, 5, 0, 0, 0)]
msp.add_lwpolyline(points)

msp.add_text("Text Style Example: Liberation Serif",
             dxfattribs={
                 'style': 'LiberationSerif',
                 'height': 0.35}
             ).set_pos((2, 6), align='LEFT')

doc.saveas("circled_diamond_with_text.dxf")