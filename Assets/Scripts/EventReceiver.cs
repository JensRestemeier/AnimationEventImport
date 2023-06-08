using UnityEngine;
using System;

public class EventReceiver : MonoBehaviour {
	public void Apple() {
		Debug.Log ("Apple()");
	}
	public void Banana(int i) {
		Debug.Log (String.Format ("Banana({0})", i));
	}
	public void Pear(float f) {
		Debug.Log (String.Format ("Pear({0})", f));
	}
	public void Raspberry(string s) {
		Debug.Log (String.Format ("Raspberry({0})", s));
	}
}
