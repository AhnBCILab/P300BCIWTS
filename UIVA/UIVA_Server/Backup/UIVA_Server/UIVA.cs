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
    class UIVA_Epoc
    {
        // Remote
        AnalogRemote anaRemote;
        ButtonRemote buttRemote;


        // Data buffers
        public double channel_val;    // signal data(serial)
        public int num_channel;  // number of channels
        public bool buttA;       // Button A
        public bool buttZ;       // Button Z
        public DateTime anaTimeStamp;   // Time event for analog events
        public DateTime buttTimeStamp;  // Time event for button events


        public UIVA_Epoc(String ID)  //// ID = name = token[1] = openvibe_vrpn_analog@localhost (cfg file)
        {
            anaRemote = new AnalogRemote(ID);
            anaRemote.AnalogChanged += new AnalogChangeEventHandler(EpocAnalogChanged);
            anaRemote.MuteWarnings = true;

            buttRemote = new ButtonRemote(ID);
            buttRemote.ButtonChanged += new ButtonChangeEventHandler(EpocButtonChanged);
            buttRemote.MuteWarnings = true;


        }

        /* Analog event handler */
        private void EpocAnalogChanged(object sender, AnalogChangeEventArgs e)
        {
            anaTimeStamp = e.Time.ToLocalTime();
            channel_val = e.Channels[0];        ////  I guess that index 0 of array 'Channels' will be signal data.
            //num_channel = (int)e.Channels[1];   ////  I guess that index 1 of array 'Channels' will be number of channels.
        }


        /* Button event handler */
        private void EpocButtonChanged(object sender, ButtonChangeEventArgs e)
        {
            buttTimeStamp = e.Time.ToLocalTime();
            switch (e.Button)
            {
                case 0: // A
                    if (e.IsPressed) { buttA = true; } else { buttA = false; }
                    break;
                case 1: // B
                    if (e.IsPressed) { buttZ = true; } else { buttZ = false; }
                    break;
                default:
                    break;
            }
        }

        /* Epoc_Remote mainloop() */
        public void Update()
        {
            anaRemote.Update();
            buttRemote.Update();
        }


        /* Encode Epoc data to UIVA_Client */
        public String Encode()
        {
            String buttStr = "";
            // Uppercase for button press, lowercase for button release
            if (buttA) { buttStr += ",A"; } else { buttStr += ",a"; }
            if (buttZ) { buttStr += "Z"; } else { buttStr += "z"; }
            buttStr += buttTimeStamp.ToString("o");
            buttStr += "\n";

            // 아래의 format이 UIVA_Client GetEpocData()의 string array 'sections'으로 들어가게 된다.
            String anaStr = String.Format("EPOC,,{0},{1},{2}", channel_val, num_channel, anaTimeStamp.ToString("o"));
            return anaStr + buttStr;
        }

    }

    class UIVA_ButtonServer
    {
        // Server
        ButtonServer buttServer;
        Connection vrpnConnection;
        int buttNums = 6;  // You can use the number of buttons as you need by chainging this value.

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
                
                Console.WriteLine("UIVA_Server Test..."+i);
            }
            Console.WriteLine("UIVA_Server VRPN Connection Completed!");
        }

        /* Press */
        public void Press(int num)
        {
            buttServer.Buttons[num] = true;
            buttServer.Update();
            vrpnConnection.Update();
            Console.WriteLine(buttServer.Buttons[num]);

            Release(num); //
        }

        /* Release */
        public void Release(int num)
        {

            buttServer.Buttons[num] = false;
            buttServer.Update();
            vrpnConnection.Update();
            Console.WriteLine(buttServer.Buttons[num]);
        }

        /* Encode Epoc data to UIVA_Client */
        public String Encode()
        {
            String buttStr = "";
           return buttStr;
        }

    }

}