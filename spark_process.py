import matplotlib.pyplot as plt
from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD

NORMALIZER = 100
TRAINING_DATA_PERCENTAGE = 0.8
FILE_LOCATION = "/Users/pengtang/PycharmProjects/million_song_ml/my_csv.csv"

def parsePoint(line):
    values = [x for x in line.split('|')]
    try:
        return LabeledPoint(float(values[4])/NORMALIZER, [float(values[5])/NORMALIZER])
    except:
        return LabeledPoint(0, [0])

# Let's draw the scattered plot
f = open(FILE_LOCATION, 'r')
line_count = 0
fail_count = 0
for line in f.readlines():
    if line_count == 0:
        line_count += 1
        continue
    values = [x for x in line.split('|')]
    try:
        plt.scatter(float(values[4])/NORMALIZER, float(values[5])/NORMALIZER)
    except ValueError:
        # print line
        # print values
        fail_count += 1
print "we failed", fail_count, "for drawing"

sc = SparkContext(appName="Million_Song_Subset")
song_rdd = sc.textFile(FILE_LOCATION)


header = song_rdd.first() #extract header
song_rdd = song_rdd.filter(lambda row: row != header)   # filter out header
train = song_rdd.take(int(song_rdd.count() * TRAINING_DATA_PERCENTAGE))
song_rdd_train = song_rdd.filter(lambda row: row in train)  # training data
song_rdd_test = song_rdd.filter(lambda row: row not in train) # testing data

# print "we have ", song_rdd.count(), " records"
# print "we have ", song_rdd_train.count(), " records for training"
# print "we have ", song_rdd_test.count(), " records for testing"

parsedData = song_rdd_train.map(parsePoint)

# Build the model on training data
model = LinearRegressionWithSGD.train(parsedData, intercept = True)

# Test the model on testing data, save result to a csv file
result_file = open("result_file.csv", "w")
result_file.write("input|output|desired_output\n")
for test_record in song_rdd_test.collect():
    values = [x for x in test_record.split('|')]
    try:
        test_input = float(values[4]) / NORMALIZER
        test_output = model.predict([test_input])
        test_desired_output = float(values[5]) / NORMALIZER

        result_file.write(str(test_input) + '|' + str(test_output) + '|' + str(test_desired_output) + '\n')
    except ValueError:
        pass
result_file.close()


#Evaluate the model on training data
#valuesAndPreds = parsedData.map(lambda p: (p.label, model.predict(p.features)))
#MSE = valuesAndPreds.map(lambda (v, p): (v - p)**2).reduce(lambda x, y: x + y) / valuesAndPreds.count()
#print("Mean Squared Error = " + str(MSE))

# Show the drawing
plt.show()
