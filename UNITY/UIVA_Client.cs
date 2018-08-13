///-----------------------------------------------------------------------------------
///-----------------------------------------------------------------------------------
/// UIVA (Unity Indie VRPN Adapter) Unity
/// 
/// Function: The client side of UIVA living in Unity as a DLL file.
///           Unity creates a UIVA class and calls its GetXXXData(out X, out X) functions
///           to get the latest data from the sensor devices.
/// 
/// About UIVA:
/// 
///   UIVA is a middle-ware between VRPN and Unity. It enables games developed by Unity3D INDIE
///   to be controlled by devices powered by VRPN. It has a client and a server simultaneously.
///   For VRPN, UIVA is its client which implements several callback functions to receive the 
///   latest data from the devices. For Unity, UIVA is a server that stores the latest sensor
///   data which allows it to query. The framework is shown as below:
///   
///        ~~~Sensor~~~      ~~~VRPN~~~      ~~~~~~~~~~~~UIVA~~~~~~~~~~~~~~~    ~~~Unity3D~~~     
///        
///   Kinect-----(FAAST)---->|--------|    |--------|--------|    |---------|
///    Wii ----(VRPN Wii)--->|        |    |        |        |    |         |--->Object transform
///   BPack --(VRPN BPack)-->|  VRPN  |    |  VRPN  | Unity  |    |  Unity  |
///           ...            |        |===>|  .net  | socket |===>|  socket |--->GUI
///           ...            | server |    |        |        |    |         |
///           ...            |        |    | client | server |    |  client |--->etc. of Unity3D
///           ...            |--------|    |--------|--------|    |---------|
///    
/// Special note: 
///
///      The VRPNWrapper implemented by the AR lab of Georgia Institute of Technology offers
///   a easier to use wrapper of VRPN to be used as a plugin in Unity3D Pro. If you can afford 
///   the Pro version of Unity. I suggest you to use VRPNWrapper. Their website is:
///           https://research.cc.gatech.edu/uart/content/about
///   They also implemented a ARToolkit wrapper which enables AR application in Unity. 
///   Check out their UART project, it is awesome!
///    
/// Author: 
/// 
/// Jia Wang (wangjia@wpi.edu)
/// Human Interaction in Virtual Enviroments (HIVE) Lab
/// Department of Computer Science
/// Worcester Polytechnic Institute
/// 
/// History: (1.0) 01/11/2011  by  Jia Wang
///
/// Acknowledge: Thanks to Chris VanderKnyff for the .NET version of VRPN
///                     to UNC for the awesome VRPN
///                     to Unity3D team for the wonderful engine
///              
///              and above all, special thanks to 
///                 Prof. Robert W. Lindeman (http://www.wpi.edu/~gogo) 
///              for the best academic advice.
///              
///-----------------------------------------------------------------------------------
///-----------------------------------------------------------------------------------

using System;
using System.Collections.Generic;
using System.Text;
using System.Net.Sockets;
using System.Net;

/// <summary>
/// UIVA_Client class
/// </summary>
public class UIVA_Client
{
    Socket socClient;       //Socket deal with communication
    private byte[] recBuffer = new byte[100];   //Receive buffer
    private byte[] blankBuffer = new byte[100];
    public string recStr = "";                 //Deciphered receive

    /// <summary>
    /// Connect and test connection
    /// </summary>
    /// <param name="serverIP">The IP address of the server, 
    /// should be the local IP if used as Unity interface</param>
    public UIVA_Client(string serverIP)
    {
        // If the UIVA server is in the local machine,
        // find its IP address and connect automatically
        if (serverIP == "localhost")
        {
            IPHostEntry host;
            host = Dns.GetHostEntry(Dns.GetHostName()); //host 이름에 대한 IP주소를 host에 assign함. 
            foreach (IPAddress ip in host.AddressList)
            {
                if (ip.AddressFamily.ToString() == "InterNetwork")
                {
                    serverIP = ip.ToString();
                }
            }
        }

        try
        {
            //Create a client socket
            socClient = new Socket(AddressFamily.InterNetwork,
                                SocketType.Stream, ProtocolType.IP);
            //Parse the IP address string into an IPAddress object
            IPAddress serverAddr = IPAddress.Parse(serverIP);
            //Port: 8881
            IPEndPoint serverMachine = new IPEndPoint(serverAddr, 8881);
            //Connect
            socClient.Connect(serverMachine);
            //Send a confirmation message
            SendMessage("Ready?\n");
            ReceiveMessage();
            if (recStr != "Ready!")
            {
                throw new Exception("Not ready?");
            }
            else recStr = "";
        }
        catch (Exception e)
        {
            Exception initError = new Exception(e.ToString()
                                    + "\nClient failed to connect to server. Is your IP correct?"
                                    + "Is your UIVA working\n");
            throw initError;
        }
    }

    /// <summary>
    /// Send a message to the server
    /// </summary>
    /// <param name="msg">message content, end with a '\n'</param>
    public void SendMessage(string msg)
    {
        try
        {
            //Encode a message
            byte[] sendBuffer = Encoding.ASCII.GetBytes(msg);
            socClient.Send(sendBuffer);
        }
        catch (Exception e)
        {
            Exception sendError = new Exception(e.ToString() + "Client failed to send message.\n");
            throw sendError;
        }
    }

    /// <summary>
    /// Receive message from the server, decode and store in "recStr" variable
    /// </summary>
    public void ReceiveMessage()
    {
        try
        {
            Buffer.BlockCopy(blankBuffer, 0, recBuffer, 0, 6);
            socClient.Receive(recBuffer);
            recStr = Encoding.Default.GetString(recBuffer);
            //Remove the tailing '\0's after the '\n' token, caused by the buffer size
            int ixEnd = recStr.IndexOf('\n');
            recStr = recStr.Remove(ixEnd);
        }
        catch (Exception e)
        {
            Exception recError = new Exception(e.ToString()
                                    + "Client failed to receive message.\n");
            throw recError;
        }
    }

    public void GetDirectionData(int which, out string butt)
    {
        SendMessage(String.Format("Biosemi?{0}?\n", which));
        ReceiveMessage();
        try
        {
            butt = recStr;
        }
        catch (Exception e)
        {
            throw new Exception(e.ToString() + "\n\nRECEIVED FROM UIVA_SERVER: " + recStr);
        }
    }

    public void GetDirectionData(out string butt)
    {
        GetDirectionData(1, out butt);
    }

    public void GetOrder()
    {
        SendMessage(String.Format("Biosemi?{0}?\n", 1));
        ReceiveMessage();
        /*try
        {
            socClient.Receive(odrBuffer);
            odrStr = Encoding.Default.GetString(odrBuffer);
            Console.WriteLine("Order string: " + odrStr);
            //Remove the tailing '\0's after the '\n' token, caused by the buffer size
            int ixEnd = odrStr.IndexOf('\n');
            odrStr = odrStr.Remove(ixEnd);
        }
        catch (Exception e)
        {
            Exception recError = new Exception(e.ToString()
                                    + "Client failed to receive message.\n");
            throw recError;
        }*/
        try
        {
        }
        catch (Exception e)
        {
            throw new Exception(e.ToString() + "\n\nRECEIVED FROM UIVA_SERVER: " + recStr);
        }
    }

    /// <summary>
    /// Communicate to UIVA in reverse    
    public void Press(int num)
    {
        SendMessage(String.Format("Press?{0}?\n", num));
    }

    public void Press_O(int num)
    {
        SendMessage(String.Format("Press_O?{0}?\n", num));
    }

    public void Release(int num)
    {
        SendMessage(String.Format("Release?{0}?\n", num));
    }

    /// </summary>

    /// <summary>
    /// Disconnect from UIVA
    /// </summary>
    public void Disconnect()
    {
        SendMessage("Bye?\n");      //Send disconnect request
    }
}