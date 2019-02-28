# from visit_utils import *
# Source("/path/to/view.py")
# import re, os, sys
def setup_ccl_plot():
    DeleteAllPlots()
    #OpenDatabase("/data/kxx/GR_AMR/random-4/scalar-00001.visit/dumps.visit")
    OpenDatabase("/path/to/dumps.visit")
    # DefinePythonExpression("density",["DIFFr","DIFFchi"],file = '/data/kxx/GR_AMR/random-4/filter.py',type = 'scalar')
    DefinePythonExpression("density",["DIFFr","DIFFchi"],file = '/path/to/filter.py',type = 'scalar')
    AddPlot("Pseudocolor","density")
    # change 3d angle
    # Begin spontaneous state
    View3DAtts = View3DAttributes()
    View3DAtts.viewNormal = (-0.6172, 0.512036, 0.597397)
    View3DAtts.focus = (80, 80, 80)
    View3DAtts.viewUp = (0.648935, -0.0980637, 0.754498)
    View3DAtts.viewAngle = 30
    View3DAtts.parallelScale = 138.564
    View3DAtts.nearPlane = -277.128
    View3DAtts.farPlane = 277.128
    View3DAtts.imagePan = (0, 0)
    View3DAtts.imageZoom = 1
    View3DAtts.perspective = 1
    View3DAtts.eyeAngle = 2
    View3DAtts.centerOfRotationSet = 0
    View3DAtts.centerOfRotation = (80, 80, 80)
    View3DAtts.axis3DScaleFlag = 0
    View3DAtts.axis3DScales = (1, 1, 1)
    View3DAtts.shear = (0, 0, 1)
    View3DAtts.windowValid = 1
    SetView3D(View3DAtts)
    # DrawPlots()
    # End spontaneous state


# extract the selected regions
def cal_den(ts):
    SetTimeSliderState(ts)
    DrawPlots()
    Query('MinMax')
    # get the coordinates
    # str = Query('MinMax')
    # extr = re.findall(r'-?\d+\.?\d*e?-?\d*?', str)
    val = GetQueryOutputValue()
    # not change the default color screen settings
    th_atts = ThresholdAttributes()
    th_atts.listedVarNames = ("density")
    th_atts.zonePortions = (1)
    th_atts.lowerBounds = (val[0])
    th_atts.upperBounds = (val[1])
    SetOperatorOptions(th_atts)
    DrawPlots()

# get the total steps    
'''
def get_plot_step():
    setup_ccl_plot()
    DrawPlots()
    nts = TimeSliderGetNStates()
    print "the total step is : %d" % nts
'''

# show each screen modified
def setup_graphs(start=0,stride=1):
    setup_ccl_plot()
    DrawPlots()
    nts = TimeSliderGetNStates()
    for ts in range(start,nts,stride):
        cal_den(ts)
        print "step: %d  \n" % ts 
        