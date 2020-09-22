#!/usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import math

#Kun definert som global for å enkelt finne det man må endre på.
global file_name
global U_0

# Skriv inn navnet på datafilen, pass på at denne ligger i samme mappe som koden
# hvis filen ligger et annet sted må man skrive full "path" til filen.
file_name = "data_mena1001_lab1a.txt"

# Sett her verdien for startspenningen målt i øvelse 1a - del 4
U_0 = 80 #enhet mV

# Denne funksjonen regner ut verdien for uttrykket i ligning 8 og plotter
# Det utførs også en lineær regresjon og stigningstallet spyttes ut
def Plot(x_array, y_array, temp_array):

    #For plotting av spenning vs. temp:
    spenninger = []
    temperaturer = []
    for i in range(len(x_array)):

        #For å beregne Seebeck koeffisienten:
        spenninger.append(float(y_array[i]))
        temperaturer.append(float(temp_array[i]))

        #For å beregne varmeledningsevnen:
        x_array[i] = int(x_array[i])
        y_array[i] = math.log(abs(float(y_array[i])/U_0))

    #Endrer formen til listene til 1D numpy arrays slik at de kan leses av algoritmen LinearRegression
    X = np.asarray(x_array).reshape(-1,1)
    Y = np.asarray(y_array).reshape(-1,1)

    numpy_spenninger = np.asarray(spenninger).reshape(-1,1)
    numpy_temperaturer = np.flip(np.asarray(temperaturer).reshape(-1,1))


    model = LinearRegression()

    #lineær regresjon på spenning vs. tid
    model.fit(X, Y)
    Y_pred = model.predict(X)
    stigningstall_varmeledning = model.coef_

    #lineær regresjon på spenning vs. temperatur
    model.fit(numpy_temperaturer, numpy_spenninger)
    spenning_pred = model.predict(numpy_temperaturer)
    stigningstall_seebeck = model.coef_

    #plotter ln(U(t)/U(0)) vs tid for å bestemme varmeledningsevnen
    plt.subplot(211)
    plt.tight_layout()
    plt.scatter(X, Y)
    plt.xlabel("tid [s]")
    plt.ylabel("ln(U(t)/U(0))")
    plt.plot(X, Y_pred, 'r')
    plassering1 = plt.subplot(211)
    plassering1.annotate('Stigningstall: {:.2E}'.format(stigningstall_varmeledning[0][0]), xy=(0.9, 1), xycoords='axes fraction', fontsize=10,
                xytext=(0, -20), textcoords='offset points',
                ha='right', va='top')

    #Plotter spenning vs temp for å bestemme seebeck koeffisienten
    plt.subplot(212)
    plt.tight_layout()
    plt.scatter(numpy_temperaturer, numpy_spenninger)
    plt.xlabel("Temperatur [K]")
    plt.ylabel("Spenning [mV]")
    plt.plot(numpy_temperaturer, spenning_pred, 'r')
    plassering2 = plt.subplot(212)
    plassering2.annotate('Stigningstall: {:.2}mV/K'.format(stigningstall_seebeck[0][0]), xy=(0.9, 1), xycoords='axes fraction', fontsize=10,
                xytext=(0, -20), textcoords='offset points',
                ha='right', va='top')
    #plassering2.text('Stigningstall: {}'.format(str(stigningstall_seebeck)), verticalalignment='top', horizontalalignment='right')

    plt.show()

def Main():

    #Spenning
    U = []
    #Tid
    t = []
    #Temperatur
    T = []
    nummer = 1
    try:
        with open(str(file_name),"r") as f:

            for nummer, line in enumerate(f):

                print(
                      "t_{}:{}s".format(nummer, line.split(',')[0])+"    ","U_{}:{}mV".format(nummer, line.split(',')[1])+"   ",
                      "T_{}:{}K".format(nummer, round(float(line.split(',')[2].rstrip('\n'))+273.15, 2))
                      )
                U.append(abs(float(line.split(',')[1].rstrip('\n'))))
                t.append(line.split(',')[0].rstrip('\n'))
                T.append(float(line.split(',')[2].rstrip('\n'))+273.15)

                nummer += 1

    except FileNotFoundError:
        print("Fant ikke filen, har du skrevet rett navn/path?")

    Plot(t,U,T)


Main()
