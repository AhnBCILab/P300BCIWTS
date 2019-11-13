import numpy as np
from scipy.signal import butter, lfilter
import time
import os
from keras.models import load_model

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

def main():
        #load cnn model and predict result
        model = load_model('C:/Users/wldk5/WorldSystem/Zero/ZeroModel/ZeroCNN.h5')
#        global file_exist, file1, file2, channelNum
        eegData_txt = 'C:/Users/wldk5/WorldSystem/Zero/CNNtemp/eegData.out'
        stims_txt = 'C:/Users/wldk5/WorldSystem/Zero/CNNtemp/stims.out'
        start_txt = 'C:/Users/wldk5/WorldSystem/Zero/CNNtemp/start.out'
        result_txt = 'C:/Users/wldk5/WorldSystem/Zero/CNNtemp/result.out'
        
        while True:
            #load text file
            while True:
                if os.path.isfile(start_txt):
                    break
            start_time = time.time()
            
            while(time.time() - start_time < 35):
                pass
            if os.path.isfile(result_txt):
                        os.remove(eegData_txt)
                        os.remove(stims_txt)
                        os.remove(result_txt)
            while True:
                if os.path.isfile(eegData_txt) & os.path.isfile(stims_txt):
                    processing_time = time.time()
                    os.remove(start_txt)
                    eegData = np.loadtxt(eegData_txt, delimiter = ",")
                    stims = np.loadtxt(stims_txt, delimiter = ",")
                    break
            print("got process")
            ### Preprocessing process
            channelNum = 32
            samplingFreq = 512
            downsampleRate = 4
            
            sampleNum = eegData.shape[1]
            
            #Downsampling
            eegData = Re_referencing(eegData, channelNum, sampleNum)

            #Bandpass Filter
            eegData = butter_bandpass_filter(eegData, 0.5, 10, samplingFreq, 4)
            
            #Epoching
            epochSampleNum = int(np.floor(0.4 * samplingFreq))
            offset = int(np.floor(0.3 * samplingFreq))
            baseline = int(np.floor(0.7 * samplingFreq))
            [Epochs1, Num1] = Epoching(eegData, stims, 1, samplingFreq, channelNum, epochSampleNum, offset, baseline)
            [Epochs2, Num2] = Epoching(eegData, stims, 2, samplingFreq, channelNum, epochSampleNum, offset, baseline)
            [Epochs3, Num3] = Epoching(eegData, stims, 3, samplingFreq, channelNum, epochSampleNum, offset, baseline)
            [Epochs4, Num4] = Epoching(eegData, stims, 4, samplingFreq, channelNum, epochSampleNum, offset, baseline)
            [Epochs5, Num5] = Epoching(eegData, stims, 5, samplingFreq, channelNum, epochSampleNum, offset, baseline)
            [Epochs6, Num6] = Epoching(eegData, stims, 6, samplingFreq, channelNum, epochSampleNum, offset, baseline)
            
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
            answer = [answer]
            
            np.savetxt(result_txt, answer)
            print("Process time: ", time.time() - processing_time)
                    
if __name__ == "__main__":
    main()