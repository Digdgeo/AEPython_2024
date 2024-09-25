
import os, time, fiona, shapely, math
import numpy as np
from shapely.geometry import Polygon, Point, LineString, mapping
from fiona.crs import from_epsg


class alejandro():
    
    def __init__(self, shape, ext=True, perp=True, perp_max=True):
        t0 = time.time()
        
        # Initialize the class with the shapefile and optional parameters
        self.shape = shape  # Input shapefile path
        self.shp = fiona.open(shape)  # Open the shapefile
        self.csr = self.shp.crs  # Coordinate reference system of the shapefile
        self.perp = perp  # Whether to calculate perpendiculars
        self.path = os.path.split(shape)[0]  # Get the directory of the shapefile
        self.shape_name = os.path.split(shape)[1][:-4]  # Get the shapefile name (without extension)
        self.npath = os.path.join(self.path, 'lines')  # Directory to store the output shapefiles
        print(self.npath)
        os.makedirs(self.npath, exist_ok=True)  # Create the output directory if it doesn't exist
        
        # Initialize dictionaries to store line data
        self.din = {}  # For storing the longest internal lines
        self.dout = {}  # For storing the longest external lines (intersecting but not fully inside)
        self.dperp = {}  # For storing perpendicular lines
        self.ext = ext  # Whether to calculate external lines
        self.max_perp = {}  # For storing the maximum perpendicular line
        self.perp_max = perp_max  # Whether to calculate maximum perpendicular
        
        # Initialize dictionaries to store vertices and polygons
        self.d = {i['properties']['id']: [] for i in self.shp}  # Store the vertices for each polygon ID
        self.dpg = {i['properties']['id']: [] for i in self.shp}  # Store the polygons themselves
        
        nshape = 0  # Counter for the number of polygons
        nvertex = 0  # Counter for the number of vertices
        
        # Define output shapefiles for internal, external, perpendicular, and max perpendicular lines
        self.outdin = os.path.join(self.npath, self.shape_name + '_int.shp')
        self.outout = os.path.join(self.npath, self.shape_name + '_out.shp')
        self.outperp = os.path.join(self.npath, self.shape_name + '_perpendicular.shp')
        self.outmaxperp = os.path.join(self.npath, self.shape_name + '_max_perpendicular.shp')
        
        print(self.outdin, "\n", self.outmaxperp)
        
        # Iterate through each polygon in the shapefile
        for e in self.shp:
            nshape += 1  # Increment the polygon counter
            id_ = e['properties']['id']  # Get the ID of the polygon
            coords = e['geometry']['coordinates'][0]  # Get the coordinates of the polygon
            self.dpg[id_] = Polygon(e['geometry']['coordinates'][0])  # Store the polygon geometry in the dictionary
            for pt in coords:  # Iterate over each vertex in the polygon
                nvertex += 1  # Increment the vertex counter
                self.d[id_].append(Point(pt))  # Store the vertices in the dictionary

        print('Se han importado', nshape, 'poligonos y', nvertex - nshape, 'vertices en', time.time() - t0, 'segundos')

    def get_lines(self):
        """Calculate the longest internal and external lines for each polygon."""
        
        t0 = time.time()
        counter = 0

        din = {}  # Internal lines dictionary
        dout = {}  # External lines dictionary
        
        # Iterate over the dictionary of polygons
        for k, v in self.d.items():

            m_in = 0  # Maximum length of internal lines
            m_out = 0  # Maximum length of external lines

            print('\n########################################Haciendo el ID:', k, '\n')

            # Iterate over pairs of points (vertices) in the polygon
            for n, e in enumerate(v):
                for nn, ee in enumerate(v):
                    if nn > n:  # To avoid duplicate comparisons
                        counter += 1
                        l = e.distance(ee)  # Calculate the distance between two points (line length)

                        # Internal lines
                        if l > m_in:
                            line = LineString((e, ee))  # Create a LineString from the two points

                            if line.within(self.dpg[k]):  # Check if the line is fully within the polygon
                                self.din[k] = line  # Store the longest internal line
                                m_in = l  # Update the maximum internal line length
                                
                            elif line.intersects(self.dpg[k]):  # Check if the line intersects the polygon
                                if l > m_out:  # Check if the length is greater than the current external max
                                    self.dout[k] = line  # Store the longest external line
                                    m_out = l  # Update the maximum external line length

        print('Se han recorrido', counter, 'vertices en', time.time() - t0, 'segundos\n')
        
    def write_lines(self):
        """Write the internal and external lines to shapefiles."""
        
        # Define the schema for the shapefiles
        schema = {
                    'geometry': 'LineString',
                    'crs': self.shp.crs,
                    'properties': {'id': 'int', 'length': 'float'}}

        # Write internal lines shapefile
        with fiona.open(self.outdin, 'w', crs=self.csr, driver='ESRI Shapefile', schema=schema) as c:
            for k, v in self.din.items():
                c.write({
                    'geometry': mapping(v),
                    'properties': {'id': k, 'length': v.length}})
                
        if self.ext == True:
            # Write external lines shapefile
            with fiona.open(self.outout, 'w', crs=self.csr, driver='ESRI Shapefile', schema=schema) as c:
                for k, v in self.dout.items():
                    c.write({
                        'geometry': mapping(v),
                        'properties': {'id': k, 'length': v.length}})

    def get_perpendicular(self):
        """Calculate the perpendicular line at the midpoint of the longest internal line."""
        
        for k, v in self.din.items():
            mid_point = v.interpolate(0.5, normalized=True)  # Get the midpoint of the internal line
            
            pt1 = list(v.coords)[0]  # First point of the internal line
            pt2 = list(v.coords)[1]  # Second point of the internal line

            # Calculate the bearing (angle) of the internal line
            x_diff = pt2[0] - pt1[0]
            y_diff = pt2[1] - pt1[1]
            bearing = math.degrees(math.atan2(y_diff, x_diff))
            
            # Calculate the coordinates of the perpendicular line
            nangle = bearing - 90
            nbearing = math.radians(nangle)
            x = list(mid_point.coords)[0][0] + v.length * math.cos(nbearing)
            y = list(mid_point.coords)[0][1] + v.length * math.sin(nbearing)

            bearing = math.radians(bearing + 90)
            nx = list(mid_point.coords)[0][0] + v.length * math.cos(bearing)
            ny = list(mid_point.coords)[0][1] + v.length * math.sin(bearing)

            # Create a perpendicular line
            p1 = Point(x, y)
            p2 = Point(nx, ny)
            perpline = LineString((p1, p2))
            
            # Calculate the intersection of the perpendicular line with the polygon
            intersection = perpline.intersection(self.dpg[k])
            self.dperp[k] = intersection
            
            # If we want to calculate the maximum perpendicular
            if self.perp_max == True:
                md = 0  # Maximum distance of the perpendicular line
                dist = v.length / 100  # Distance increment
                for i in range(-50, 51):
                    mperp = perpline.parallel_offset(dist * i)  # Offset the perpendicular line
                    mintersection = mperp.intersection(self.dpg[k])  # Find intersection with the polygon
                    if mintersection.length > md:
                        self.max_perp[k] = mintersection  # Store the longest perpendicular
                        md = mintersection.length

    def write_perp_lines(self, dict_, out):
        """Write perpendicular lines to a shapefile."""
        
        schema = {
                    'geometry': 'LineString',
                    'crs': self.csr,
                    'properties': {'id': 'int', 'length': 'float'}}
        
        # Write the perpendicular lines to the output shapefile
        print(out)
        with fiona.open(out, 'w', crs=self.csr, driver='ESRI Shapefile', schema=schema) as c:
            for k, v in dict_.items():
                c.write({
                    'geometry': mapping(v),
                    'properties': {'id': k, 'length': v.length}})
                
    def run(self):
        """Main method to run all steps."""
        
        a.get_lines()  # Calculate internal and external lines
        a.write_lines()  # Write the lines to shapefiles
        if self.perp == True:
            a.get_perpendicular()  # Calculate perpendicular lines
            a.write_perp_lines(self.dperp, self.outperp)  # Write perpendicular lines
            if self.perp_max == True:
                a.write_perp_lines(self.max_perp, self.outmaxperp)  # Write the longest perpendicular line
