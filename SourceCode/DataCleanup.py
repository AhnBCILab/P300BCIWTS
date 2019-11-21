# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:34:51 2019

@author: user
"""
import os, glob
import shutil

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)
        
def main():
        ##Generate User folder
        RootPath = "C:/Users/user/WorldSystem/UserData/"
        TrainingData_Path = "C:/Users/user/WorldSystem/Within/Training/Data/"
        OnlineResult_Path = "C:/Users/user/WorldSystem/WorldDemo/World_125/WorldTravelSystem_Data/StreamingAssets/"
        OnlineData_Path = "C:/Users/user/WorldSystem/Within/Online/Data/"
        DataAcquisition_Path = "C:/Users/user/WorldSystem/DataAcquisition/Data/"
        PreSurvey_Path = "C:/Users/user/WorldSystem/Survey_Program/Build/Survey_Program_Data/StreamingAssets/"
        PostSurvey_Path = "C:/Users/user/WorldSystem/Post_Survey/Build/Post_Survey_Data/StreamingAssets/"
        Result_list = []
            #They are stored in the list in the order they are stored.
        Result_list = sorted(glob.glob(OnlineResult_Path + '*.txt'), key=os.path.getmtime)
            #Create a folder with the name of the first file created
        UserName = Result_list[0][85:-4]
        CurrentFolder = RootPath + UserName
        
        if not os.path.exists(CurrentFolder):
            createFolder(CurrentFolder)
                #Create detail folder
            createFolder(CurrentFolder + '/TrainData')
            createFolder(CurrentFolder + '/OnlineData')
            createFolder(CurrentFolder + '/ZeroData')
            createFolder(CurrentFolder + '/AcquiredData')
            createFolder(CurrentFolder + '/OnlineTarget')
            createFolder(CurrentFolder + '/ZeroTarget')
            createFolder(CurrentFolder + '/PreSurvey')
            createFolder(CurrentFolder + '/PostSurvey')
        
        ##Survey
            #PreSurvey
        PreSurvey_list = []
        PreSurvey_list = glob.glob(PreSurvey_Path + '*.txt')
        shutil.move(PreSurvey_list[0], CurrentFolder + '/PreSurvey/' + PreSurvey_list[0][83:])
            #PostSurvey
        PostSurvey_list = []
        PostSurvey_list = glob.glob(PostSurvey_Path + '*.txt')
        shutil.move(PostSurvey_list[0], CurrentFolder + '/PostSurvey/' + PostSurvey_list[0][77:])
        
        ##Training Data
        Training_list = []
        Training_list = glob.glob(TrainingData_Path + '*.ov')
        shutil.move(Training_list[0], CurrentFolder + '/TrainData/' + Training_list[0][47:])
        
        ##Acquired Data
        Acquiring_list = []
        Acquiring_list = glob.glob(DataAcquisition_Path + '*.ov')
        shutil.move(Acquiring_list[0], CurrentFolder + '/AcquiredData/' + Acquiring_list[0][47:])
        
        ##OnlineData, ZeroData, Target
        for k in range(0, 2):
            ##Result txt file read in order to get orders
            f = open(Result_list[k], 'r', encoding='utf-16')
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
                print(j)
            f.close()
                #Move Result file to new folder
            if k==0:
                shutil.move(Result_list[k], CurrentFolder + '/OnlineTarget/' + Result_list[k][85:])
            else:
                shutil.move(Result_list[k], CurrentFolder + '/ZeroTarget/' + Result_list[k][85:])
                
            ##Move online data into CurrentFolder according to order
            Online_list = []
            Online_list = sorted(glob.glob(OnlineData_Path + '*.ov'), key=os.path.getmtime)
                #File renaming
            RenameFile = []
            for i in range(0, j):
                os.rename(Online_list[i],OnlineData_Path + Resultline[i][7] + '_' + Online_list[i][45:])
                RenameFile.append(OnlineData_Path + Resultline[i][7] + '_' + Online_list[i][45:])
                #Move files to new folder
            if k==0:
                for i in range(0, j):
                    shutil.move(RenameFile[i], CurrentFolder + '/OnlineData/' + RenameFile[i][45:])
            else:
                for i in range(0, j):
                    shutil.move(RenameFile[i], CurrentFolder + '/ZeroData/' + RenameFile[i][45:])
            
if __name__ == "__main__":
    main()