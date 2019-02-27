# return the special value for density in regions
# import sys,os
class PyExpr(SimplePythonExpression):
    def __init__(self):
        """
        Constructor.
        """
        SimplePythonExpression.__init__(self)
        # set to provide a name & description for your expression.
        self.name = "PyExpr"
        self.description = "Custom Python Expression"
        # output_is_point_var:
        # true  if output centering is nodal
        # false if output centering is zonal
        self.output_is_point_var  = False
        # output_dimension:
        # set to indicate number of components in the output tuple.
        self.output_dimension = 1
        self.coef = 2 # define the default judgement coefficient
        self.total = 0 # define the total volume in hypersurface
        self.vols = 0 # individual volume
        self.energy = 0 
        self.avg = 0 
        self.sel = 0 # recognition part 
        # self.frac = 0
        
    def modify_contract(self,contract):
        pass

    def derive_variable(self,ds_in,domain_id):
        """
        Called to process each chunk.

        Use self.input_var_names & self.arguments to access expression
        variable names and const arguments.

        Return a new vtkDataArray with expression result values.
        """
        DIFFr_cell_vals = ds_in.GetCellData().GetArray(self.input_var_names[0]) 
        DIFFchi_cell_vals = ds_in.GetCellData().GetArray(self.input_var_names[1])
        ncells = ds_in.GetNumberOfCells()
        res = vtk.vtkFloatArray()
        res.SetNumberOfComponents(1)
        res.SetNumberOfTuples(ncells)

        # get the total conformal volume
        for i in xrange(ncells):
            cell = ds_in.GetCell(i)
            bounds = cell.GetBounds()
            self.vols = (1/((DIFFchi_cell_vals.GetTuple1(i)+1)**3)) * (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (bounds[5] - bounds[4])
            self.total += self.vols

        # get the total conformal energy

        for i in xrange(ncells):
            cell = ds_in.GetCell(i)
            bounds = cell.GetBounds()
            self.vols = (1/((DIFFchi_cell_vals.GetTuple1(i)+1)**3)) * (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (bounds[5] - bounds[4])
            self.energy += DIFFr_cell_vals.GetTuple1(i) * self.vols

        # calculate the average density
        self.avg = self.energy/self.total

        # select the proper mesh point
        '''
        for i in xrange(ncells):
            # res.SetTuple1(i, self.vol) # res.SetTuple1 is a wrapper function to take the input as the mesh value
            # solve the self.density value judgement
            # coef is the value to evaluate
            if DIFFr_cell_vals.GetTuple1(i) < (self.avg * self.coef):
                res.SetTuple1(i,0)
            else:
                res.SetTuple1(i,DIFFr_cell_vals.GetTuple1(i))
                self.vols = (1/((DIFFchi_cell_vals.GetTuple1(i)+1)**3)) * (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) * (bounds[5] - bounds[4])
                self.sel += DIFFr_cell_vals.GetTuple1(i) * self.vols
        '''
        # calculate the fraction of density
        for i in xrange(ncells):
            frac = DIFFr_cell_vals.GetTuple1(i)/self.avg
            res.SetTuple1(i,frac)

        # extract the fraction 
        '''
        self.frac = self.sel / self.energy
        file = "~/GR_AMR/frac.txt"
        detect = open(file,'w')
        # todo: write the fraction value to certain file
        '''

        return res  
    
py_filter = PyExpr