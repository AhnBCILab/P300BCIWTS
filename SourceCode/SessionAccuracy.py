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
        TotalAccZ = np.zeros((UserNum,1))
        for i in range(0,UserNum):
            OnlineTarget_Path = glob.glob(Target_list[i] + '/OnlineTarget/*.txt')
            ZeroTarget_Path = glob.glob(Target_list[i] + '/ZeroTarget/*.txt')
            ##Result txt file read in order to get orders
            OT = []
            ZT = []
            [TryO, OT] = Readtxt(OnlineTarget_Path[0])
            [TryZ, ZT] = Readtxt(ZeroTarget_Path[0])
            print(str(Target_list[i][35:]))
        #     print("FinO: \n", TryO, OT)
        #     print("FinZ: \n", TryZ, ZT)
            CorrectO = 0
            CorrectZ = 0
            
            ##Find Session Accuracy
            for k in range(0, TryO):
                if(OT[k][7] == OT[k][19]):
                    CorrectO = CorrectO + 1
            for k in range(0, TryZ):
                if(ZT[k][7] == ZT[k][19]):
                    CorrectZ = CorrectZ + 1
            
            ##Print result
            AccO = CorrectO/TryO
            AccZ = CorrectZ/TryZ
            print("Online:",AccO)
            print("Zero:",AccZ)
            print("\n")
            TotalAccO[i,0] = AccO
            TotalAccZ[i,0] = AccZ
        print("Total Accuracy")
        print("Online:", np.mean(TotalAccO))
        print("Zeros:", np.mean(TotalAccZ))
        
if __name__ == "__main__":
    main()