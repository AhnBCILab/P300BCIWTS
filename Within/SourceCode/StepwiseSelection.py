import numpy as np
import pickle
import pandas as pd
import statsmodels.api as sm
import hdf5storage
from scipy.signal import butter, lfilter, sosfiltfilt
import os, glob, time
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# import matlab.engine
from datetime import datetime
from sklearn.externals import joblib


def stepwise_selection(X, y, 
                       initial_list=[], 
                       threshold_in=0.01, 
                       threshold_out = 0.05, 
                       verbose=True):
    """ The original author of stepwise_selection is: https://datascience.stackexchange.com/users/24162/david-dale
    It perform a forward-backward feature selection 
    based on p-value from statsmodels.api.OLS
    Arguments:
        X - pandas.DataFrame with candidate features
        y - list-like with the target
        initial_list - list of features to start with (column names of X)
        threshold_in - include a feature if its p-value < threshold_in
        threshold_out - exclude a feature if its p-value > threshold_out
        verbose - whether to print the sequence of inclusions and exclusions
    Returns: list of selected features 
    Always set threshold_in < threshold_out to avoid infinite looping.
    See https://en.wikipedia.org/wiki/Stepwise_regression for the details
    """
    included = list(initial_list)
    while True:
        changed=False
        # forward step
        excluded = list(set(X.columns)-set(included))
        new_pval = pd.Series(index=excluded)
        for new_column in excluded:
            model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included+[new_column]]))).fit()
            new_pval[new_column] = model.pvalues[new_column]
        best_pval = new_pval.min()
        if best_pval < threshold_in:
            best_feature = new_pval.idxmin()
            included.append(best_feature)
            changed=True
            if verbose:
                print('Add  {:30} with p-value {:.6}'.format(best_feature, best_pval))

        # backward step
        model = sm.OLS(y, sm.add_constant(pd.DataFrame(X[included]))).fit()
        # use all coefs except intercept
        pvalues = model.pvalues.iloc[1:]
        worst_pval = pvalues.max() # null if pvalues is empty
        if worst_pval > threshold_out:
            changed=True
            worst_feature = pvalues.idxmax()
            included.remove(worst_feature)
            if verbose:
                print('Drop {:30} with p-value {:.6}'.format(worst_feature, worst_pval))
        if not changed:
            break
    return included

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

def Convert_to_featureVector(EpochsT, NumT, EpochsN, NumN, featureNum):
        FeaturesT = np.zeros((NumT, featureNum))
        for i in range(NumT):
            FeaturesT[i,:] = np.reshape(EpochsT[i,:,:],(1,featureNum))
        FeaturesN = np.zeros((NumN, featureNum))
        for j in range(NumN):
            FeaturesN[j,:] = np.reshape(EpochsN[j,:,:],(1,featureNum))
        return [FeaturesT,FeaturesN]
    


def main():
        start = time.time()
        
        ##Generate Preprocessing Training data
        ctime = datetime.today().strftime("%m%d_%H%M")
        SelectedF_path = 'D:/WorldSystem/Within/StepWise/Features/' + ctime + 'SelectedFeatures.pickle'
        Classifier_path = 'D:/WorldSystem/Within/StepWise/Classifiers/' + ctime + 'Classifier.pickle'
        
        channelNum = 32
        downsampleRate = 4
        
        ov_Path = "C:/Users/wldk5/WorldSystem/Within/Training/Data/"
        current_list = []
        current_list = sorted(glob.glob(ov_Path + '*.ov'), key=os.path.getmtime, reverse=True)
        ovfile_name = current_list[0]
        matfile_name = current_list[0][:-3] + ".mat"
        # matfile_name = "D:/WorldSystem/Within/Training\Data/Training-[2020.06.25-22.15.42].mat"
        
        # print("current ov file path:", current_list[0])
        # eng = matlab.engine.start_matlab()
        # k = eng.convert_ov2mat(ovfile_name, matfile_name)
        mat = hdf5storage.loadmat(matfile_name)
        channelNames = mat['channelNames']
        eegData = mat['eegData']
        samplingFreq = mat['samplingFreq']
        samplingFreq = samplingFreq[0,0]
        stims = mat['stims']
        channelNum = channelNames.shape
        channelNum = channelNum[1]
        eegData = np.transpose(eegData)
        
        ##Preprocessing process
        eegData = Downsampling(eegData, downsampleRate)
        samplingFreq = samplingFreq/4
        sampleNum = eegData.shape[1]
        
        #Common Average Reference
        eegData = Re_referencing(eegData, channelNum, sampleNum)

        #Bandpass Filter
        eegData = butter_bandpass_filter(eegData, 0.5, 10, samplingFreq,4)
    
        #Epoching
        epochSampleNum = int(np.floor(0.4 * samplingFreq))
        offset = int(np.floor(0.2 * samplingFreq))
        baseline = int(np.floor(0.6 * samplingFreq))
        [EpochsT, NumT] = Epoching(eegData, stims, 1, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        [EpochsN, NumN] = Epoching(eegData, stims, 0, samplingFreq, channelNum, epochSampleNum, offset, baseline)
        
        #DownsamplingEpoch
        [EpochsT,EpochsN,epochSampleNum] = DownsamplingEpoch(EpochsT, EpochsN, downsampleRate)
        
        #Convert to feature vector
        featureNum = channelNum*epochSampleNum
        [FeaturesT, FeaturesN] = Convert_to_featureVector(EpochsT, NumT, EpochsN, NumN, featureNum)
        TrainData = np.concatenate((FeaturesT, FeaturesN))
        TrainLabel = np.concatenate((np.ones((NumT,1)).astype(int),np.zeros((NumN,1)).astype(int))).ravel()
        
        #Feature Selection process
        x = np.arange(featureNum)
        Data = pd.DataFrame(TrainData ,columns=x)
        SelectedFeatures = stepwise_selection(Data, TrainLabel)
        print('resulting features:')
        SelectedFeatures = np.sort(SelectedFeatures)
        print(SelectedFeatures)
        SWTrainData = TrainData[:,SelectedFeatures]
        
        #Saving LDA classifier and Selected features
        lda = LinearDiscriminantAnalysis(solver='lsqr',shrinkage='auto')
        lda.fit(SWTrainData, TrainLabel)
        joblib.dump(lda, Classifier_path)
        with open(SelectedF_path, 'wb') as f:
            pickle.dump(SelectedFeatures, f)
        #print(SelectedFeatures)
        print("time :", time.time() - start)
        
if __name__ == "__main__":
    main()