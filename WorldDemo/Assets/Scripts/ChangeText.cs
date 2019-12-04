using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Experimental;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class ChangeText : MonoBehaviour
{

    public float current_time = 0.0f;
    public int[] traintext = new int[] { 1, 2, 3, 4, 5, 6 };
    int arrownumber = 0;

    //bool blinkstate = true;
    Text text;

    // Use this for initialization
    void Start()
    {
        text = GetComponent<Text>();
    }

    // Update is called once per frame
    void Update()
    {
        current_time += Time.deltaTime;
        if (current_time < 2.0f)
        {
            if (arrownumber == 6)
            {
                text.text = "Finish";                
            }
            else text.text = "Wait...";
        }
        else if (current_time > 2.0f && current_time < 41.0f)
        {
            if (arrownumber == 0)
            {
                PrintNextArrow(traintext[arrownumber]);
            }
            else if (arrownumber == 1)
            {
                PrintNextArrow(traintext[arrownumber]);
            }
            else if (arrownumber == 2)
            {
                PrintNextArrow(traintext[arrownumber]);
            }
            else if (arrownumber == 3)
            {
                PrintNextArrow(traintext[arrownumber]);
            }
            else if (arrownumber == 4)
            {
                PrintNextArrow(traintext[arrownumber]);
            }
            else if (arrownumber == 5)
            {
                PrintNextArrow(traintext[arrownumber]);
            }
        }
        else if (current_time > 41.0f)
        {
            current_time = 0.0f;
            arrownumber++;
            //blinkstate = true;
        }
    }

    void PrintNextArrow(int arrow)
    {
        if (arrow == 1)
        {            
            text.text = "Look at    1    button";
        }
        else if (arrow == 2)
        {            
            text.text = "Look at    2    button";
        }
        else if (arrow == 3)
        {            
            text.text = "Look at    3    button";
        }
        else if (arrow == 4)
        {
            text.text = "Look at    4    button";
        }
        else if (arrow == 5)
        {
            text.text = "Look at    5    button";
        }
        else if (arrow == 6)
        {
            text.text = "Look at    6    button";
        }
    }
}