import firebase_admin
import numpy as numpy
from firebase_admin import credentials
from firebase_admin import firestore
import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

# --------------------------------------------------------------------
# 				Retrieving Data from Firebase
# --------------------------------------------------------------------

# Use a service account
cred = credentials.Certificate('./service_account.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

series_reference = db.collection(u'users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi/series')
series_reference_request = series_reference.get()

dataset = []
dates = []

for asset in series_reference_request:
    asset_dict = asset.to_dict()
    dates.append(str(asset_dict[u'date']))
    dataset.append(float(asset_dict[u'close']))

dataset = pandas.DataFrame(data=dataset)

# --------------------------------------------------------------------
# 		Convert an array of values into a dataset matrix
# --------------------------------------------------------------------
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

# --------------------------------------------------------------------
# 		Data normalization to an interval between -1 and 1       
# --------------------------------------------------------------------

# fix random seed for reproducibility
numpy.random.seed(7)

#  Normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)


# --------------------------------------------------------------------
# 		Splitting up the dataset in a train and a test dataset
# --------------------------------------------------------------------

train_size = int(len(dataset) * 0.8) 	# Train Size
test_size = len(dataset) - train_size	# Test Size

train_close_values = dataset[0:train_size, :]			# Train Close Values
test_close_values = dataset[train_size:len(dataset), :]	# Test Close Values

train_date_values = dates[0:train_size]				# Train Date Values
test_date_values = dates[train_size:len(dates)]		# Test Date Values

# --------------------------------------------------------------------
# 		Reshaping into X=t and Y=t+1
# --------------------------------------------------------------------

# reshape into X=t and Y=t+1
look_back = 3
trainX, trainY = create_dataset(train_close_values, look_back)
testX, testY = create_dataset(test_close_values, look_back)

print('trainX')
print(trainX)
print('trainY')
print(trainY)

# --------------------------------------------------------------------
# 		Wave_Dancer Core Model
# --------------------------------------------------------------------

# create and fit the LSTM network   
model = Sequential()
model.add(Dense(12, input_dim=look_back, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(trainX, trainY, epochs=10, batch_size=2, verbose=2)


# --------------------------------------------------------------------
# 		Calculating MSE
# --------------------------------------------------------------------

# make predictions
train_predictions = model.predict(trainX)
test_predictions = model.predict(testX)

# invert predictions
train_predictions = scaler.inverse_transform(train_predictions)
trainY = scaler.inverse_transform([trainY])
test_predictions = scaler.inverse_transform(test_predictions)
testY = scaler.inverse_transform([testY])

# calculate root mean squared error
trainScore = math.sqrt(mean_squared_error(trainY[0], train_predictions[:,0]))
print('Train Score: %.2f RMSE' % (trainScore))
testScore = math.sqrt(mean_squared_error(testY[0], test_predictions[:,0]))
print('Test Score: %.2f RMSE' % (testScore))


# --------------------------------------------------------------------
# 		Visualization
# --------------------------------------------------------------------

# shift train predictions for plotting
train_predictionsPlot = numpy.empty_like(dataset)
train_predictionsPlot[:, :] = numpy.nan
train_predictionsPlot[look_back:len(train_predictions)+look_back, :] = train_predictions
# shift test predictions for plotting
test_predictionsPlot = numpy.empty_like(dataset)
test_predictionsPlot[:, :] = numpy.nan
test_predictionsPlot[len(train_predictions)+(look_back*2)+1:len(dataset)-1, :] = test_predictions
# plot baseline and predictions
# plt.plot(scaler.inverse_transform(dataset))
# plt.plot(train_predictionsPlot)
# plt.plot(test_predictionsPlot)
# plt.show()


# --------------------------------------------------------------------
# 		Writing Data to the Firebase Database
# --------------------------------------------------------------------

# Train Predictions

train_predictions_firestore_collection = db.collection(u'users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi/train_predictions')

for i in range(1, len(train_predictions)):
    train_predictions_firestore_collection.document(train_date_values[i]).set({
		'date': str(train_date_values[i]),
		'predicted_close': float(train_predictions[i]) 
	})

print('trian_predictions have been written to firebase.')

# Test Predictions

test_predictions_firestore_collection = db.collection(u'users/pej3fiZSJTf4tNHfNHCKHxa7eJf2/markets/cXdEgLKHka1UfLqC3NVU/assets/GsLZC6PukRyz0JUGMNYi/test_predictions')

for i in range(1, len(test_predictions)):
	print(str(test_date_values[i]))
	test_predictions_firestore_collection.document(test_date_values[i]).set({'date': str(test_date_values[i]),'predicted_close': float(test_predictions[i])})

print('test_predictions have been written to firebase.')

