using System.Collections;
using System.Collections.Generic;
using UnityEngine.SceneManagement;
using UnityEngine;
using System.IO;
using UnityEngine.Experimental;

public class OnlineButton : MonoBehaviour
{

    // Use this for initialization
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {

    }
    public void ChangeGameScene()
    {
        FileInfo fi = new FileInfo(Application.dataPath + "/StreamingAssets/" + InputName.patient_id + ".txt");
        if (fi.Exists) InputName.patient_id = InputName.Real_id + InputName.number;
        InputName.number = InputName.number + 1;
        SceneManager.LoadScene("Main");
    }
}