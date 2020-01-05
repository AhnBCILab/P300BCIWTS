import numpy as np
from scipy.signal import butter, lfilter
import os, glob
from keras.models import load_model
import matlab.engine
import hdf5storage

def Readtxt(directory):
    ##Result txt file read in order to get orders
    f = open(directory, 'r', encoding='utf-16')
    j = 0
    Resultline = []
    while True:
        Resultline.append(f.readline())
        j = j + 1
        if Resultline[-1] == "\n": 
            Resultline.pop()
            j = j - 1
        if not Resultline[-1]: 
            Resultline.pop()
            j = j - 1
            break
#         print(j)
    f.close()
    return [j, Resultline]

### The Methods for Signal Processing ###
def Downsampling(eegData, downsampleRate):
        num = np.floor(eegData.shape[1] / downsampleRate).astype(int)
        Downsampled = np.zeros((eegData.shape[0],num))
        for i in range(num):
            for j in range(eegData.shape[0]):
                Downsampled[j,i] = np.mean(eegData[j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
        return Downsampled

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
    
def Epoching(eegData, stims, code, samplingRate, nChannel, epochSampleNum, epochOffset,baseline):
        Time = stims[np.where(stims[:,1] == code),0][0]
        Time = np.floor(np.multiply(Time,samplingRate)).astype(int)
        Time_after = np.add(Time,epochOffset).astype(int)
        Time_base = np.add(Time,baseline).astype(int)
        Num = Time.shape
        Epochs = np.zeros((Num[0], nChannel, epochSampleNum))
        for j in range(Num[0]):
            Epochs[j, :, :] = eegData[:,Time_after[j]:Time_after[j] + epochSampleNum]
            for i in range(nChannel):
                Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time_after[j]:Time_base[j]]))
        return [Epochs,Num[0]]
    
def EpochingNum(eegData, stims, code, samplingRate, nChannel, epochSampleNum, epochOffset,baseline, epochNum):
        Time = stims[np.where(stims[:,1] == code),0][0]
        Time = np.floor(np.multiply(Time,samplingRate)).astype(int)
        Time_after = np.add(Time,epochOffset).astype(int)
        Time_base = np.add(Time,baseline).astype(int)
        Epochs = np.zeros((epochNum, nChannel, epochSampleNum))
        for j in range(epochNum):
            Epochs[j, :, :] = eegData[:,Time_after[j]:Time_after[j] + epochSampleNum]
            for i in range(nChannel):
                Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time_after[j]:Time_base[j]]))
        return [Epochs,epochNum]

def DownsamplingOnlineEpoch(Epochs1, Epochs2, Epochs3, Epochs4, Epochs5, Epochs6, downsampleRate):
        num = np.floor(Epochs1.shape[2] / downsampleRate).astype(int)
        Downsampled1 = np.zeros((Epochs1.shape[0],Epochs1.shape[1],num))
        Downsampled2 = np.zeros((Epochs2.shape[0],Epochs2.shape[1],num))
        Downsampled3 = np.zeros((Epochs3.shape[0],Epochs3.shape[1],num))
        Downsampled4 = np.zeros((Epochs4.shape[0],Epochs4.shape[1],num))
        Downsampled5 = np.zeros((Epochs5.shape[0],Epochs5.shape[1],num))
        Downsampled6 = np.zeros((Epochs6.shape[0],Epochs6.shape[1],num))
        for i in range(num):
            for j in range(Epochs1.shape[1]):
                for k in range(Epochs1.shape[0]):
                    Downsampled1[k,j,i] = np.mean(Epochs1[k,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
                    Downsampled2[k,j,i] = np.mean(Epochs2[k,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
                    Downsampled3[k,j,i] = np.mean(Epochs3[k,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
                    Downsampled4[k,j,i] = np.mean(Epochs4[k,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
                    Downsampled5[k,j,i] = np.mean(Epochs5[k,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
                    Downsampled6[k,j,i] = np.mean(Epochs6[k,j,i*downsampleRate:(i+1)*downsampleRate],dtype=np.float64)
        return [Downsampled1, Downsampled2, Downsampled3, Downsampled4, Downsampled5, Downsampled6, num]

def CNNComputeTarget(eegData, stims, samplingFreq, channelNum, model, Trior):
#        sampleNum = eegData.shape[1]
        downsampleRate = 4
        
        Downsampling(eegData, downsampleRate)
        samplingFreq = samplingFreq/4
        sampleNum = eegData.shape[1]
        
        #Common Average Reference
        eegData = Re_referencing(eegData, channelNum, sampleNum)

        #Bandpass Filter
        eegData = butter_bandpass_filter(eegData, 0.5, 10, samplingFreq, 4)

        #Epoching
        epochSampleNum = int(np.floor(1.0 * samplingFreq))
        offset = int(np.floor(0.1 * samplingFreq))
        baseline = int(np.floor(1.1 * samplingFreq))
        [Epochs1, Num1] = EpochingNum(eegData, stims, 1, samplingFreq, channelNum, epochSampleNum, offset, baseline, Trior)
        [Epochs2, Num2] = EpochingNum(eegData, stims, 2, samplingFreq, channelNum, epochSampleNum, offset, baseline, Trior)
        [Epochs3, Num3] = EpochingNum(eegData, stims, 3, samplingFreq, channelNum, epochSampleNum, offset, baseline, Trior)
        [Epochs4, Num4] = EpochingNum(eegData, stims, 4, samplingFreq, channelNum, epochSampleNum, offset, baseline, Trior)
        [Epochs5, Num5] = EpochingNum(eegData, stims, 5, samplingFreq, channelNum, epochSampleNum, offset, baseline, Trior)
        [Epochs6, Num6] = EpochingNum(eegData, stims, 6, samplingFreq, channelNum, epochSampleNum, offset, baseline, Trior)

        #Downsampling Epochs
        [Epochs1,Epochs2,Epochs3,Epochs4,Epochs5,Epochs6,epochSampleNum] = DownsamplingOnlineEpoch(Epochs1, Epochs2, Epochs3, Epochs4, Epochs5, Epochs6, downsampleRate)
        samplingFreq = samplingFreq/4

        result = np.zeros((1,6))

        Epochs1 = np.reshape(Epochs1, (Num1,1,channelNum,epochSampleNum))
        Epochs2 = np.reshape(Epochs2, (Num2,1,channelNum,epochSampleNum))
        Epochs3 = np.reshape(Epochs3, (Num3,1,channelNum,epochSampleNum))
        Epochs4 = np.reshape(Epochs4, (Num4,1,channelNum,epochSampleNum))
        Epochs5 = np.reshape(Epochs5, (Num5,1,channelNum,epochSampleNum))
        Epochs6 = np.reshape(Epochs6, (Num6,1,channelNum,epochSampleNum))

        a1 = model.predict(Epochs1)
        a2 = model.predict(Epochs2)
        a3 = model.predict(Epochs3)
        a4 = model.predict(Epochs4)
        a5 = model.predict(Epochs5)
        a6 = model.predict(Epochs6)

        result[0,0] = np.sum(a1[:,1])
        result[0,1] = np.sum(a2[:,1])
        result[0,2] = np.sum(a3[:,1])
        result[0,3] = np.sum(a4[:,1])
        result[0,4] = np.sum(a5[:,1])
        result[0,5] = np.sum(a6[:,1])

        answer = np.argmax(result) + 1
        print(result)
        return answer

def main():
        ###ZeroCNN: Compute accuracy of user data on specific triors
        UserData_Path = "C:/Users/user/WorldSystem/UserData"
        Target_list = []
            #They are stored in the list in the order they are stored.
        Target_list = sorted(glob.glob(UserData_Path + '/*'), key=os.path.getmtime)
        UserNum = np.shape(Target_list)[0]
        Accuracy = np.zeros((UserNum,5))
        samplingFreq = 2048
        channelNum = 32
        model = load_model('C:/Users/user/WorldSystem/Zero/ZeroModel/ZeroCNN3.h5')
        for i in range(0,UserNum):
            print(str(Target_list[i][35:]))
            ZeroData_Path = []
            ZeroData_Path = sorted(glob.glob(Target_list[i] + '/ZeroData/*.mat'), key=os.path.getmtime)
            ZeroTarget_Path = []            
#            ZeroStims_Path = []
            ZeroTarget_Path = glob.glob(Target_list[i] + '/ZeroTarget/*.txt')
#            ZeroData_Path = sorted(glob.glob(Target_list[i] + '/ZeroData/txt_files/eegData/*.out'), key=os.path.getmtime)
#            ZeroStims_Path = sorted(glob.glob(Target_list[i] + '/ZeroData/txt_files/stims/*.out'), key=os.path.getmtime)
            
            ##Result txt file read in order to get orders
            OT = []
            [TryO, OT] = Readtxt(ZeroTarget_Path[0])
            Trior = 1
            ##Find Session Accuracy
            for l in range(0, 5):
                print("Epoch number:",Trior)
                CorrectO = 0
                for k in range(0, TryO):
                    mat = hdf5storage.loadmat(ZeroData_Path[k])
                    eegData = mat['eegData']
                    stims = mat['stims']
                    eegData = np.transpose(eegData)                    
                    
#                    eegData = np.loadtxt(ZeroData_Path[k], delimiter = ",")
#                    stims = np.loadtxt(ZeroStims_Path[k], delimiter = ",")
                    result = CNNComputeTarget(eegData, stims, samplingFreq, channelNum, model, Trior)
                    if(OT[k][7] == str(result)):
                        CorrectO = CorrectO + 1
                    print("Target:",OT[k][7])
                    print("result:",result)
                Accuracy[i,l] = CorrectO/TryO
                if(l == 0):
                    Trior = Trior * 5
                else:
                    Trior = Trior + 5
            print("Acc:",Accuracy[i,:])
        print("All patient:")
        print(Accuracy)
        print("Acc mean")
        np.mean(Accuracy,axis=0)
            
if __name__ == "__main__":
    main()