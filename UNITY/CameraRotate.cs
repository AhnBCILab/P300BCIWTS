using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraRotate : MonoBehaviour {

    Cinemachine.CinemachineFreeLook cine;
	// Use this for initialization
	void Start () {
        cine = GetComponent<Cinemachine.CinemachineFreeLook>();
	}
	
	// Update is called once per frame
	void Update ()
    {
		if (Input.GetKey("a"))
        {
            cine.m_XAxis.Value = cine.m_XAxis.Value - 10.0f;

        }
        else if (Input.GetKey("d"))
        {
            cine.m_XAxis.Value = cine.m_XAxis.Value + 10.0f;
        }      
    }
}
