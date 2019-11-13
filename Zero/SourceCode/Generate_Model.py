## DataProcessing and model generation process
import hdf5storage
import numpy as np
from scipy.signal import butter, lfilter
import math
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from keras.utils import np_utils
import tensorflow as tf
from keras import backend as K
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten, AveragePooling2D, Activation
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential

def Re_referencing(eegData, channelNum, sampleNum):
    after_car = np.zeros((channelNum,sampleNum))
    for i in np.arange(channelNum):
        after_car[i,:] = eegData[i,:] - np.mean(eegData,axis=0)
    return after_car

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def Epoching(eegData, stimsT, samplingFreq, channelNum, epochSampleNum, offset, baseline):
    Time_after = np.add(stimsT,offset).astype(int)
    Time_base = np.add(stimsT,baseline).astype(int)
    Num = stimsT.shape[1]
    Epochs = np.zeros((Num, channelNum, epochSampleNum))
    for j in range(Num):
        Epochs[j, :, :] = eegData[:,Time_after[0][j]:Time_after[0][j] + epochSampleNum]
        for i in range(channelNum):
            Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time_after[0][j]:Time_base[0][j]]))
    return [Epochs,Num]

def DownsamplingEpoch(EpochsT, EpochsN, downsampleRate):
    num = np.floor(EpochsT.shape[2] / downsampleRate).astype(int)
    DownsampledT = np.zeros((EpochsT.shape[0],EpochsT.shape[1],num))
    DownsampledN = np.zeros((EpochsN.shape[0],EpochsN.shape[1],num))
    for i in range(num):
        for j in range(EpochsT.shape[1]):
            for k in range(EpochsT.shape[0]):
                DownsampledT[k,j,i] = np.mean(EpochsT[k,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
            for l in range(EpochsN.shape[0]):
                DownsampledN[l,j,i] = np.mean(EpochsN[l,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
    return [DownsampledT, DownsampledN, num]

def GenerateP300Data(filename):
    target = np.zeros((300,32,51))
    nontarget = np.zeros((1500,32,51))
    for i in np.arange(1,3):
        if (i==2):
            filename = filename + '_2'
        mat = hdf5storage.loadmat(filename)
        eegData = mat['eegData']
        samplingFreq = mat['samplingFreq'][0,0]
        stimsN = mat['stimsN']
        stimsT = mat['stimsT']
        channelNum = 32
        sampleNum = eegData.shape[1]
    
        ## Preprocessing process
        # eegData1 = eegData
    
        #Common Average Reference
        eegData = Re_referencing(eegData, channelNum, sampleNum)
    
        #Bandpass Filter
        eegData = butter_bandpass_filter(eegData, 0.5, 10, samplingFreq,4)
        # FFTPlotFull(eegData, samplingFreq)
        # # FFTPlot(eegData, samplingFreq, 15)
    
        #Epoching
        epochSampleNum = int(np.floor(0.4 * samplingFreq))
        offset = int(np.floor(0.2 * samplingFreq))
        baseline = int(np.floor(0.6 * samplingFreq))
        [EpochsT, NumT] = Epoching(eegData, stimsT, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [EpochsN, NumN] = Epoching(eegData, stimsN, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        # EpochPlot(EpochsT, EpochsN, epochSampleNum, 0.2, 0.6, 30)
    
        #Downsampling
        downsampleRate = 4
        samplingFreq = samplingFreq/4
        [EpochsT,EpochsN,epochSampleNum] = DownsamplingEpoch(EpochsT, EpochsN, downsampleRate)
        # EpochPlot(EpochsT, EpochsN, epochSampleNum, 0.2, 0.6, 31)
    
        # eegData = Downsampling(eegData, 4)
        # samplingFreq = samplingFreq/4

        # # plotEEGdata(eegData, channelNum)
        target[150*(i-1):150*i,:,:] = EpochsT
        nontarget[750*(i-1):750*i,:,:] = EpochsN
    tar = filename + '_t.out'
    ntar = filename + '_nt.out'
    
    with open(tar, 'w') as f:
        f.write('# Array shape: {0}\n'.format(target.shape))
        for data_slice in target:
            np.savetxt(f, data_slice)
            f.write('# New slice\n')
    
    with open(ntar, 'w') as fl:
        fl.write('# Array shape: {0}\n'.format(nontarget.shape))
        for data_slice in nontarget:
            np.savetxt(fl, data_slice)
            fl.write('# New slice\n')
    
    return [target, nontarget]

#saveTargetroot = '/home/wsanghum/PythonFiles/alltarget.out'
#saveNontargetroot = '/home/wsanghum/PythonFiles/allnontarget.out'
#root = '/home/wsanghum/matlab/Data/S'
    
saveTargetroot = 'C:/Users/wldk5/WorldSystem/Zero/CNNdata/55P300data/PythonData/alltarget.out'
saveNontargetroot = 'C:/Users/wldk5/WorldSystem/Zero/CNNdata/55P300data/PythonData/allnontarget.out'
root = 'C:/Users/wldk5/WorldSystem/Zero/CNNdata/55P300data/MatlabData/S'
filename2 = '_2'
filename = ''
alltarget = np.zeros((300*55,32,51))
allnontarget = np.zeros((1500*55,32,51))
for i in np.arange(1,56):
    filename = ''
    if(i<10):
        filename = root + '0' + str(i)
    else:
        filename = root + str(i)
    [alltarget[300*(i-1):300*i,:,:],allnontarget[1500*(i-1):1500*i,:,:]] = GenerateP300Data(filename)
    print("subject {0} is preprocessed".format(str(i)))

with open(saveTargetroot, 'w') as outfile:
    outfile.write('# Array shape: {0}\n'.format(alltarget.shape))
    for data_slice in alltarget:
        np.savetxt(outfile, data_slice)
        outfile.write('# New slice\n')
a = np.loadtxt(saveTargetroot)
print(a.shape)
a = a.reshape((300*55,32,51))
print(np.all(a == alltarget))

with open(saveNontargetroot, 'w') as outfile:
    outfile.write('# Array shape: {0}\n'.format(allnontarget.shape))

    for data_slice in allnontarget:
        np.savetxt(outfile, data_slice)
        outfile.write('# New slice\n')
b = np.loadtxt(saveNontargetroot)
print(b.shape)
b = b.reshape((1500*55,32,51))
print(np.all(b == allnontarget))

#nsb = 1;
#print(nsb);
#target = alltarget[np.setdiff1d(np.arange(0,16500), np.arange((nsb-1)*300,nsb*300)),:,:];
#nontarget = allnontarget[np.setdiff1d(np.arange(0,82500), np.arange((nsb-1)*1500,nsb*1500)),:,:];


#trainingData = np.concatenate((target,nontarget),axis = 0);
trainingData = np.concatenate((alltarget,allnontarget),axis = 0);
trainingData = np.reshape(trainingData,(1800*54,1,32,51));

label = np.concatenate((np.ones(300*54),np.zeros(1500*54)),0);
label = np_utils.to_categorical(label, 2);

##Generating CNN model
model = Sequential();
#model.add(AveragePooling2D(pool_size=(1, 4), strides=(1,4))) # this was added
model.add(Conv2D(51, kernel_size=(1, 25),data_format='channels_first',input_shape=(1, 32,51)))
model.add(BatchNormalization())
model.add(Conv2D(51, (32, 1),data_format='channels_first'))
model.add(BatchNormalization())
model.add(Flatten())
model.add(Dense(2))
model.add(Activation('softmax'))

#model = multi_gpu_model(model, gpus=2);
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam');

data = trainingData;
randIdx = np.random.permutation(54*1800);
trainIdx = randIdx[0:int(1800*54*0.95)];
valIdx = randIdx[int(1800*54*0.95):54*1800];

trainData = data[trainIdx,:,:,:];
trainLabel = label[trainIdx];
valData = data[valIdx,:,:,:];
valLabel = label[valIdx];

early_stopping = EarlyStopping(patience = 3);

fittedModel = model.fit(trainData, trainLabel, epochs=10, validation_data=(valData, valLabel), callbacks=[early_stopping]);

model.save('C:/Users/wldk5/WorldSystem/Zero/ZeroModel/ZeroCNN.h5')
model.save_weights('C:/Users/wldk5/WorldSystem/Zero/ZeroModel/ZeroCNNWeight.h5')