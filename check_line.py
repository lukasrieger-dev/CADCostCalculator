import ezdxf


document = ezdxf.readfile('./docs/Blende_doppelt.dxf')
msp = document.modelspace()

for e in msp:
    dxftype = e.dxftype()
    if dxftype == 'LWPOLYLINE':
        with e.points('xyseb') as points:
            print(points)