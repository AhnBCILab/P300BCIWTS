import os, glob
import shutil
import matlab.engine

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
#        start_txt = 'C:/Users/user/WorldSystem/Zero/CNNtemp/start.out'
#        if os.path.isfile(start_txt):
#            os.remove(start_txt)
#    
#        ##Generate User folder
#        RootPath = "C:/Users/user/WorldSystem/UserData/"
#        TrainingData_Path = "C:/Users/user/WorldSystem/Within/Training/Data/"
#        OnlineResult_Path = "C:/Users/user/WorldSystem/WorldDemo/World_125/WorldTravelSystem_Data/StreamingAssets/"
#        OnlineData_Path = "C:/Users/user/WorldSystem/Within/Online/Data/"
#        OnlineTxt_Path = "C:/Users/user/WorldSystem/Within/Online/Data/txt_files/"
#        Stepwise_Path = "C:/Users/user/WorldSystem/Within/StepWise/"
#        ZeroData_Path = "C:/Users/user/WorldSystem/Zero/Online/Data/"
#        ZeroTxt_Path = "C:/Users/user/WorldSystem/Zero/Online/Data/txt_files/"
#        DataAcquisition_Path = "C:/Users/user/WorldSystem/DataAcquisition/Data/"
#        PreSurvey_Path = "C:/Users/user/WorldSystem/Survey_Program/Build/Survey_Program_Data/StreamingAssets/"
#        PostSurvey_Path = "C:/Users/user/WorldSystem/Post_Survey/Build/Post_Survey_Data/StreamingAssets/"
#        Result_list = []
#            #They are stored in the list in the order they are stored.
#        Result_list = sorted(glob.glob(OnlineResult_Path + '*.txt'), key=os.path.getmtime)
#            #Create a folder with the name of the first file created
#        UserName = Result_list[0][86:-4]
#        CurrentFolder = RootPath + UserName
#        
#        if not os.path.exists(CurrentFolder):
#            createFolder(CurrentFolder)
#                #Create detail folder
#            createFolder(CurrentFolder + '/TrainData')
#            createFolder(CurrentFolder + '/TrainData/SelectedFeatures')
#            createFolder(CurrentFolder + '/TrainData/Classifier')
#            createFolder(CurrentFolder + '/OnlineData')
#            createFolder(CurrentFolder + '/OnlineData/txt_files')
#            createFolder(CurrentFolder + '/OnlineData/txt_files/eegData')
#            createFolder(CurrentFolder + '/OnlineData/txt_files/stims')
#            createFolder(CurrentFolder + '/ZeroData')
#            createFolder(CurrentFolder + '/ZeroData/txt_files')
#            createFolder(CurrentFolder + '/ZeroData/txt_files/eegData')
#            createFolder(CurrentFolder + '/ZeroData/txt_files/stims')
#            createFolder(CurrentFolder + '/AcquiredData')
#            createFolder(CurrentFolder + '/OnlineTarget')
#            createFolder(CurrentFolder + '/ZeroTarget')
#            createFolder(CurrentFolder + '/PreSurvey')
#            createFolder(CurrentFolder + '/PostSurvey')
#        
##        ##Survey
#            #PreSurvey
#        PreSurvey_list = []
#        PreSurvey_list = glob.glob(PreSurvey_Path + '*.txt')
#        shutil.move(PreSurvey_list[0], CurrentFolder + '/PreSurvey/' + PreSurvey_list[0][84:])
#            #PostSurvey
#        PostSurvey_list = []
#        PostSurvey_list = glob.glob(PostSurvey_Path + '*.txt')
#        shutil.move(PostSurvey_list[0], CurrentFolder + '/PostSurvey/' + PostSurvey_list[0][78:])
#        
#        ##Training Data
#        Training_list = []
#        Training_list = glob.glob(TrainingData_Path + '*.ov')
#        shutil.move(Training_list[0], CurrentFolder + '/TrainData/' + Training_list[0][48:])
#        Training_mat = []
#        Training_mat = glob.glob(TrainingData_Path + '*.mat')
#        shutil.move(Training_mat[0], CurrentFolder + '/TrainData/' + Training_mat[0][48:])
#        
#        ##Acquired Data
#        Acquiring_list = []
#        Acquiring_list = glob.glob(DataAcquisition_Path + '*.ov')
#        shutil.move(Acquiring_list[0], CurrentFolder + '/AcquiredData/' + Acquiring_list[0][48:])
#        shutil.move(Acquiring_list[1], CurrentFolder + '/AcquiredData/' + Acquiring_list[1][48:])
#        
#        ##Selected Features, Classifiers
#        SF_list = []
#        C_list = []
#        SF_list = glob.glob(Stepwise_Path + '/Features/*.pickle')
#        C_list = glob.glob(Stepwise_Path + '/Classifiers/*.pickle')
#        shutil.move(SF_list[0], CurrentFolder + '/TrainData/SelectedFeatures/' + SF_list[0][53:])
#        shutil.move(C_list[0], CurrentFolder + '/TrainData/Classifier/' + C_list[0][56:])
#        
#        ##OnlineData, ZeroData, Target
#        for k in range(0, 2):
#            ##Result txt file read in order to get orders
#            Resultline = []
#            [j, Resultline] = Readtxt(Result_list[k])
#            
#            ###First txt file: SWLDA online result / Second txt file: ZeroCNN online result
#            if k==0:
#                shutil.move(Result_list[k], CurrentFolder + '/OnlineTarget/' + Result_list[k][86:])
#            else:
#                shutil.move(Result_list[k], CurrentFolder + '/ZeroTarget/' + Result_list[k][86:])
#        
#            ##Move online data into CurrentFolder according to order and File renaming
#            if k==0:
#                Online_list = []
#                OnlineTxt_eeg = []
#                OnlineTxt_stims = []
#                Online_list = sorted(glob.glob(OnlineData_Path + '*.ov'), key=os.path.getmtime)
#                OnlineTxt_eeg = sorted(glob.glob(OnlineTxt_Path + '/eegData/' + '*.out'), key=os.path.getmtime)
#                OnlineTxt_stims = sorted(glob.glob(OnlineTxt_Path + '/stims/' + '*.out'), key=os.path.getmtime)
#                RenameFileO = []
#                for i in range(0, j):
#                    os.rename(Online_list[i],OnlineData_Path + Resultline[i][7] + '_' + Online_list[i][46:])
#                    RenameFileO.append(OnlineData_Path + Resultline[i][7] + '_' + Online_list[i][46:])
#            else:
#                Zero_list = []
#                ZeroTxt_eeg = []
#                ZeroTxt_stims = []
#                Zero_list = sorted(glob.glob(ZeroData_Path + '*.ov'), key=os.path.getmtime)
#                ZeroTxt_eeg = sorted(glob.glob(ZeroTxt_Path + '/eegData/' + '*.out'), key=os.path.getmtime)
#                ZeroTxt_stims = sorted(glob.glob(ZeroTxt_Path + '/stims/' + '*.out'), key=os.path.getmtime)
#                RenameFileZ = []
#                for i in range(0, j):
#                    os.rename(Zero_list[i],ZeroData_Path + Resultline[i][7] + '_' + Zero_list[i][44:])
#                    RenameFileZ.append(ZeroData_Path + Resultline[i][7] + '_' + Zero_list[i][44:])
#            
#                #Move files to new folder
#            if k==0:
#                for i in range(0, j):
#                    shutil.move(RenameFileO[i], CurrentFolder + '/OnlineData/' + RenameFileO[i][46:])
#                    shutil.move(OnlineTxt_eeg[i], CurrentFolder + '/OnlineData/txt_files/eegData/' + OnlineTxt_eeg[i][65:])
#                    shutil.move(OnlineTxt_stims[i], CurrentFolder + '/OnlineData/txt_files/stims/' + OnlineTxt_stims[i][63:])
#            else:
#                for i in range(0, j):
#                    shutil.move(RenameFileZ[i], CurrentFolder + '/ZeroData/' + RenameFileZ[i][44:])
#                    shutil.move(ZeroTxt_eeg[i], CurrentFolder + '/ZeroData/txt_files/eegData/' + ZeroTxt_eeg[i][63:])
#                    shutil.move(ZeroTxt_stims[i], CurrentFolder + '/ZeroData/txt_files/stims/' + ZeroTxt_stims[i][61:])
        
        ov_Path = "C:/Users/user/Desktop/6_SWLDAOnline-[2019.12.05-20.00.48].ov"
        matfile_name = "C:/Users/user/Desktop/6_SWLDAOnline-[2019.12.05-20.00.48].mat"
        
        print("current ov file path:", ov_Path)
        eng = matlab.engine.start_matlab()
        k = eng.convert_ov2mat(ov_Path, matfile_name)
        
if __name__ == "__main__":
    main()