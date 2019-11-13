using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Experimental;
using UnityEngine.UI;

public class PanelControl : MonoBehaviour {

    public GameObject panel;
    public float current_time = 0.0f;
    
    // Use this for initialization
    void Start () {
        //panel = GetComponent<GameObject>();
        panel.SetActive(false);
    }
	
	// Update is called once per frame
	void Update () {
        current_time += Time.deltaTime;
        if (current_time > 5.0f)
        {
            panel.SetActive(true);
        }
    }
}
