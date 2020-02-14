import numpy as np
import os, glob

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
        ##Compute session accuracy of user data
        UserData_Path = "C:/Users/user/WorldSystem/UserData"
        Target_list = []
            #They are stored in the list in the order they are stored.
        Target_list = sorted(glob.glob(UserData_Path + '/*'), key=os.path.getmtime)
        UserNum = np.shape(Target_list)[0]
        TotalAccO = np.zeros((UserNum,1))
        TotalAccO2 = np.zeros((UserNum,1))
        for i in range(0,UserNum):
            OnlineTarget_Path = glob.glob(Target_list[i] + '/OnlineTarget/*.txt')
#            ZeroTarget_Path = glob.glob(Target_list[i] + '/ZeroTarget/*.txt')
            ##Result txt file read in order to get orders
            OT = []
            ZT = []
            [TryO, OT] = Readtxt(OnlineTarget_Path[0])
            [TryO2, OT2] = Readtxt(OnlineTarget_Path[1])
            print(str(Target_list[i][35:]))
        #     print("FinO: \n", TryO, OT)
        #     print("FinZ: \n", TryZ, ZT)
            CorrectO = 0
            CorrectO2 = 0
            
            ##Find Session Accuracy
            for k in range(0, TryO):
                if(OT[k][7] == OT[k][19]):
                    CorrectO = CorrectO + 1
            for k in range(0, TryO2):
                if(OT2[k][7] == OT2[k][19]):
                    CorrectO2 = CorrectO2 + 1
            
            ##Print result
            AccO = CorrectO/TryO
            AccO2 = CorrectO2/TryO2
            print("Online:",AccO)
            print("Online2:",AccO2)
            print("\n")
            TotalAccO[i,0] = AccO
            TotalAccO2[i,0] = AccO2
        print("Total Accuracy")
        print("Online:", np.mean(TotalAccO))
        print("Online2:", np.mean(TotalAccO2))
        
if __name__ == "__main__":
    main()