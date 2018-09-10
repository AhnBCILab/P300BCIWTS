///-----------------------------------------------------------------------------------
///-----------------------------------------------------------------------------------
/// UIVA Server - Unity Indie VRPN Adapter 
/// 
/// File: UIVA.cs
/// 
/// Description:
///     Each device has a UIVA_Device class, which contains data buffers and callbacks 
///     functions.
/// 
/// Author: 
///     Jia Wang (wangjia@wpi.edu)
///     Human Interaction in Virtual Enviroments (HIVE) Lab
///     Department of Computer Science
///     Worcester Polytechnic Institute
/// 
/// History: (1.0) 02/05/2011  by  Jia Wang           
///-----------------------------------------------------------------------------------
///-----------------------------------------------------------------------------------

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Vrpn;
using System.Threading;

namespace UIVA_Server
{
    class VRPN_ButtonServer
    {
        // Server
        ButtonRemote buttRemote;

        public bool b_0 = false;
        public bool b_1 = false;
        public bool b_2 = false;
        public bool b_3 = false;
        public bool b_4 = false;
        public bool b_5 = false;
        public bool b_6 = false;
        public bool b_7 = false;

        public VRPN_ButtonServer(string ID)
        {
            buttRemote = new ButtonRemote(ID);
            buttRemote.ButtonChanged += new ButtonChangeEventHandler(EpocButtonChanged);
            buttRemote.MuteWarnings = true;
        }

        private void EpocButtonChanged(object sender, ButtonChangeEventArgs e)
        {
            //Console.Write("button changed!");
            switch (e.Button)
            {
                case 0:
                    b_0 = true;
                    break;
                case 1:
                    b_1 = true;
                    break;
                case 2:
                    b_2 = true;
                    break;
                case 3:
                    b_3 = true;
                    break;
                case 4:
                    b_4 = true;
                    break;
                case 5:
                    b_5 = true;
                    break;
                case 6:
                    b_6 = true;
                    break;
                case 7:
                    b_7 = true;
                    break;
                default:
                    break;
            }
        }

        public void Update()
        {
            buttRemote.Update();
        }

        public String Encode()
        {
            String buttStr = "";
            // Uppercase for button press, lowercase for button release
            if (b_0) { buttStr = "Zero\n"; b_0 = false; }
            else if (b_1) { buttStr = "One\n"; b_1 = false; }
            else if (b_2) { buttStr = "Two\n"; b_2 = false; }
            else if (b_3) { buttStr = "Three\n"; b_3 = false; }
            else if (b_4) { buttStr = "Four\n"; b_4 = false; }
            else if (b_5) { buttStr = "Five\n"; b_5 = false; }
            else if (b_6) { buttStr = "Six\n"; b_6 = false; }
            else if (b_7) { buttStr = "Seven\n"; b_7 = false; }
            else { buttStr = "No_Value\n"; }
            return buttStr;
        }
    }

    class UIVA_ButtonServer
    {
        // Server
        ButtonServer buttServer;
        Connection vrpnConnection;
        int buttNums = 8;  // You can use the number of buttons as you need by chainging this value.

        public UIVA_ButtonServer()
        {
            vrpnConnection = Connection.CreateServerConnection(50555);// port number
            buttServer = new ButtonServer("button_test@localhost", vrpnConnection, 32);   // 마지막은 버튼 개수 
            buttServer.MuteWarnings = true;
        }

        public void WakeUpTest()
        {
            for (int i = 1; i < 7; i++)
            {
                Thread.Sleep(500);
                for (int j = 0; j < buttNums; j++)
                {
                    buttServer.Buttons[j] = true;
                    buttServer.Update();
                    vrpnConnection.Update();

                    buttServer.Buttons[j] = false;
                    buttServer.Update();
                    vrpnConnection.Update();
                }
                Console.WriteLine("UIVA_Server Test..." + i);
            }
            Console.WriteLine("UIVA_Server VRPN Connection Completed!");
        }

        /* Press */
        public void Press(int num)
        {
            buttServer.Buttons[num] = true;
            buttServer.Update();
            vrpnConnection.Update();
            //Console.WriteLine(buttServer.Buttons[num]);
            Release(num); //바로 끄게 만들어서 표시되는데 오류가 없도록.
        }

        /* Release */
        public void Release(int num)
        {
            buttServer.Buttons[num] = false;
            buttServer.Update();
            vrpnConnection.Update();
            Console.WriteLine("\n");
            //Console.WriteLine(buttServer.Buttons[num]);
        }
    }
}