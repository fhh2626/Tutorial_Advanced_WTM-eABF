# -*- coding: utf-8 -*-
# Simulated Tempering Reweighter v0,1 alpha
# by Haohao Fu (fhh2626_at_gmail.com)
#
#　this toolkit is intended to calculate free-energy profile from
#  simulated tempering and parallel tempering

import sys
import numpy as np
import scipy

TEMPERATURE = 300
ORIGIN_PMF_FILE = 'merge.pmf'
ORIGIN_CVTRJFILE = 'output/free_energy.colvars.traj'
ORIGIN_COLUMN = [1]

COLUMN = [3, 4]
LOWERBOUNDARY = [0, 0]
UPPERBOUNDARY = [20, 20]
WIDTH = [0.2, 0.2]
OUTPUTPREFIX = 'reweighted.pmf'

BOLTZMANN = 0.00198719
ACCURACY = 0.000001

class reweighter:
    ''' do simulated/parallel tempering reweighting '''

    def __init__(self, 
                 temperatures, 
                 targetTemp, 
                 originalPmfFile,
                 cvtrjFile, 
                 originalColumn,
                 column, 
                 lowerboundary, 
                 upperboundary, 
                 width,
                 outputPrefix):
        ''' initialization
            inputs:
              temperatures: list of float, temperature of each replica
              targetTemp: float, of which temperature free-energy profile is generated
              originalPmfFile: string, path to input NAMD pmf file
              cvtrjFile: string, path to cvtrj file
              originalColumn: list of int, data which columns in cvtrj file will be read for the original CVs
              column: list of int, data which columns in cvtrj filw will be read for the new CVs
              lowerboundary: list of float, lowerboundary of free-energy profile
              upperboundary: list of float, upperboundary of free-energy profile
              width: list of float, with of free-energy profile
              outputPrefix: string, path to output files
        '''

        self._temperatures = temperatures
        self._targetTemp = targetTemp
        self._originalPmfFile = originalPmfFile
        self._cvtrjFile = cvtrjFile
        self._originalColumn = originalColumn
        self._column = column
        self._lowerboundary = np.array(lowerboundary)
        self._upperboundary = np.array(upperboundary)
        self._width = np.array(width)
        self._outputPrefix = outputPrefix

        self._dimension = len(self._column)

        assert((self._dimension) == len(self._lowerboundary))
        assert((self._dimension) == len(self._upperbounadry))
        assert((self._dimension) == len(self._width))
        assert(self._targetTemp in self._temperatures)

        self._histogram = np.zeros(((self._upperbounadry - self._lowerboundary + ACCURACY) / self._width).astype(int), float)
    
    def _readPMF(self):
        ''' read pmf file and store it internally '''
        pmfMatrix = np.loadtxt(self.originalPmfFile)
        pmfDimension = pmfMatrix.shape()[1] - 1
        pmfLowerboundary = np.min(pmfMatrix, axis=0)
        pmfUpperboundary = np.max(pmfMatrix, axis=0)
        pmfWidth = pmfMatrix[1,:-1] - pmfMatrix[0,:-1]

        pmfGrid = ((pmfUpperboundary - pmfLowerboundary + 0.00001) / pmfWidth).astype(int)

    def _readData(self):
        ''' read energy data '''

        print('Reading colvars.traj file.\n')

        with open(self._cvtrjFile, 'r') as cvtrjInput:
            with open(self._originalPmfFile, 'r') as pmfInput:

                # read cvtrj file
                for line in cvtrjInput.readlines():
                    if line.startswith('#'):
                        continue
                    
                    splitedLine = line.strip().split()
                    position = np.array(splitedLine[ORIGIN_COLUMN], dtype=float)

                    if (position - self._lowerboundary).any() < 0 or (position - self._upperboundary).any() > 0:
                        continue
                    else:
                        weightedSample = 
                        self._histogram[((position - self._lowerboundary) / self._width).astype(int)]

                    
        logInput = open(self._logFile, 'r')
        cvtrjInput = open(self._cvtrjFile, 'r')

        for line in logInput.readlines():
            if not line.startswith('TCL: ST: Step:'):
                continue
            splitedLine = line.strip().split()
            currentStep = int(splitedLine[3])
            currentTemp = float(splitedLine[5])
            currentEnergy = float(splitedLine[7])
        
            

        logInput.close()
        cvtrjInput.close()

        self._energyData = np.array(self._energyData)
        self._cvData = np.array(self._cvData)

        print('Reading completed!\n')

    def _calcPMF(self):
        ''' generate histogram and calculate PMF'''

        print('Calculating histogram.\n')

        for i in range(len(self._temperatures)):
            print(f'{i / len(self._temperatures) * 100}% finished.\n')
            for j in range(len(self._energyData[i])):
                pos = np.array((self._cvData[i][j] - self._lowerboundary + ACCURACY) / self._width, np.int)
                histogram[tuple(pos)] += np.exp(self._energyData[i][j] / BOLTZMANN * self._temperatureFactors[i])

        histogram[histogram==0] += ACCURACY

        self._pmf = -BOLTZMANN * self._targetTemp * np.log(histogram)
        self._pmf -= np.min(self._pmf)

        print('Calculating histogram finished!\n')

    def _writePMF(self):
        ''' write PMF to a file '''

        print('Writing PMF to a file.\n')

        with open(self._outputPrefix + '.pmf', 'w') as pmfOutput:
            # head of PMF
            pmfOutput.write(f'#     {self._dimension}\n')
            for i in range(self._dimension):
                pmfOutput.write(f'#    {self._lowerboundary[i]}    {self._width[i]}    {np.shape(self._pmf)[i]}    {0}\n')
            
            # loop over arbitrary dimension
            n = 0
            loopFlag = np.zeros(self._dimension, np.int)

            while n >= 0:
                RC = (loopFlag + 0.5) * self._width + self._lowerboundary
                for item in RC:
                    pmfOutput.write(f'{item}  ')
                pmfOutput.write(f'{self._pmf[tuple(loopFlag)]}\n')

                # mimic an nD for loop
                n = self._dimension - 1
                while n >= 0:
                    loopFlag[n] += 1
                    if loopFlag[n] > np.shape(self._pmf)[n] - 1:
                        loopFlag[n] = 0
                        n -= 1
                        pmfOutput.write('\n')
                    else:
                        break

        print('Writing PMF finished!\n')


    def calcPMF(self):
        ''' calculate and write pmf '''
        self._readData()
        self._calcPMF()
        self._writePMF()


a = reweighter(TEMPERATURES, TARGETTEMPERATURE, LOGFILE, CVTRJFILE, COLUMN, LOWERBOUNDARY, UPPERBOUNDARY, WIDTH, OUTPUTPREFIX)
a.calcPMF()