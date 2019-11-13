using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ChangeOrder : MonoBehaviour
{
    public Text txt;
    public int random = 0;
    public string path = "";

    // Start is called before the first frame update
    void Start()
    {
        random = Random.Range(1, 7);
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
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
