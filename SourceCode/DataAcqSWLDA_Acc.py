import numpy as np
from scipy.signal import butter, lfilter
import os, glob
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.externals import joblib
import matlab.engine
import hdf5storage
import pickle

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
    
def DifISI_SWLDAComputeTarget(eegData, stims, samplingFreq, channelNum, SelectedFeatures, lda, Trior):
        downsampleRate = 4
        
        #Downsampling
        eegData = Downsampling(eegData, downsampleRate)
        samplingFreq = samplingFreq/4
        sampleNum = eegData.shape[1]
        
        #Common Average Reference
        eegData = Re_referencing(eegData, channelNum, sampleNum)

        #Bandpass Filter
        eegData = butter_bandpass_filter(eegData, 0.5, 10, samplingFreq, 4)

        #Epoching
        epochSampleNum = int(np.floor(0.4 * samplingFreq))
        offset = int(np.floor(0.2 * samplingFreq))
        baseline = int(np.floor(0.6 * samplingFreq))
        [Epochs1, Num1] = Epoching(eegData, stims, 1, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [Epochs2, Num2] = Epoching(eegData, stims, 2, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [Epochs3, Num3] = Epoching(eegData, stims, 3, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [Epochs4, Num4] = Epoching(eegData, stims, 4, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [Epochs5, Num5] = Epoching(eegData, stims, 5, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [Epochs6, Num6] = Epoching(eegData, stims, 6, samplingFreq, channelNum, epochSampleNum, offset, baseline)

        #Downsampling Epochs
        [Epochs1,Epochs2,Epochs3,Epochs4,Epochs5,Epochs6,epochSampleNum] = DownsamplingOnlineEpoch(Epochs1, Epochs2, Epochs3, Epochs4, Epochs5, Epochs6, downsampleRate)
        samplingFreq = samplingFreq/4
        
        #Convert a feature vector
        featureNum = channelNum*epochSampleNum
        [Features1, Features2, Features3, Features4, Features5, Features6] = Online_Convert_to_featureVector(Epochs1, Epochs2, Epochs3, Epochs4, Epochs5, Epochs6, Num1, featureNum)        

        print(np.shape(Features1))
        #Classification process
        result = np.zeros((1,6))
        Features1 = Features1[:,SelectedFeatures]
        Features2 = Features2[:,SelectedFeatures]
        Features3 = Features3[:,SelectedFeatures]
        Features4 = Features4[:,SelectedFeatures]
        Features5 = Features5[:,SelectedFeatures]
        Features6 = Features6[:,SelectedFeatures]

        result = np.zeros((6,6))
        answer = np.zeros((1,6))
        
        for sessionNum in range(0,6):
            print("sessionBound:",sessionNum*20,(sessionNum+1)*20)
            F1 = Features1[sessionNum*20:(sessionNum+1)*20]
            F2 = Features2[sessionNum*20:(sessionNum+1)*20]
            F3 = Features3[sessionNum*20:(sessionNum+1)*20]
            F4 = Features4[sessionNum*20:(sessionNum+1)*20]
            F5 = Features5[sessionNum*20:(sessionNum+1)*20]
            F6 = Features6[sessionNum*20:(sessionNum+1)*20]
            
            a1 = lda.predict(F1[0:Trior])
            a2 = lda.predict(F2[0:Trior])
            a3 = lda.predict(F3[0:Trior])
            a4 = lda.predict(F4[0:Trior])
            a5 = lda.predict(F5[0:Trior])
            a6 = lda.predict(F6[0:Trior])
            
            result[sessionNum,0] = np.sum(a1)
            result[sessionNum,1] = np.sum(a2)
            result[sessionNum,2] = np.sum(a3)
            result[sessionNum,3] = np.sum(a4)
            result[sessionNum,4] = np.sum(a5)
            result[sessionNum,5] = np.sum(a6)
            
            answer[0,sessionNum] = np.argmax(result[sessionNum,:]) + 1
        print("result",result)
        print("answer:", answer)
        RealAnswer = [1.0,2.0,3.0,4.0,5.0,6.0]
        boolAns = np.equal(RealAnswer,answer)
        print("boolAns:",boolAns)
        Accuracy = np.count_nonzero(boolAns) / 6
        print("Accuracy:",Accuracy)
        return Accuracy

def main():
        ###Different ISI SWLDA: Compute accuracy of user data on specific triors
        UserData_Path = "C:/Users/user/WorldSystem/UserData"
        Target_list = []
            #They are stored in the list in the order they are stored.
        Target_list = sorted(glob.glob(UserData_Path + '/*'), key=os.path.getmtime)
        UserNum = np.shape(Target_list)[0]
        Accuracy = np.zeros((UserNum,2,5))
        for i in range(0,UserNum):
            print(str(Target_list[i][35:]))
            current_list = []
            SelectedFeatures_Path = []
            Classifier_Path = []
            current_list = glob.glob(Target_list[i] + '/AcquiredData/*.ov')
            SelectedFeatures_Path = sorted(glob.glob(Target_list[i] + '/TrainData/SelectedFeatures/*.pickle'), key=os.path.getmtime)
            Classifier_Path = sorted(glob.glob(Target_list[i] + '/TrainData/Classifier/*.pickle'), key=os.path.getmtime)
            
            with open(SelectedFeatures_Path[3], 'rb') as f:
                SelectedFeatures = pickle.load(f)
            lda = LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto')
            lda = joblib.load(Classifier_Path[3])
            
            for t in range(0,2):
                print("Data num:",t)
            
                ovfile_name = current_list[t]
                matfile_name = current_list[t][:-3] + ".mat"
        
                print("current ov file path:", current_list[t])
        #         eng = matlab.engine.start_matlab()
        #         k = eng.convert_ov2mat(ovfile_name, matfile_name)
                mat = hdf5storage.loadmat(matfile_name)
                channelNames = mat['channelNames']
                eegData = mat['eegData']
                samplingFreq = mat['samplingFreq']
                samplingFreq = samplingFreq[0,0]
                stims = mat['stims']
                channelNum = channelNames.shape
                channelNum = channelNum[1]
                eegData = np.transpose(eegData)
            
                ##Result txt file read in order to get orders
                Trior = 1
                ##Find Session Accuracy
                for l in range(0, 5):
                    print("\nEpoch number:",Trior)
                    Accuracy[i,t,l] = DifISI_SWLDAComputeTarget(eegData, stims, samplingFreq, channelNum, SelectedFeatures, lda, Trior)
                    if(l == 0):
                        Trior = Trior * 5
                    else:
                        Trior = Trior + 5
                        
            print("Acc for no.1:",Accuracy[i,0,:])
            print("Acc for no.2:",Accuracy[i,1,:])
            print("\n")
        print("Finish")
        for t in range(0, UserNum):
            print(print(str(Target_list[t][35:])))
            print(Accuracy[t])
        print("Acc mean")
        print(np.mean(Accuracy,axis=0))
            
if __name__ == "__main__":
    main()