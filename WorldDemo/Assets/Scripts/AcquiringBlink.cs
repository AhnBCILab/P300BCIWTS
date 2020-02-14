using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;
using UnityEngine.Experimental;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class AcquiringBlink : MonoBehaviour

{
    public StimulusSender theSender = null;
    ColorBlock cb;
    public Button Button0; //image to toggle
    public Button Button1; //image to toggle
    public Button Button2; //image to toggle
    public Button Button3; //image to toggle 
    public Button Button4; //image to toggle
    public Button Button5; //image to toggle

    public int num_of_blink_arrow = 2;
    public float current_time = 0.0f;

    public float interval = 0.0625f;
    public float startDelay = 0.062f;
    public float timebetweenarrows = 0.0635f;

    public int blinkcnt = 0;
    public int BlinkCount = 120;

    bool isBlinking = false;
    bool but0 = true, but1 = true, but2 = true, but3 = true, but4 = true, but5 = true;
    public int cnt_but0 = 0, cnt_but1 = 0, cnt_but2 = 0, cnt_but3 = 0, cnt_but4 = 0, cnt_but5 = 0;
    int count = 0;
    public byte buttonIndexNum = 0;
    int targetChange = 0;
    int rndnum = 0;

    public byte finish = 7;

    public int[] ranArr = { 0, 1, 2, 3, 4, 5 };

    bool blinkstate = true;
    Button pubimg;

    void Start()
    {
        theSender = new StimulusSender();
        theSender.open("localhost", 12140);
        cb.normalColor = Color.gray;
        cb.colorMultiplier = 1.5f;
        Button0.colors = cb;
        Button1.colors = cb;
        Button2.colors = cb;
        Button3.colors = cb;
        Button5.colors = cb;
        Button4.colors = cb;
    }
    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Q))
        {
            SceneManager.LoadScene("Menu");
        }
        current_time += Time.deltaTime;
        if (targetChange == 6 && current_time < 10.0f)
        {
            if (current_time > 5.0f) {
                theSender.send(finish);
                theSender.close();
            }
            if (current_time > 5.0f) SceneManager.LoadScene("Menu");
        }
        //Restart blinking
        if (current_time > 5.0f && blinkstate == true)
        {
            blinkstate = false;
            but0 = true;
            but1 = true;
            but2 = true;
            but3 = true;
            but4 = true;
            but5 = true;
            blinkcnt = 0;
            BlinkButton();
        }
        else if (current_time > 39.0f)
        {
            current_time = 0.0f;
            blinkstate = true;
        }
    }
    public void BlinkButton()
    {
        if (blinkcnt < BlinkCount)
        {
            rndnum = UnityEngine.Random.Range(0, 6);
            if (rndnum == 0 && but0 == true)
            {
                but0 = false;

                //if (ranArr[targetChange] == rndnum)
                //    buttonIndexNum = 1;
                //else
                //    buttonIndexNum = 0;
                buttonIndexNum = 1;
                theSender.send(buttonIndexNum);

                pubimg = Button0;

                if (isBlinking)
                    return;
                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 0 && but0 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 1 && but1 == true)
            {
                but1 = false;

                //if (ranArr[targetChange] == rndnum)
                //    buttonIndexNum = 1;
                //else
                //    buttonIndexNum = 0;
                buttonIndexNum = 2;
                theSender.send(buttonIndexNum);

                pubimg = Button1;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 1 && but1 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 2 && but2 == true)
            {
                but2 = false;

                //if (ranArr[targetChange] == rndnum)
                //    buttonIndexNum = 1;
                //else
                //    buttonIndexNum = 0;
                buttonIndexNum = 3;
                theSender.send(buttonIndexNum);

                pubimg = Button2;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 2 && but2 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 3 && but3 == true)
            {
                but3 = false;

                //if (ranArr[targetChange] == rndnum)
                //    buttonIndexNum = 1;
                //else
                //    buttonIndexNum = 0;
                buttonIndexNum = 4;
                theSender.send(buttonIndexNum);

                pubimg = Button3;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 3 && but3 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 4 && but4 == true)
            {
                but4 = false;

                //if (ranArr[targetChange] == rndnum)
                //    buttonIndexNum = 1;
                //else
                //    buttonIndexNum = 0;
                buttonIndexNum = 5;
                theSender.send(buttonIndexNum);

                pubimg = Button4;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 4 && but4 == false)
            {
                BlinkButton();
            }
            else if (rndnum == 5 && but5 == true)
            {
                but5 = false;

                //if (ranArr[targetChange] == rndnum)
                //    buttonIndexNum = 1;
                //else
                //    buttonIndexNum = 0;
                buttonIndexNum = 6;
                theSender.send(buttonIndexNum);

                pubimg = Button5;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 5 && but5 == false)
            {
                BlinkButton();
            }

            if (but0 == false && but1 == false && but2 == false && but3 == false && but4 == false && but5 == false)
            {
                but0 = true;
                but1 = true;
                but2 = true;
                but3 = true;
                but4 = true;
                but5 = true;
            }
        }
        else
        {
            targetChange++;
            //if (targetChange == 6 && repeat == 0)
            //{
            //    targetChange = 0;
            //    repeat++;
            //}
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

            if (rndnum == 0) cnt_but0++;
            else if (rndnum == 1) cnt_but1++;
            else if (rndnum == 2) cnt_but2++;
            else if (rndnum == 3) cnt_but3++;
            else if (rndnum == 4) cnt_but4++;
            else cnt_but5++;

            count = 0;
            isBlinking = false;
            Invoke("BlinkButton", timebetweenarrows);
        }
    }

}