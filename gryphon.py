import sys
import os
import numpy
import statistics

# Class defining a set of measurements (single row of input file)
class DataSet(object):
    
    # Create an instance with readonly set ID
    def __init__(self, setId):
        self.set = setId
        self.measureSet = []
        self.groups = []

    # Method to append a subset
    def addSubset(self, measurements):

        # If there is an existing subset check the length
        if len(self.measureSet) > 0:
            assert len(self.measureSet[len(self.measureSet) - 1]) == len(measurements), "Measurement sets are different lengths! Aborting!"

        # Add the subset
        #print("Adding {} measurements to dataset {}".format(len(measurements), self.set))
        self.measureSet.append(measurements)

    # Method to compute the outliers
    def process(self):
        assert (len(self.measureSet) > 0 and len(self.measureSet[0]) > 0), "No measurements found to filter! Aborting!"

        # Loop over all the measurements
        self.groups = []
        for m in range(len(self.measureSet[0])):

            # Build a set of points from all the subsets
            grp = MeasurementGroup()
            for ss in range(len(self.measureSet)):
                grp.points.append(self.measureSet[ss][m])

            # Process the group
            grp.process()

            # Update the dataset state
            self.groups.append(grp)

class MeasurementGroup(object):
    
    # Init
    def __init__(self):
        self.rawMean = 0.0
        self.rawVariance = 0.0
        self.rawStdDev = 0.0
        self.filteredMean = 0.0
        self.filteredVariance = 0.0
        self.filteredStdDev = 0.0
        self.points = []
        self.medDist = []
        self.outliers = []
        self.retained = []
        self.outliersIdx = []
        self.retainedIdx = []
    
    def process(self):

        # Make sure that we have enough points to process
        assert len(self.points) > 2, "Measurement Group does not contain enough points! Aborting!"

        # Compute pre-filter mean, variance and standard deviation
        self.rawMean = statistics.mean(self.points)
        self.rawVariance = statistics.variance(self.points)
        self.rawStdDev = statistics.stdev(self.points)

        # Compute median
        median = statistics.median(self.points)

        # Compute absolute distance to median of each point in set
        self.medDist = []
        for i in range(len(self.points)):
            self.medDist.append(-abs(self.points[i] - median))

        # Sort distances and retain indices
        idx = numpy.argsort(self.medDist)

        # Split into outliers and retained points discarding 2 values
        self.outliers = []
        self.retained = []
        self.outliersIdx = []
        self.retainedIdx = []
        for i in range(len(idx)):
            if i < 2:
                self.outliersIdx.append(idx[i])
                self.outliers.append(self.points[idx[i]])
            else:
                self.retainedIdx.append(idx[i])
                self.retained.append(self.points[idx[i]])

        # Compute post-filter mean, variance and standard deviation
        self.filteredMean = statistics.mean(self.retained)
        self.filteredVariance = statistics.variance(self.retained)
        self.filteredStdDev = statistics.stdev(self.retained)

    # Method to determine whether a specified value is a retained or not
    def isRetainedValue(self, value):
        for i in range(len(self.retained)):
            if self.retained[i] == value:
                return True
        return False

########################
## Script begins here ##
########################

# Enable test mode
testMode = False

# Load the file
if testMode != True:
    assert (len(sys.argv) > 1), "You must specify the full name of the input data file!"
    filename = sys.argv[1]
else:
    filename = "TestMeasurements.txt"
try:
    inFile = open(filename, "r")
except IOError:
    print("Could not open file: {}".format(sys.argv[1]))

# Read in the file line by line and build the DataSets
contents = inFile.readlines()
inFile.close()
datasets = []
for line in contents:

    # Split line into chunks at the pipe
    chunks = line.split('|')

    # Check the correct size
    assert (len(chunks) > 1), "The line {} is too short! Aborting!".format(line)

    # Create measurement array
    ma = []
    for i in range(1, len(chunks)):
        ma.append(float(chunks[i]))
    
    # Check to see if dataset already exists for that ID
    # If so append, if not create a new dataset
    data = None
    for tmp in datasets:
        if tmp.set == chunks[0]:
            data = tmp
            break
    if data is not None:
        data.addSubset(ma)
    else:
        print("Creating a new dataset with ID {}".format(chunks[0]))
        data = DataSet(chunks[0])
        data.addSubset(ma)
        datasets.append(data)

# Loop over the datasets and filter them all
print("Input file read. {} datasets found.".format(len(datasets)))
for ds in datasets:
    print("Processing group with ID {}".format(ds.set))
    ds.process()

# Write results to file
outLines = []
for ds in datasets:
    print("Formatting dataset with ID {}".format(ds.set))

    # For each measure set (line of the input file)
    for ms in ds.measureSet:

        # Create a new line
        line = []

        # For each measurement in the set
        for m in range(len(ms)):

            # Determine whether the value was retained or not
            if ds.groups[m].isRetainedValue(ms[m]):
                line.append("{}R".format(ms[m]))
            else:
                line.append("{}X".format(ms[m]))
    
        # Generate the line
        outLines.append("{}|{}\n".format(ds.set, '|'.join(line)))

    # For each group (vertical slice through set) get mean and variance
    lineMean = []
    lineVar = []
    for g in ds.groups:

        # Extract mean amd variance
        lineMean.append("{:.2f}M".format(g.filteredMean))
        lineVar.append("{:.2f}V".format(g.filteredVariance))

    # Generate the lines
    outLines.append("{}|{}\n".format(ds.set, '|'.join(lineMean)))
    outLines.append("{}|{}\n".format(ds.set, '|'.join(lineVar)))

# Write the lines to a file
splitFile = os.path.splitext(filename)
outFile = open(splitFile[0] + "_filtered" + splitFile[1], "w")
outFile.writelines(outLines)
outFile.close()