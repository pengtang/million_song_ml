# Machine Learning on Million Song Subset with Spark

## Project Description
This project applies machine learning techniques on the million song subset, it runs a regression on the "start_of_fade_out" and "duration".

## Data Source and Description

Original subset data could be found at http://static.echonest.com/millionsongsubset_full.tar.gz

The data Description is at http://labrosa.ee.columbia.edu/millionsong/pages/example-track-description

## Project Dependency
Python dependency: tables, numpy, scipy, pyspark, matplotlib

## Run project
Step 1: Generate the csv file based on h5 file (a file my_csv.csv will be saved under your running location)
```sh
python convert_h5_to_csv.py <h5_directory/h5_files>
```

Step 2: Run spark(need to change csv file location in the spark_process.py)
```sh
python spark_process.py
```

## Result files
figure_1.png is the scatter plot of "start_of_fade_out" and "duration"

my_csv.csv is the important fields of a song transformed from a h5 file

result_file.csv is the test data result on the regression model
