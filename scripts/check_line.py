import ezdxf


document = ezdxf.readfile('./docs/UM00056770-20mm-S235JR.dxf')
msp = document.modelspace()

for e in msp:
    dxftype = e.dxftype()
    print(dxftype)
    if dxftype == 'LWPOLYLINE':
        with e.points('xyseb') as points:
            print(points)
    if dxftype == 'LINE':
        print(e.dxf.start)
        print(e.dxf.end)
    elif dxftype == 'ARC':
        print("---------")
        print(e.dxf.radius)
        print(e.dxf.center)
        print(e.start_point)
        print(e.end_point)
        print(e.dxf.start_angle)
        print(e.dxf.end_angle)
        print("---------")
    else:
        print(e.dxf.dxfattribs._attribs)