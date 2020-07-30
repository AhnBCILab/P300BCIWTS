import numpy as np
from scipy.signal import butter, lfilter, sosfiltfilt
import time
import os, glob
import shutil
from datetime import datetime
import socket
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.externals import joblib
import pickle

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
        sos = butter(order, [low, high], btype='band', output='sos')
        return sos
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        sos = butter_bandpass(lowcut, highcut, fs, order=order)
        y = sosfiltfilt(sos, data)
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

def main():
#        global file_exist, file1, file2, channelNum
        eegData_txt = 'WorldSystem/Within/Onlinetemp/eegData.out'
        stims_txt = 'WorldSystem/Within/Onlinetemp/stims.out'
        start_txt = 'WorldSystem/Within/Onlinetemp/start.out'
        moveData_eeg = 'WorldSystem/Within/Online/Data/txt_files/eegData/'
        moveData_stims = 'WorldSystem/Within/Online/Data/txt_files/stims/'
        
        channelNum = 32
        downsampleRate = 4
        
        serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSock.bind(('', 12240))
        serverSock.listen(0)
        connectionSock, addr = serverSock.accept()
        print('The connection has been confirmed at',str(addr))
        
        #Load lda classifier and selected features
        SelectedF_path = 'WorldSystem/Within/StepWise/Features/'
        Classifier_path = 'WorldSystem/Within/StepWise/Classifiers/'
        
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
        
        for i in range(0, 12):
            samplingFreq = 512
            #load text file
            while True:
                if os.path.isfile(start_txt):
                    break
            start_time = time.time()
            
            while(time.time() - start_time < 25):
                pass
            
            while True:
                if os.path.isfile(eegData_txt) & os.path.isfile(stims_txt):
                    processing_time = time.time()
                    os.remove(start_txt)
                    eegData = np.loadtxt(eegData_txt, delimiter = ",")
                    stims = np.loadtxt(stims_txt, delimiter = ",")
                    ctime = datetime.today().strftime("%m%d_%H%M%S")
                    moveData_e = moveData_eeg + ctime + 'eegData.out'
                    moveData_s = moveData_stims + ctime + 'stims.out'
                    shutil.move(eegData_txt, moveData_e)
                    shutil.move(stims_txt, moveData_s)
                    break
            print("got process")
            
            ### Preprocessing process
            ##EEG Preprocessing        
            sampleNum = eegData.shape[1]
            
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
            
            print("Process time: ", time.time() - processing_time)
            print("Result: ", answer)
            print("status: ", result)
            connectionSock.send(str(answer).encode("utf-8"))
            
if __name__ == "__main__":
    main()