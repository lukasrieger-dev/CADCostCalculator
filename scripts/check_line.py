import ezdxf


DXF_TYPE_LWPOLYLINE = 'LWPOLYLINE'
DXF_TYPE_CIRCLE = 'CIRCLE'
DXF_TYPE_TEXT = 'TEXT'
DXF_TYPE_MTEXT = 'MTEXT'
DXF_TYPE_LINE = 'LINE'
DXF_TYPE_ARC = 'ARC'
DXF_TYPE_INSERT = 'INSERT'

document = ezdxf.readfile('../tests/dxf/UM00056770-20mm-S235JR.dxf')
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