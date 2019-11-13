using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Experimental;

public class MovingWorld : MonoBehaviour {

	// Use this for initialization
	//Transform tf;
	//public float speed = 30;
	void Start () {
		//tf = transform;
	}
	
	// Update is called once per frame

	 //public float xspeed= -1f;
	public float zspeed= -30f;
	
	void Update () {

		transform.Rotate(0, 0, zspeed * Time.deltaTime);

		// transform.Translate(xspeed, 0, 0);

		// if(transform.localPosition.x < -30f){
		
		// 	transform.localPosition = new Vector3(-15f, 0, 0);
		// }

		// tf.Rotate(0, 0, speed * Time.deltaTime);

		// if(transform.localRotation.z < speed){
		
		// 	transform.localRotation = new Vector3(0, 0, );
		// }

		//transform.Rotate(0, yspeed * Time.deltaTime, 0);


	}
}
