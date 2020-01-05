import os, glob
import shutil
import numpy as np

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

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

def main():
        start_txt = 'C:/Users/wldk5/WorldSystem/Zero/CNNtemp/start.out'
        if os.path.isfile(start_txt):
            os.remove(start_txt)
    
        ##Generate User folder
        RootPath = "C:/Users/wldk5/WorldSystem/UserData/"
        RestingState_Path = "C:/Users/wldk5/WorldSystem/RestingState/"
        TrainingData_Path = "C:/Users/wldk5/WorldSystem/Within/Training/Data/"
        OnlineResult_Path = "C:/Users/wldk5/WorldSystem/WorldDemo/World_125/WorldTravelSystem_Data/StreamingAssets/"
        OnlineData_Path = "C:/Users/wldk5/WorldSystem/Within/Online/Data/"
        OnlineTxt_Path = "C:/Users/wldk5/WorldSystem/Within/Online/Data/txt_files/"
        Stepwise_Path = "C:/Users/wldk5/WorldSystem/Within/StepWise/"
        ZeroData_Path = "C:/Users/wldk5/WorldSystem/Zero/Online/Data/"
        ZeroTxt_Path = "C:/Users/wldk5/WorldSystem/Zero/Online/Data/txt_files/"
        DataAcquisition_Path = "C:/Users/wldk5/WorldSystem/DataAcquisition/Data/"
        PreSurvey_Path = "C:/Users/wldk5/WorldSystem/Survey_Program/Build/Survey_Program_Data/StreamingAssets/"
        PostSurvey_Path = "C:/Users/wldk5/WorldSystem/Post_Survey/Build/Post_Survey_Data/StreamingAssets/"
        Result_list = []
            #They are stored in the list in the order they are stored.
        Result_list = sorted(glob.glob(OnlineResult_Path + '*.txt'), key=os.path.getmtime)
            #Create a folder with the name of the first file created
        UserName = Result_list[0][86:-4]
        CurrentFolder = RootPath + UserName
        
        if not os.path.exists(CurrentFolder):
            createFolder(CurrentFolder)
                #Create detail folder
            createFolder(CurrentFolder + '/RestingData')
            createFolder(CurrentFolder + '/TrainData')
            createFolder(CurrentFolder + '/TrainData/SelectedFeatures')
            createFolder(CurrentFolder + '/TrainData/Classifier')
            createFolder(CurrentFolder + '/OnlineData')
            createFolder(CurrentFolder + '/OnlineData/txt_files')
            createFolder(CurrentFolder + '/OnlineData/txt_files/eegData')
            createFolder(CurrentFolder + '/OnlineData/txt_files/stims')
            createFolder(CurrentFolder + '/ZeroData')
            createFolder(CurrentFolder + '/ZeroData/txt_files')
            createFolder(CurrentFolder + '/ZeroData/txt_files/eegData')
            createFolder(CurrentFolder + '/ZeroData/txt_files/stims')
            createFolder(CurrentFolder + '/AcquiredData')
            createFolder(CurrentFolder + '/OnlineTarget')
            createFolder(CurrentFolder + '/ZeroTarget')
            createFolder(CurrentFolder + '/PreSurvey')
            createFolder(CurrentFolder + '/PostSurvey')
        
        ##Resting Data
        Resting_list = []
        Resting_list = sorted(glob.glob(RestingState_Path + '*.ov'), key=os.path.getmtime)
        x = np.shape(Resting_list)[0]
        for t in range(0, x):
            shutil.move(Resting_list[t], CurrentFolder + '/RestingData/' + Resting_list[t][40:])
        
#        ##Survey
            #PreSurvey
        PreSurvey_list = []
        PreSurvey_list = glob.glob(PreSurvey_Path + '*.txt')
        shutil.move(PreSurvey_list[0], CurrentFolder + '/PreSurvey/' + PreSurvey_list[0][84:])
            #PostSurvey
        PostSurvey_list = []
        PostSurvey_list = glob.glob(PostSurvey_Path + '*.txt')
        shutil.move(PostSurvey_list[0], CurrentFolder + '/PostSurvey/' + PostSurvey_list[0][78:])
        
        ##Training Data
        Training_list = []
        Training_list = glob.glob(TrainingData_Path + '*.ov')
        shutil.move(Training_list[0], CurrentFolder + '/TrainData/' + Training_list[0][48:])
        Training_mat = []
        Training_mat = glob.glob(TrainingData_Path + '*.mat')
        shutil.move(Training_mat[0], CurrentFolder + '/TrainData/' + Training_mat[0][48:])
        
        ##Acquired Data
        Acquiring_list = []
        Acquiring_list = glob.glob(DataAcquisition_Path + '*.ov')
        shutil.move(Acquiring_list[0], CurrentFolder + '/AcquiredData/' + Acquiring_list[0][48:])
        shutil.move(Acquiring_list[1], CurrentFolder + '/AcquiredData/' + Acquiring_list[1][48:])
        
        ##Selected Features, Classifiers
        SF_list = []
        C_list = []
        SF_list = glob.glob(Stepwise_Path + '/Features/*.pickle')
        C_list = glob.glob(Stepwise_Path + '/Classifiers/*.pickle')
        shutil.move(SF_list[0], CurrentFolder + '/TrainData/SelectedFeatures/' + SF_list[0][53:])
        shutil.move(C_list[0], CurrentFolder + '/TrainData/Classifier/' + C_list[0][56:])
        
        ##Target
        k = np.shape(Result_list)[0]
        for t in range(0, k):
            shutil.move(Result_list[t], CurrentFolder + '/OnlineTarget/' + Result_list[t][86:])
        
        ##OnlineData
        Online_list = []
        OnlineTxt_eeg = []
        OnlineTxt_stims = []
        Online_list = sorted(glob.glob(OnlineData_Path + '*.ov'), key=os.path.getmtime)
        l = np.shape(Online_list)[0]
        for t in range(0, l):
            shutil.move(Online_list[t], CurrentFolder + '/OnlineData/' + Online_list[t][46:])
            
            #txt files
        OnlineTxt_eeg = sorted(glob.glob(OnlineTxt_Path + '/eegData/' + '*.out'), key=os.path.getmtime)
        OnlineTxt_stims = sorted(glob.glob(OnlineTxt_Path + '/stims/' + '*.out'), key=os.path.getmtime)
        s = np.shape(OnlineTxt_eeg)[0]
        for t in range(0, s):
            shutil.move(OnlineTxt_eeg[t], CurrentFolder + '/OnlineData/txt_files/eegData/' + OnlineTxt_eeg[t][65:])
            shutil.move(OnlineTxt_stims[t], CurrentFolder + '/OnlineData/txt_files/stims/' + OnlineTxt_stims[t][63:])
                
        ##ZeroData
        Zero_list = []
        ZeroTxt_eeg = []
        ZeroTxt_stims = []
        Zero_list = sorted(glob.glob(ZeroData_Path + '*.ov'), key=os.path.getmtime)
        a = np.shape(Zero_list)[0]
        for t in range(0, a):
            shutil.move(Zero_list[t], CurrentFolder + '/ZeroData/' + Zero_list[t][44:])
        
            #txt files
        ZeroTxt_eeg = sorted(glob.glob(ZeroTxt_Path + '/eegData/' + '*.out'), key=os.path.getmtime)
        ZeroTxt_stims = sorted(glob.glob(ZeroTxt_Path + '/stims/' + '*.out'), key=os.path.getmtime)
        q = np.shape(ZeroTxt_eeg)[0]
        for t in range(0, q):
            shutil.move(ZeroTxt_eeg[t], CurrentFolder + '/ZeroData/txt_files/eegData/' + ZeroTxt_eeg[t][63:])
            shutil.move(ZeroTxt_stims[t], CurrentFolder + '/ZeroData/txt_files/stims/' + ZeroTxt_stims[t][61:])
        
if __name__ == "__main__":
    main()