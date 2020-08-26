import ezdxf

doc = ezdxf.new('R2000')
msp = doc.modelspace()

points = [(0, 0, 0, 0, 0), (10, 0, 0, 0, .75), (25, 0, 0, 0, 0)]
msp.add_lwpolyline(points)

doc.saveas("polyline_test.dxf")

