import numpy as np
from scipy.signal import butter, lfilter
import time
import os, glob
import pickle
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.externals import joblib

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

def Convert_to_featureVector(EpochsT, NumT, EpochsN, NumN, featureNum):
        FeaturesT = np.zeros((NumT, featureNum))
        for i in range(NumT):
            FeaturesT[i,:] = np.reshape(EpochsT[i,:,:],(1,featureNum))
        FeaturesN = np.zeros((NumN, featureNum))
        for j in range(NumN):
            FeaturesN[j,:] = np.reshape(EpochsN[j,:,:],(1,featureNum))
        return [FeaturesT,FeaturesN]

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
                            
def SaveFullTrainingFeatures(eegData, stims, samplingFreq, channelNum, filename):
        
        downsampleRate = 4
        
        eegData = Re_referencing(eegData, channelNum, sampleNum)

        #Bandpass Filter
        eegData = butter_bandpass_filter(eegData, 0.5, 10, samplingFreq,4)
    
        #Epoching
        epochSampleNum = int(np.floor(0.4 * samplingFreq))
        offset = int(np.floor(0.2 * samplingFreq))
        baseline = int(np.floor(0.6 * samplingFreq))
        [EpochsT, NumT] = Epoching(eegData, stims, 1, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [EpochsN, NumN] = Epoching(eegData, stims, 0, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        #Convert to feature vector
        featureNum = channelNum*epochSampleNum
        [FeaturesT, FeaturesN] = Convert_to_featureVector(EpochsT, NumT, EpochsN, NumN, featureNum)
        TrainData = np.concatenate((FeaturesT, FeaturesN))
        TrainLabel = np.concatenate((np.ones((NumT,1)).astype(int),np.zeros((NumN,1)).astype(int))).ravel()
        #Save features
        with open(filename,'wb') as f:
            pickle.dump([TrainData, TrainLabel], f) # Saving eeg data

def save_data(eegData, stims, eegData_txt, stims_txt):
        np.savetxt(eegData_txt, eegData, delimiter = ",")
        np.savetxt(stims_txt, stims, delimiter = ",")

def start_txt_trigger(start_txt):
        np.savetxt(start_txt, [1])

def delay(sec):
        time.sleep(sec)

def load_result(result_txt):
        if os.path.isfile(result_txt):
            result = np.loadtxt(result_txt)
            return result
        
def classify(eegData, stims, samplingFreq, channelNum): ### Online Preprocessing code
        #Load lda classifier and selected features
        SelectedF_path = 'C:/Users/wldk5/WorldSystem/Within/StepWise/Features/'
        Classifier_path = 'C:/Users/wldk5/WorldSystem/Within/StepWise/Classifiers/'
        
        current_list = []
        current_list = sorted(glob.glob(SelectedF_path + '*.pickle'), key=os.path.getmtime, reverse=True)
        SelectedF_real = current_list[0]
        with open(SelectedF_real, 'rb') as f:
            SelectedFeatures = pickle.load(f)
        
        current_list2 = []
        current_list2 = sorted(glob.glob(Classifier_path + '*.pickle'), key=os.path.getmtime, reverse=True)
        Classifier_real = current_list2[0]
        lda = LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto')
        lda = joblib.load(Classifier_real)

        ##EEG Preprocessing        
        sampleNum = eegData.shape[1]
        
        downsampleRate = 4
        
        #Common Average Reference
        eegData = Re_referencing(eegData, channelNum, sampleNum)

        #Bandpass Filter
        eegData = butter_bandpass_filter(eegData, 0.5, 10, samplingFreq,4)
        
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
        
        #Convert o feature vector
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
        return answer