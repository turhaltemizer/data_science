import h5py
import os

class HDF5DatasetWriter():
    def __init__(self, dims, outputPath, dataKey="images", bufSize=1000):
        # Check to see if output path exists and if so raise an exception
        if(os.path.exists(outputPath)):
            raise ValueError("The supplied ouputPath already exisists and cannot be overwirtten. Manually"
                "delete the file before continuing.", outputPath)
            
        # Open the HDF5 database for writing and create two datasets: One to
        # store the images/features and another to store the class labels
        self.db = h5py.File(outputPath, "w")
        self.data = self.db.create_dataset(dataKey, dims, dtype="float")
        self.labels = self.db.create_dataset("labels", (dims[0],), dtype="int")
        
        # Store the buffer size, then initialize the buffer itself along with the index
        # into the datasets
        self.bufSize = bufSize
        self.buffer = {"data": [], "labels": []}
        self.idx = 0
        
        
    def add(self, rows, labels):
        # Add the rows and labels to the buffer
        self.buffer["data"].extend(rows)
        self.buffer["labels"].extend(labels)
        
        # Check to see if the buffer needs to be flushed to disk
        if(len(self.buffer["data"]) >= self.bufSize):
            self.flush()
            
    def flush(self):
        # Write the buffers to disk then reset the buffer
        i = self.idx + len(self.buffer["data"])
        self.data[self.idx:i] = self.buffer["data"]
        self.labels[self.idx:i] = self.buffer["labels"]
        self.idx = i
        self.buffer = {"data": [], "labels": []}
        
    def storeClassLabels(self, classLabels):
        # Create a dataset to store the actual class label names, 
        # then store the class labels
        dt = h5py.special_dtype(vlen=str)
        labelSet = self.db.create_dataset("label_names", (len(classLabels),), dtype=dt)
        labelSet[:] = classLabels
        
    def close(self):
        # Check to see if there are any other entries in the buffer 
        # that need to be flushed to disk
        if(len(self.buffer["data"]) > 0):
            self.flush()
            
        # Close the dataset
        self.db.close()