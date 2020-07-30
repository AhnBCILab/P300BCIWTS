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

public class NorthAmericaBlink : MonoBehaviour
{
    public Text txt;
    public int random = 0;
    public string path = "";

    public StimulusSender theSender = null;

    ColorBlock cb;
    public Button Alaska; //image to toggle
    public Button LA; //image to toggle
    public Button Newyork; //image to toggle
    public Button Vancouver; //image to toggle  
    public Button Lasvegas; //image to toggle 
    public Button Chicago; //image to toggle 

    public int num_of_blink_arrow = 2;
    public float current_time = 0.0f;

    public float interval = 0.0625f;
    public float startDelay = 0.062f;
    public float timebetweenarrows = 0.0635f;

    public byte finish = 7;
    public byte start = 8;

    public byte blinkcnt = 0;
    public byte BlinkCount = 120;

    bool isBlinking = false;
    bool Button0 = true, Button1 = true, Button2 = true, Button3 = true, Button4 = true, Button5 = true;
    public int noA = 0, soA = 0, Asi = 0, Afr = 0, Oce = 0, Eur = 0;
    int count = 0;
    public byte buttonIndexNum = 0;
    int rndnum = 0;
    public int[] ranArr = { 0, 1, 2, 3, 4, 5 };
    
    public string output = "";

    bool blinkstate = true;
    Button pubimg;

    void Start()
    {
        random = UnityEngine.Random.Range(1, 7);
        switch (random)
        {
            case 1:
                path = "Alaska";
                break;
            case 2:
                path = "Vancouver";
                break;
            case 3:
                path = "Newyork";
                break;
            case 4:
                path = "LosAngeles";
                break;
            case 5:
                path = "Lasvegas";
                break;
            case 6:
                path = "Chicago";
                break;
            default:
                break;
        }
        txt.text = "Look at " + path;

        theSender = new StimulusSender();
        theSender.open("localhost", 12140);

        cb.normalColor = new Color(132f, 132f, 132f, 255f);
        //cb.normalColor = Color.gray;
        cb.colorMultiplier = 1.5f;
        Alaska.colors = cb;
        LA.colors = cb;
        Newyork.colors = cb;
        Vancouver.colors = cb;
        Chicago.colors = cb;
        Lasvegas.colors = cb;
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
                theSender.send(buttonIndexNum);
                pubimg = Alaska;

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
                pubimg = Vancouver;

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
                pubimg = Newyork;

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
                pubimg = LA;

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
                pubimg = Lasvegas;

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
                pubimg = Chicago;

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
            output = InputName.theListener.receive();
            theSender.send(start);
            theSender.close();
            System.Threading.Thread.Sleep(1000);
            FileStream f = new FileStream(Application.dataPath + "/StreamingAssets/" + InputName.patient_id + ".txt", FileMode.Append, FileAccess.Write);
            StreamWriter writer = new StreamWriter(f, System.Text.Encoding.Unicode);
            writer.WriteLine("Order: " + random + " / Result: " + output + "\n");
            writer.Close();
            switch (output)
            {
                case "1":
                    SceneManager.LoadScene("Alaska");
                    break;
                case "2":
                    SceneManager.LoadScene("Vancouver");
                    break;
                case "3":
                    SceneManager.LoadScene("Newyork");
                    break;
                case "4":
                    SceneManager.LoadScene("LA");
                    break;
                case "5":
                    SceneManager.LoadScene("Lasvegas");
                    break;
                case "6":
                    SceneManager.LoadScene("Chicago");
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