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

    public StimulusSender theSender = null; // Initialize the TCP instance into null

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

    public byte finish = 7; // Marker to announce the end of the trial
    public byte start = 8; // Marker to announce the start of the next trial

    public string output = "";

    bool blinkstate = true;
    Button pubimg;

    RectTransform noArect;

    void Start()
    {
        // If you have selected a total of 6 cities, it will return to the main menu.
        if (InputName.Try == 6)
        {
            InputName.Try = 0;
            SceneManager.LoadScene("Menu");
            InputName.theListener.close();
        }

        // Code to instruct to select a button at random
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
        /////////////////////////////////////////////////
        
        // Generate a TCP instance
        theSender = new StimulusSender(); // Generate a TCP instance used for button number sender
        theSender.open("localhost", 12140);
        if (InputName.Try == 0) // If this trial is the first of a session, 
        {
            InputName.theListener = new StimulusSender(); // Generate a TCP instance used to listen to signals from openvibe
            InputName.theListener.open("localhost", 12240);
        }
        //////////////////////////

        cb.normalColor = new Color(132f, 132f, 132f, 255f);
        //cb.normalColor = Color.gray;
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
        // If you press q, you return to the main menu.
        if (Input.GetKeyDown(KeyCode.Q))
        {
            SceneManager.LoadScene("Menu");
        }
        current_time += Time.deltaTime;
        // Start blinking after 5 seconds
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
    // It minimizes the repeated blinking of the same button by making the 6 buttons blink once within each sequence(6 times) unconditionally.
    // The variables controlling this is Button0 to Button5.
    public void BlinkButton() 
    {
        ////////////////////////////////////////////// If the total number of blinks has not been reached, /////////////////////////////////////////////////
        if (blinkcnt < BlinkCount)
        {
            rndnum = UnityEngine.Random.Range(0, 6); // Randomly generate one of the values ​​from 0 to 5
            if (rndnum == 0 && Button0 == true) // If the generated random number is 0 and Button0 is true,
            {
                Button0 = false; // Change Button0 to false to indicate that the button0 is blinking
                buttonIndexNum = 1; // Assign Button0 identifier to send to OpenViBE
                theSender.send(buttonIndexNum); // Send the identifier to OpenViBE
                pubimg = NorthAmerica; // 

                if (isBlinking) // If the previous button is not blinking successfully, isBlinking is true
                    return; // Therefore, the system will stop through the return command.
                if (pubimg != null)
                {
                    isBlinking = true; // Indication of starting button blinking
                    InvokeRepeating("ToggleState", startDelay, interval); // Code to make the actual button blink
                }
            }
            else if (rndnum == 0 && Button0 == false)
            {
                BlinkButton(); // Call BlinkButton again.
            }
            else if (rndnum == 1 && Button1 == true) // Same as the first if statement
            {
                Button1 = false;
                buttonIndexNum = 2;
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

            // If all buttons blink, set the boolean value to true so that each button can blink again.
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
        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //////////////////////////////////////////////// If the total number of flashes has been reached, /////////////////////////////////////////////////
        else
        {
            InputName.Try = InputName.Try + 1;
            System.Threading.Thread.Sleep(1000); // Wait for 1 second. This latency is absolutely necessary to use the epoch for the last button blink.
            theSender.send(finish); // Send a marker to inform OpenViBE that blinking is over
            output = InputName.theListener.receive(); // Receive classification result from OpenViBE
            theSender.send(start); // Send a marker to inform OpenViBE that blinking will be re-started in next trial.
            theSender.close(); // Release a sender instance for the system reliability.
            System.Threading.Thread.Sleep(1000);

            // Write in the text file whether the classification result matched the target presented in current trial.
            FileStream f = new FileStream(Application.dataPath + "/StreamingAssets/" + InputName.patient_id + ".txt", FileMode.Append, FileAccess.Write);
            StreamWriter writer = new StreamWriter(f, System.Text.Encoding.Unicode);
            writer.WriteLine("Order: " + random + " / Result: " + output);
            writer.Close();
            //////////////////////////////////////////////////////////////////////////////////////////////////////////

            switch (output) // Scene movement according to target and classification result.
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
        ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    }
    public void ToggleState()
    {
        if (cb.normalColor == Color.gray) // If the current button color is gray,
        {
            cb.normalColor = Color.yellow; // Change its color to yellow so that the button blinks.
            pubimg.colors = cb;
        }
        else // If the current button color is yellow,
        {
            cb.normalColor = Color.gray; // Change its color to gray to stop the button blinking.
            pubimg.colors = cb;
        }
        count++;
        if (count == num_of_blink_arrow) // When the blinking is over, the count becomes 2.
        {
            CancelInvoke(); // Cancel invoking blinking function
            // Increase the blink number
            blinkcnt++;

            if (rndnum == 0) noA++;
            else if (rndnum == 1) soA++;
            else if (rndnum == 2) Asi++;
            else if (rndnum == 3) Afr++;
            else if (rndnum == 4) Oce++;
            else Eur++;

            count = 0; // Reset the blinking indicator
            isBlinking = false; // Assign false to the isBlinking variable to indicate that the button blinking has ended successfully.
            Invoke("BlinkButton", timebetweenarrows); // Call the BlinkButton function again and proceed to make the next button blink.
        }
    }

}