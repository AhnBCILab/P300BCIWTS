using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using UnityEngine.Experimental;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using System.Threading;
using System.Net;
using System.Net.Sockets;

public class Blink : MonoBehaviour
{
    public Text txt;
    public int random = 0;
    public string path = "";

    public StimulusSender theSender = null;

    ColorBlock cb;
    public Button NorthAmerica; //image to toggle
    public Button SouthAmerica; //image to toggle
    public Button Asia; //image to toggle
    public Button Africa; //image to toggle  
    public Button Oceania; //image to toggle 
    public Button Europe; //image to toggle 

    public int num_of_blink_arrow = 2;
    public float current_time = 0.0f;

    public float interval = 0.1f;
    public float startDelay = 0.1f;
    public float timebetweenarrows = 0.1f;

    public int blinkcnt = 0;
    public int BlinkCount = 120;

    bool isBlinking = false;
    bool Button0 = true, Button1 = true, Button2 = true, Button3 = true, Button4 = true, Button5 = true;
    public int noA = 0, soA = 0, Asi = 0, Afr = 0, Oce = 0, Eur = 0;
    int count = 0;
    public byte buttonIndexNum = 0;
    int rndnum = 0;

    public byte finish = 7;
    public byte start = 8;

    public int[] ranArr = { 0, 1, 2, 3, 4, 5 };
    public string output = "";
    //string ipUIVAServer = "localhost";
    //public UIVA_Client theClient = null;

    bool blinkstate = true;
    Button pubimg;

    RectTransform noArect;

    void Start()
    {
        if (InputName.Try == 6)
        {
            InputName.Try = 0;
            SceneManager.LoadScene("Menu");
            InputName.theListener.close();
        }

        random = UnityEngine.Random.Range(1, 7);
        switch (random)
        {
            case 1:
                path = "NorthAmerica";
                break;
            case 2:
                path = "Europe";
                break;
            case 3:
                path = "Asia";
                break;
            case 4:
                path = "SouthAmerica";
                break;
            case 5:
                path = "Africa";
                break;
            case 6:
                path = "Oceania";
                break;
            default:
                break;
        }
        txt.text = "Look at " + path;
        
        theSender = new StimulusSender();
        theSender.open("localhost", 12140);
        if (InputName.Try == 0)
        {
            InputName.theListener = new StimulusSender();
            InputName.theListener.open("localhost", 12240);
        }

        cb.normalColor = Color.gray;
        cb.colorMultiplier = 1.5f;
        NorthAmerica.colors = cb;
        SouthAmerica.colors = cb;
        Asia.colors = cb;
        Africa.colors = cb;
        Europe.colors = cb;
        Oceania.colors = cb;
        noArect = GetComponent<RectTransform>();
    }
    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Q))
        {
            SceneManager.LoadScene("Menu");
        }
        current_time += Time.deltaTime;
        //Restart blinking
        if (current_time > 5.0f && blinkstate == true)
        {
            blinkstate = false;
            Button0 = true;
            Button1 = true;
            Button2 = true;
            Button3 = true;
            Button4 = true;
            Button5 = true;
            blinkcnt = 0;
            BlinkButton();
        }
    }
    public void BlinkButton()
    {
        if (blinkcnt < BlinkCount)
        {
            rndnum = UnityEngine.Random.Range(0, 6);
            if (rndnum == 0 && Button0 == true)
            {
                Button0 = false;
                buttonIndexNum = 1;
                //theClient.Press_O(buttonIndexNum);
                theSender.send(buttonIndexNum);
                pubimg = NorthAmerica;

                if (isBlinking)
                    return;
                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 0 && Button0 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 1 && Button1 == true)
            {
                Button1 = false;
                buttonIndexNum = 2;
                //theClient.Press_O(buttonIndexNum);
                theSender.send(buttonIndexNum);
                pubimg = Europe;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 1 && Button1 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 2 && Button2 == true)
            {
                Button2 = false;
                buttonIndexNum = 3;
                //theClient.Press_O(buttonIndexNum);
                theSender.send(buttonIndexNum);
                pubimg = Asia;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 2 && Button2 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 3 && Button3 == true)
            {
                Button3 = false;
                buttonIndexNum = 4;
                //theClient.Press_O(buttonIndexNum);
                theSender.send(buttonIndexNum);
                pubimg = SouthAmerica;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }

            }
            else if (rndnum == 3 && Button3 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 4 && Button4 == true)
            {
                Button4 = false;
                buttonIndexNum = 5;
                //theClient.Press_O(buttonIndexNum);
                theSender.send(buttonIndexNum);
                pubimg = Africa;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }

            }
            else if (rndnum == 4 && Button4 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 5 && Button5 == true)
            {
                Button5 = false;
                buttonIndexNum = 6;
                //theClient.Press_O(buttonIndexNum);
                theSender.send(buttonIndexNum);
                pubimg = Oceania;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }

            }
            else if (rndnum == 5 && Button5 == false)
            {
                BlinkButton();
            }

            if (Button0 == false && Button1 == false && Button2 == false && Button3 == false && Button4 == false && Button5 == false)
            {
                Button0 = true;
                Button1 = true;
                Button2 = true;
                Button3 = true;
                Button4 = true;
                Button5 = true;
            }
        }
        else
        {
            InputName.Try = InputName.Try + 1;
            System.Threading.Thread.Sleep(1000);
            theSender.send(finish);
            output = InputName.theListener.receive();
            theSender.send(start);
            theSender.close();
            System.Threading.Thread.Sleep(1000);
            FileStream f = new FileStream(Application.dataPath + "/StreamingAssets/" + InputName.patient_id + ".txt", FileMode.Append, FileAccess.Write);
            StreamWriter writer = new StreamWriter(f, System.Text.Encoding.Unicode);
            writer.WriteLine("Order: " + random + " / Result: " + output);
            writer.Close();
            switch (output)
            {
                case "1":
                    SceneManager.LoadScene("NorthAmerica");
                    break;
                case "2":
                    SceneManager.LoadScene("Europe");
                    break;
                case "3":
                    SceneManager.LoadScene("Asia");
                    break;
                case "4":
                    SceneManager.LoadScene("SouthAmerica");
                    break;
                case "5":
                    SceneManager.LoadScene("Africa");
                    break;
                case "6":
                    SceneManager.LoadScene("Oceania");
                    break;
                default:
                    break;
            }
        }
    }
    public void ToggleState()
    {
        if (cb.normalColor == Color.gray)
        {
            cb.normalColor = Color.yellow;
            pubimg.colors = cb;
        }
        else
        {
            cb.normalColor = Color.gray;
            pubimg.colors = cb;
        }
        count++;
        if (count == num_of_blink_arrow)
        {
            CancelInvoke();
            blinkcnt++;

            if (rndnum == 0) noA++;
            else if (rndnum == 1) soA++;
            else if (rndnum == 2) Asi++;
            else if (rndnum == 3) Afr++;
            else if (rndnum == 4) Oce++;
            else Eur++;

            count = 0;
            isBlinking = false;
            Invoke("BlinkButton", timebetweenarrows);
        }
    }

}