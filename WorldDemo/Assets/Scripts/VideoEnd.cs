using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Experimental;
using UnityEngine.Video;
using UnityEngine.SceneManagement;



public class VideoEnd : MonoBehaviour {

    float current_time;
    private VideoPlayer m_VideoPlayer;
	// Use this for initialization
	void Start () {
        m_VideoPlayer = GetComponent<VideoPlayer>();
	}
	
	// Update is called once per frame
	void Update () {
        current_time += Time.deltaTime;

        //m_VideoPlayer.Play();
        if (current_time > 2.0f)
            if (!m_VideoPlayer.isPlaying) {
                SceneManager.LoadScene("Main"); 
            }
	}
}
