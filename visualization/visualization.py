import matplotlib.pyplot as plt
import pandas
from datetime import datetime
from dateutil import parser


class Visualization:

    def display_series(self, df):

        # fig = plt.figure(facecolor='white')
        # # ax = fig.add_subplot(111)
        # # ax.plot(df, label='True Data')
        # dates = []
        # for i in range(0, len(df)):
        #     dates.append(parser.parse(df['date'][i]))

        # print(dates)

        plt.plot(df['value'])


        plt.show()


    def plot_results(self, predicted_data, true_data):
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)
        ax.plot(true_data, label='True Data')
        plt.plot(predicted_data, label='Prediction')
        plt.legend()
        plt.show()

    def plot_results_multiple(self, predicted_data, true_data, prediction_len):
        fig = plt.figure(facecolor='white')
        ax = fig.add_subplot(111)
        ax.plot(true_data, label='True Data')
        #Pad the list of predictions to shift it in the graph to it's correct start
        for i, data in enumerate(predicted_data):
            padding = [None for p in range(i * prediction_len)]
            plt.plot(padding + data, label='Prediction')
            plt.legend()
        plt.show()
