using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class ChangeText : MonoBehaviour {

    public float current_time = 0.0f;
    public string[] traintext = new string[] { "↑", "↓", "←", "→" };
    int arrownumber = 0;
    //bool blinkstate = true;
    Text text;

	// Use this for initialization
	void Start () {
        text = GetComponent<Text>();
	}
	
	// Update is called once per frame
	void Update () {
        current_time += Time.deltaTime;
        if (current_time < 10.0f)
        {
            if(arrownumber == 4)
            {
                text.text = "Finish";
                if (current_time > 5.0f) SceneManager.LoadScene("Menu");
            }
            else text.text = "Wait...";
        }
        else if (current_time > 10.0f && current_time < 30.0f)
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
        }
        else if (current_time > 30.0f)
        {
            current_time = 0.0f;
            arrownumber++;
            //blinkstate = true;
        }
    }

    void PrintNextArrow (string arrow)
    {
        if (arrow.Equals("↑"))
        {
            //text.text = traintext[0] + traintext[1] + traintext[2] + traintext[3] + "(↑)";
            text.text = "Look at the UP arrow";
        }
        else if (arrow.Equals("↓"))
        {
            //text.text = traintext[0] + traintext[1] + traintext[2] + traintext[3] + "(↓)";
            text.text = "Look at the DOWN arrow";
        }
        else if (arrow.Equals("←"))
        {
            //text.text = traintext[0] + traintext[1] + traintext[2] + traintext[3] + "(←)";
            text.text = "Look at the LEFT arrow";
        }
        else if (arrow.Equals("→"))
        {
            //text.text = traintext[0] + traintext[1] + traintext[2] + traintext[3] + "(→)";
            text.text = "Look at the RIGHT arrow";
        }
    }
}
