using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
/*
 * Primitive TCP Tagging java client for OpenViBE 1.2.x
 *
 * @author Jussi T. Lindgren / Inria
 * @date 04.Jul.2016
 * @version 0.1
 * @todo Add error handling
 */
public class StimulusSender
{
    ////Buffer instance
    //public const int SIZE_UINT = 4;
    //public const int SIZE_INT = 4;
    //public const int SIZE_LONG = 8;
    //public const int SIZE_BYTE = 1;
    //public const int SIZE_SHORT = 2;
    //public const int SIZE_FLOAT = 4;
    //public const int SIZE_DOUBLE = 8;
    //public const int SIZE_BOOL = 1;

    private int m_iPos = 8;
    private int m_iMax = 24;
    byte[] m_Buf = new byte[24];
    
    //TCP instance
    public TcpClient m_clientSocket = new TcpClient();
    public NetworkStream readstream = default(NetworkStream);
    public BinaryWriter writer;

    // Open connection to Acquisition Server TCP Tagging 
    //JAVA TO C# CONVERTER WARNING: Method 'throws' clauses are not available in C#:
    //ORIGINAL LINE: public boolean open(String host, System.Nullable<int> port) throws Exception
    public virtual bool open(string host, int portNo)
    {
        Int32 port = portNo;
        m_clientSocket.Connect(host, port);
        //m_clientSocket = new TcpClient(host, port);
        readstream = m_clientSocket.GetStream();
        //writer = new BinaryWriter(readstream);
        Array.Clear(m_Buf, 0x0, 24);
        return true;
    }

    // Close connection
    //JAVA TO C# CONVERTER WARNING: Method 'throws' clauses are not available in C#:
    //ORIGINAL LINE: public boolean close() throws Exception
    public virtual bool close()
    {
        readstream.Close();
        m_clientSocket.Close();
        return true;
    }

    // Send stimulation with a timestamp. 
    //JAVA TO C# CONVERTER WARNING: Method 'throws' clauses are not available in C#:
    //ORIGINAL LINE: public boolean send(System.Nullable<long> stimulation, System.Nullable<long> timestamp) throws Exception
    public virtual bool send(byte stimulation)
    {
        m_clientSocket.NoDelay = true;
        m_Buf[m_iPos] = stimulation;    // Stimulation id
        //writer.Write(m_Buf);
        readstream.Write(m_Buf, 0, 24);
        return true;
    }

    //JAVA TO C# CONVERTER WARNING: Method 'throws' clauses are not available in C#:
    //ORIGINAL LINE: public String receive() throws Exception
    public virtual string receive()
    {
        byte[] data = new byte[256];

        // String to store the response ASCII representation.
        string responseData = string.Empty;

        // Read the first batch of the TcpServer response bytes.
        int bytes = readstream.Read(data, 0, data.Length);
        responseData = System.Text.Encoding.ASCII.GetString(data, 0, bytes);

        return responseData;
    }

    public void allocate(int iLimit)
    {
        m_iPos = 0;
        m_iMax = iLimit;
        m_Buf = new byte[iLimit];
    }

    public void putLong(long s)
    {
        if ((m_iPos + 8) > m_iMax)
            return;
        byte[] buf = new byte[8];

        buf = BitConverter.GetBytes(s);

        m_Buf[m_iPos++] = buf[0];
        m_Buf[m_iPos++] = buf[1];
        m_Buf[m_iPos++] = buf[2];
        m_Buf[m_iPos++] = buf[3];
        m_Buf[m_iPos++] = buf[4];
        m_Buf[m_iPos++] = buf[5];
        m_Buf[m_iPos++] = buf[6];
        m_Buf[m_iPos++] = buf[7];
    }

    public void putLongZero()
    {
        if ((m_iPos + 8) > m_iMax)
            return;
        m_Buf[m_iPos++] = 0;
        m_Buf[m_iPos++] = 0;
        m_Buf[m_iPos++] = 0;
        m_Buf[m_iPos++] = 0;
        m_Buf[m_iPos++] = 0;
        m_Buf[m_iPos++] = 0;
        m_Buf[m_iPos++] = 0;
        m_Buf[m_iPos++] = 0;
    }
}