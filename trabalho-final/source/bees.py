#!/usr/bin/env python

import pandas as pd, numpy as np, matplotlib.pyplot as plt, datetime, os, math
from influxdb import DataFrameClient

from tensorflow.compat.v1 import set_random_seed
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, GRU
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from skits.preprocessing import HorizonTransformer

file = "https://www.researchgate.net/profile/Gustavo_Pessin/publication/335243419_RFIDAmazonBees/data/5d5ae226299bf1b97cf774dc/RFIDAmazonBees.xlsx"
df = pd.read_excel( file )


df[ "x" ]= df.Day.dt.strftime('%Y-%m-%d')
df['xx'] = pd.to_datetime(df['Hour'], format='%H').dt.time
df['tempo'] = pd.to_datetime( df['x'].apply( str ) + ' ' + df['xx'].apply( str ) )

df.set_index( [ "tempo" ], inplace = True )

df.drop( "x", axis = 1, inplace = True )
df.drop( "xx", axis = 1, inplace = True )
df.drop( "Day", axis = 1, inplace = True )
df.drop( "Hour", axis = 1, inplace = True )

np.set_printoptions( edgeitems = 5, suppress = True, linewidth = None, threshold = None )
plt.style.use( "ggplot" )

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

seed = 3
np.random.seed( seed )
set_random_seed( seed )

client = DataFrameClient( host = "database", port = 8086 )
client.create_database( "tecpro" )

plt.style.use( "ggplot" )

client.write_points( df, "bees", database = "tecpro" )

client.switch_database( "tecpro" )

query = """
	select ActivityLevel
	from bees
	order by time
"""

dfn = client.query( query )

x = np.array( dfn[ "bees" ].ActivityLevel.values )



dataset = x

scaler = MinMaxScaler( feature_range = ( 0, 1 ) )
dataset = scaler.fit_transform( dataset.reshape( -1, 1 ) )

train_size = int( len( dataset ) * 0.67 )
test_size = len( dataset ) - train_size
train, test = dataset[ 0 : train_size, : ], dataset[ train_size : len( dataset ), : ]

look_back = 1

ht = HorizonTransformer( horizon = 2 )

trainX = ht.fit_transform( train )[ : len( train ) - 1, 0 ].reshape( -1, 1 )
trainY = ht.fit_transform( train )[ : len( train ) - 1, 1 ]

testX = ht.fit_transform( test )[ : len( test ) - 1, 0 ].reshape( -1, 1 )
testY = ht.fit_transform( test )[ : len( test ) - 1, 1 ]

trainX = np.reshape( trainX, ( trainX.shape[ 0 ], 1, trainX.shape[ 1 ] ) )
testX = np.reshape( testX, ( testX.shape[ 0 ], 1, testX.shape[ 1 ] ) )

lstm = Sequential()
lstm.add( LSTM( 3, input_shape = ( 1, look_back ) ) )
lstm.add( Dense( 1 ) )
lstm.compile( loss = "mean_squared_error", optimizer = "adam" )
lstm.fit( trainX, trainY, epochs = 30, batch_size = 1, verbose = 1 )

trainPredict_lstm = lstm.predict( trainX )
testPredict_lstm = lstm.predict( testX )

trainPredict_lstm = scaler.inverse_transform( trainPredict_lstm )
testPredict_lstm = scaler.inverse_transform( testPredict_lstm )



trainX = np.reshape( trainX, ( trainX.shape[ 0 ], 1, trainX.shape[ 1 ] ) )
testX = np.reshape( testX, ( testX.shape[ 0 ], 1, testX.shape[ 1 ] ) )

gru = Sequential()
gru.add( GRU( 3, input_shape = ( 1, look_back ) ) )
gru.add( Dense( 1 ) )
gru.compile( loss = "mean_squared_error", optimizer = "adam" )
gru.fit( trainX, trainY, epochs = 30, batch_size = 1, verbose = 1 )

trainPredict_gru = gru.predict( trainX )
testPredict_gru = gru.predict( testX )

trainPredict_gru = scaler.inverse_transform( trainPredict_gru )
trainY = scaler.inverse_transform( [ trainY ] )
testPredict_gru = scaler.inverse_transform( testPredict_gru )
testY = scaler.inverse_transform( [ testY ] )



trainScore_lstm = math.sqrt( mean_squared_error( trainY[ 0 ], trainPredict_lstm[ :, 0 ] ) )
testScore_lstm = math.sqrt( mean_squared_error( testY[ 0 ], testPredict_lstm[ :, 0 ] ) )

trainScore_gru = math.sqrt( mean_squared_error( trainY[ 0 ], trainPredict_gru[ :, 0 ] ) )
testScore_gru = math.sqrt( mean_squared_error( testY[ 0 ], testPredict_gru[ :, 0 ] ) )

trainPredictPlot_lstm = np.empty_like( dataset )
trainPredictPlot_lstm[ :, : ] = np.nan
trainPredictPlot_lstm[ look_back : len( trainPredict_lstm ) + look_back, : ] = trainPredict_lstm

testPredictPlot_lstm = np.empty_like( dataset )
testPredictPlot_lstm[ :, : ] = np.nan
testPredictPlot_lstm[ len( trainPredict_lstm ) + ( look_back * 2 ) : len( dataset ), : ] = testPredict_lstm



trainPredictPlot_gru = np.empty_like( dataset )
trainPredictPlot_gru[ :, : ] = np.nan
trainPredictPlot_gru[ look_back : len( trainPredict_gru ) + look_back, : ] = trainPredict_gru

testPredictPlot_gru = np.empty_like( dataset )
testPredictPlot_gru[ :, : ] = np.nan
testPredictPlot_gru[ len( trainPredict_gru ) + ( look_back * 2 ) : len( dataset ), : ] = testPredict_gru



fig, axes = plt.subplots( nrows = 2, ncols = 1, figsize = ( 14.23, 7.54 ), dpi = 90 )
fig.subplots_adjust( left = 0.03, right = 0.96, top = 0.96, bottom = 0.06 )

axes[ 0 ].plot( scaler.inverse_transform( dataset ), color = "blue" )
axes[ 0 ].plot( trainPredictPlot_gru, color = "red", linestyle = "dashed" )
axes[ 0 ].plot( testPredictPlot_gru, color = "red" )
axes[ 0 ].text( 786, 2.3, "GRU\n" + str( round( testScore_gru, 3 ) ) )
axes[ 0 ].axvline( 497, color = "green" )

axes[ 1 ].plot( scaler.inverse_transform( dataset ), color = "blue" )
axes[ 1 ].plot( trainPredictPlot_lstm, color = "red", linestyle = "dashed" )
axes[ 1 ].plot( testPredictPlot_lstm, color = "red" )
axes[ 1 ].text( 786, 2.3, "LSTM\n" + str( round( testScore_lstm, 3 ) ) )
axes[ 1 ].axvline( 497, color = "green" )

fig.savefig( "../output/bees.png" )

print()
print( "Arquivo output/bees.png gerado com sucesso." )
print()
