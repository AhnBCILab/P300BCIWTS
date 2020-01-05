import numpy as np
from scipy.signal import butter, lfilter
import os, glob
import pickle
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.externals import joblib

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
    
#def Epoching(eegData, stims, code, samplingRate, nChannel, epochSampleNum, epochOffset, baseline):
#        Time = stims[np.where(stims[:,1] == code),0][0]
#        Time = np.floor(np.multiply(Time,samplingRate)).astype(int)
#        Time_offset = np.add(Time,epochOffset).astype(int)
#        Time_base = np.subtract(Time,baseline).astype(int)
##        Time_base = np.add(Time,baseline).astype(int)
#        Num = Time.shape
#        Epochs = np.zeros((Num[0], nChannel, epochSampleNum))
#        for j in range(Num[0]):
#            Epochs[j, :, :] = eegData[:,Time_offset[j]:Time_offset[j] + epochSampleNum]
#            for i in range(nChannel):
#                Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time_base[j]:Time[j]]))
#        return [Epochs,Num[0]]

#def EpochingNum(eegData, stims, code, samplingRate, nChannel, epochSampleNum, epochOffset, baseline, epochNum): # [-100 100]
#        Time = stims[np.where(stims[:,1] == code),0][0]
#        Time = np.floor(np.multiply(Time,samplingRate)).astype(int)
#        Time_offset = np.add(Time,epochOffset).astype(int)
#        Time_base = np.subtract(Time,baseline).astype(int)
##        Time_base = np.add(Time,baseline).astype(int)
##        Num = Time.shape
#        Epochs = np.zeros((epochNum, nChannel, epochSampleNum))
#        for j in range(epochNum):
#            Epochs[j, :, :] = eegData[:,Time_offset[j]:Time_offset[j] + epochSampleNum]
#            for i in range(nChannel):
#                Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time_base[j]:Time_offset[j]]))
#        return [Epochs,epochNum]

#def Epoching(eegData, stims, code, samplingRate, nChannel, epochSampleNum, epochOffset,baseline): # [0 100]
#        Time = stims[np.where(stims[:,1] == code),0][0]
#        Time = np.floor(np.multiply(Time,samplingRate)).astype(int)
#        Time_after = np.add(Time,epochOffset).astype(int)
#        Time_base = np.add(Time,baseline).astype(int)
#        Num = Time.shape
#        Epochs = np.zeros((Num[0], nChannel, epochSampleNum))
#        for j in range(Num[0]):
#            Epochs[j, :, :] = eegData[:,Time_after[j]:Time_after[j] + epochSampleNum]
#            for i in range(nChannel):
#                Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time[j]:Time_base[j]]))
#        return [Epochs,Num[0]]
    
#def EpochingNum(eegData, stims, code, samplingRate, nChannel, epochSampleNum, epochOffset, baseline, epochNum):
#        Time = stims[np.where(stims[:,1] == code),0][0]
#        Time = np.floor(np.multiply(Time,samplingRate)).astype(int)
#        Time_offset = np.add(Time,epochOffset).astype(int)
#        Time_base = np.subtract(Time,baseline).astype(int)
##        Time_base = np.add(Time,baseline).astype(int)
#        Epochs = np.zeros((epochNum, nChannel, epochSampleNum))
#        for j in range(epochNum):
#            Epochs[j, :, :] = eegData[:,Time_offset[j]:Time_offset[j] + epochSampleNum]
#            for i in range(nChannel):
#                Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time_base[j]:Time[j]]))
#        return [Epochs,epochNum]

def EpochingNum(eegData, stims, code, samplingRate, nChannel, epochSampleNum, epochOffset,baseline, epochNum): # [100 700]
        Time = stims[np.where(stims[:,1] == code),0][0]
        Time = np.floor(np.multiply(Time,samplingRate)).astype(int)
        Time_after = np.add(Time,epochOffset).astype(int)
        Time_base = np.add(Time,baseline).astype(int)
#        Num = Time.shape
        Epochs = np.zeros((epochNum, nChannel, epochSampleNum))
        for j in range(epochNum):
            Epochs[j, :, :] = eegData[:,Time_after[j]:Time_after[j] + epochSampleNum]
#            for i in range(nChannel):
#                Epochs[j, i, :] = np.subtract(Epochs[j, i, :], np.mean(eegData[i,Time_after[j]:Time_base[j]]))
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

def Online_Convert_to_featureVector(Epochs1, Epochs2, Epochs3, Epochs4, Epochs5, Epochs6, Num, featureNum):
        Features1 = np.zeros((Num, featureNum))
        for i in range(Num):
            Features1[i,:] = np.reshape(Epochs1[i,:,:],(1,featureNum))
        Features2 = np.zeros((Num, featureNum))
        for i in range(Num):
            Features2[i,:] = np.reshape(Epochs2[i,:,:],(1,featureNum))
        Features3 = np.zeros((Num, featureNum))
        for i in range(Num):
            Features3[i,:] = np.reshape(Epochs3[i,:,:],(1,featureNum))
        Features4 = np.zeros((Num, featureNum))
        for i in range(Num):
            Features4[i,:] = np.reshape(Epochs4[i,:,:],(1,featureNum))
        Features5 = np.zeros((Num, featureNum))
        for i in range(Num):
            Features5[i,:] = np.reshape(Epochs5[i,:,:],(1,featureNum))
        Features6 = np.zeros((Num, featureNum))
        for i in range(Num):
            Features6[i,:] = np.reshape(Epochs6[i,:,:],(1,featureNum))
            
        return [Features1,Features2,Features3,Features4,Features5,Features6]
    
def SWLDAComputeTarget(eegData, stims, samplingFreq, channelNum, SelectedFeatures, lda, Trior):
        sampleNum = eegData.shape[1]
        downsampleRate = 4
        
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
    
        #Convert a feature vector
        featureNum = channelNum*epochSampleNum
        [Features1, Features2, Features3, Features4, Features5, Features6] = Online_Convert_to_featureVector(Epochs1, Epochs2, Epochs3, Epochs4, Epochs5, Epochs6, Num1, featureNum)        

        #Classification process
        result = np.zeros((1,6))
        Features1 = Features1[:,SelectedFeatures]
        Features2 = Features2[:,SelectedFeatures]
        Features3 = Features3[:,SelectedFeatures]
        Features4 = Features4[:,SelectedFeatures]
        Features5 = Features5[:,SelectedFeatures]
        Features6 = Features6[:,SelectedFeatures]

        but1_pred = lda.predict(Features1)
        but2_pred = lda.predict(Features2)
        but3_pred = lda.predict(Features3)
        but4_pred = lda.predict(Features4)
        but5_pred = lda.predict(Features5)
        but6_pred = lda.predict(Features6)

        result[0,0] = np.sum(but1_pred)
        result[0,1] = np.sum(but2_pred)
        result[0,2] = np.sum(but3_pred)
        result[0,3] = np.sum(but4_pred)
        result[0,4] = np.sum(but5_pred)
        result[0,5] = np.sum(but6_pred)

        answer = np.argmax(result) + 1
        print(result)
        return answer

def main():
        ###SWLDA: Compute accuracy of user data on specific triors
        UserData_Path = "C:/Users/user/WorldSystem/UserData"
        Target_list = []
            #They are stored in the list in the order they are stored.
        Target_list = sorted(glob.glob(UserData_Path + '/*'), key=os.path.getmtime)
        UserNum = np.shape(Target_list)[0]
        Accuracy = np.zeros((UserNum,5))
        samplingFreq = 512
        channelNum = 32
        for i in range(0,UserNum):
            print(str(Target_list[i][35:]))
            OnlineTarget_Path = []
            OnlineData_Path = []
            OnlineStims_Path = []
            SelectedFeatures_Path = []
            Classifier_Path = []
            OnlineTarget_Path = glob.glob(Target_list[i] + '/OnlineTarget/*.txt')
            OnlineData_Path = sorted(glob.glob(Target_list[i] + '/OnlineData/txt_files/eegData/*.out'), key=os.path.getmtime)
            OnlineStims_Path = sorted(glob.glob(Target_list[i] + '/OnlineData/txt_files/stims/*.out'), key=os.path.getmtime)
            SelectedFeatures_Path = sorted(glob.glob(Target_list[i] + '/TrainData/SelectedFeatures/*.pickle'), key=os.path.getmtime)
            Classifier_Path = sorted(glob.glob(Target_list[i] + '/TrainData/Classifier/*.pickle'), key=os.path.getmtime)
            
            with open(SelectedFeatures_Path[10], 'rb') as f:
                SelectedFeatures = pickle.load(f)
            lda = LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto')
            lda = joblib.load(Classifier_Path[10])
            
            ##Result txt file read in order to get orders
            OT = []
            [TryO, OT] = Readtxt(OnlineTarget_Path[0])
            Trior = 1
            ##Find Session Accuracy
            for l in range(0, 5):
                print("Epoch number:",Trior)
                CorrectO = 0
                for k in range(0, TryO):
                    eegData = np.loadtxt(OnlineData_Path[k], delimiter = ",")
                    stims = np.loadtxt(OnlineStims_Path[k], delimiter = ",")
                    result = SWLDAComputeTarget(eegData, stims, samplingFreq, channelNum, SelectedFeatures, lda, Trior)
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
        print(np.mean(Accuracy,axis=0))
        
if __name__ == "__main__":
    main()