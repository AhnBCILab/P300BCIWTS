using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine.SceneManagement;
using UnityEngine;
using UnityEngine.Experimental;
using UnityEngine.UI;

public class SouthAmericaBlink : MonoBehaviour
{
    public Text txt;
    public int random = 0;
    public string path = "";

    public StimulusSender theSender = null;
    public StimulusSender theListener = null;
    ColorBlock cb;
    public Button Barbados; //image to toggle
    public Button BuenosAires; //image to toggle
    public Button Cusco; //image to toggle
    public Button EasterIsland; //image to toggle  
    public Button Patagonia; //image to toggle 
    public Button RiodeJaneiro; //image to toggle  

    public int num_of_blink_arrow = 2;
    public float current_time = 0.0f;

    public float interval = 0.0625f;
    public float startDelay = 0.062f;
    public float timebetweenarrows = 0.0635f;

    public byte finish = 7;
    public byte start = 8;

    public int blinkcnt = 0;
    public int BlinkCount = 120;

    bool isBlinking = false;
    bool Button0 = true, Button1 = true, Button2 = true, Button3 = true, Button4 = true, Button5 = true;
    public int noA = 0, soA = 0, Asi = 0, Afr = 0, Oce = 0, Eur = 0;
    int count = 0;
    public byte buttonIndexNum = 0;
    int rndnum = 0;
    public int[] ranArr = { 0, 1, 2, 3, 4, 5 };

    public string outp = "";
    public string output = "";

    bool blinkstate = true;
    Button pubimg;

    void Start()
    {
        random = UnityEngine.Random.Range(1, 7);
        switch (random)
        {
            case 1:
                path = "Barbados";
                break;
            case 2:
                path = "EasterIsland";
                break;
            case 3:
                path = "Cusco";
                break;
            case 4:
                path = "BuenosAires";
                break;
            case 5:
                path = "Patagonia";
                break;
            case 6:
                path = "RiodeJaneiro";
                break;
            default:
                break;
        }
        txt.text = "Look at " + path;

        theSender = new StimulusSender();
        theSender.open("localhost", 12140);
        theListener = new StimulusSender();
        theListener.open("localhost", 12240);
        cb.normalColor = Color.gray;
        cb.colorMultiplier = 1.5f;
        Barbados.colors = cb;
        BuenosAires.colors = cb;
        Cusco.colors = cb;
        EasterIsland.colors = cb;
        RiodeJaneiro.colors = cb;
        Patagonia.colors = cb;
    }
    private void Update()
    {
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
                theSender.send(buttonIndexNum);
                pubimg = Barbados;

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
                theSender.send(buttonIndexNum);
                pubimg = EasterIsland;

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
                theSender.send(buttonIndexNum);
                pubimg = Cusco;

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
                theSender.send(buttonIndexNum);
                pubimg = BuenosAires;

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
                theSender.send(buttonIndexNum);
                pubimg = Patagonia;

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
                theSender.send(buttonIndexNum);
                pubimg = RiodeJaneiro;

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
            System.Threading.Thread.Sleep(1000);
            theSender.send(finish);
            output = theListener.receive();
            outp = output.Substring(0, 28);
            theSender.send(start);
            theSender.close();
            theListener.close();
            System.Threading.Thread.Sleep(1000);
            FileStream f = new FileStream(Application.dataPath + "/StreamingAssets/" + InputName.patient_id + ".txt", FileMode.Append, FileAccess.Write);
            StreamWriter writer = new StreamWriter(f, System.Text.Encoding.Unicode);
            writer.WriteLine("Order: " + random + " / Result: " + outp[27] + "\n");
            writer.Close();
            switch (outp)
            {
                case "OVTK_StimulationId_Number_01":
                    SceneManager.LoadScene("Barbados");
                    break;
                case "OVTK_StimulationId_Number_02":
                    SceneManager.LoadScene("EasterIsland");
                    break;
                case "OVTK_StimulationId_Number_03":
                    SceneManager.LoadScene("Cusco");
                    break;
                case "OVTK_StimulationId_Number_04":
                    SceneManager.LoadScene("BuenosAires");
                    break;
                case "OVTK_StimulationId_Number_05":
                    SceneManager.LoadScene("Patagonia");
                    break;
                case "OVTK_StimulationId_Number_06":
                    SceneManager.LoadScene("RiodeJaneiro");
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