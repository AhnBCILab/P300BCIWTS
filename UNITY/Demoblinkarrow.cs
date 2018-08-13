using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Gamekit3D;
using UnityEngine;
using UnityEngine.UI;

public class Demoblinkarrow : MonoBehaviour
{
    public Cinemachine.CinemachineFreeLook cine;

    public static Demoblinkarrow Instance
    {
        get { return s_Instance; }
    }

    protected static Demoblinkarrow s_Instance;

    [HideInInspector]
    public bool playerControllerInputBlocked;

    protected Vector2 m_Movement;
    protected Vector2 m_Camera;
    protected bool m_Jump;
    protected bool m_Attack;
    protected bool m_Pause;
    protected bool m_ExternalInputBlocked;
    public Vector2 MoveInput
    {
        get
        {
            if (playerControllerInputBlocked || m_ExternalInputBlocked)
                return Vector2.zero;
            return m_Movement;
        }
    }
    public Vector2 CameraInput
    {
        get
        {
            if (playerControllerInputBlocked || m_ExternalInputBlocked)
                return Vector2.zero;
            return m_Camera;
        }
    }
    public bool JumpInput
    {
        get { return m_Jump && !playerControllerInputBlocked && !m_ExternalInputBlocked; }
    }
    public bool Attack
    {
        get { return m_Attack && !playerControllerInputBlocked && !m_ExternalInputBlocked; }
    }
    public bool Pause
    {
        get { return m_Pause; }
    }
    WaitForSeconds m_AttackInputWait;
    Coroutine m_AttackWaitCoroutine;

    const float k_AttackInputDuration = 0.03f;

    public Image UpArrow; //image to toggle
    public Image DownArrow; //image to toggle
    public Image LeftArrow; //image to toggle
    public Image RightArrow; //image to toggle  
    public int num_of_blink_arrow = 2;
    public float current_time = 0.0f;
    float m_current_time = 0.0f;

    public float interval = 0.1f;
    public float startDelay = 0.1f;
    public float timebetweenarrows = 0.1f;

    public int blinkcnt = 0;
    public int BlinkCount = 40;

    bool isBlinking = false;
    bool arrow0 = true, arrow1 = true, arrow2 = true, arrow3 = true;
    public int up = 0, down = 0, left = 0, right = 0;
    int count = 0;
    int buttonIndexNum = 0;
    int rndnum = 0;
    public string order = "";
    public int value = 4;

    string ipUIVAServer = "localhost";
    public string buttons;

    bool blinkstate = true;
    UIVA_Client theClient = null;

    Image pubimg;

    void Start()
    {
        cine = GetComponent<Cinemachine.CinemachineFreeLook>();

        m_AttackInputWait = new WaitForSeconds(k_AttackInputDuration);

        //if (s_Instance == null)
        //    s_Instance = this;
        //else if (s_Instance != this)
        //    throw new UnityException("There cannot be more than one PlayerInput script.  The instances are " + s_Instance.name + " and " + name + ".");

        theClient = new UIVA_Client(ipUIVAServer);
        UpArrow.enabled = true;
        DownArrow.enabled = true;
        LeftArrow.enabled = true;
        RightArrow.enabled = true;
    }
    private void Update()
    {
        current_time += Time.deltaTime;

        if (Input.GetKey("w"))
        {
            m_current_time = 0.0f;
            m_Movement.Set(0f, 0.5f);

        }
        else if (Input.GetKey("s"))
        {
            m_current_time = 0.0f;
            m_Movement.Set(0f, -0.5f);
        }
        if (Input.GetKey("a"))
        {
            cine.m_XAxis.Value = cine.m_XAxis.Value - 10.0f;

        }
        else if (Input.GetKey("d"))
        {
            cine.m_XAxis.Value = cine.m_XAxis.Value + 10.0f;
        }
        m_current_time += Time.deltaTime;

        if (m_current_time > 1.0)
        {
            m_Movement.Set(0f, 0f);
            m_current_time = 0.0f;
        }
        m_Jump = Input.GetButton("Jump");

        if (Input.GetButtonDown("Fire1"))
        {
            if (m_AttackWaitCoroutine != null)
                StopCoroutine(m_AttackWaitCoroutine);

            m_AttackWaitCoroutine = StartCoroutine(AttackWait());
        }

        m_Pause = Input.GetButtonDown("Pause");

        //Restart blinking
        if (current_time > 10.0f && blinkstate == true)
        {
            blinkstate = false;
            arrow0 = true;
            arrow1 = true;
            arrow2 = true;
            arrow3 = true;
            blinkcnt = 0;
            Blink();
        }
        else if (current_time > 30.0f)
        {
            current_time = 0.0f;
            blinkstate = true;
        }
    }
    IEnumerator AttackWait()
    {
        m_Attack = true;

        yield return m_AttackInputWait;

        m_Attack = false;
    }

    public bool HaveControl()
    {
        return !m_ExternalInputBlocked;
    }

    public void ReleaseControl()
    {
        m_ExternalInputBlocked = true;
    }

    public void GainControl()
    {
        m_ExternalInputBlocked = false;
    }


    public void Blink()
    {
        if (blinkcnt < BlinkCount)
        {
            rndnum = UnityEngine.Random.Range(0, 4);
            if (rndnum == 0 && arrow0 == true)
            {
                arrow0 = false;
                buttonIndexNum = 0;
                theClient.Press_O(buttonIndexNum);
                pubimg = UpArrow;

                if (isBlinking)
                    return;
                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 0 && arrow0 == false)
            {
                Blink();
            }
            else if (rndnum == 1 && arrow1 == true)
            {
                arrow1 = false;
                buttonIndexNum = 1;
                theClient.Press_O(buttonIndexNum);
                pubimg = DownArrow;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 1 && arrow1 == false)
            {
                Blink();
            }
            else if (rndnum == 2 && arrow2 == true)
            {
                arrow2 = false;
                buttonIndexNum = 2;
                theClient.Press_O(buttonIndexNum);
                pubimg = LeftArrow;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }
            }
            else if (rndnum == 2 && arrow2 == false)
            {
                Blink();
            }
            else if (rndnum == 3 && arrow3 == true)
            {
                arrow3 = false;
                buttonIndexNum = 3;
                theClient.Press_O(buttonIndexNum);
                pubimg = RightArrow;

                if (isBlinking)
                    return;

                if (pubimg != null)
                {
                    isBlinking = true;
                    InvokeRepeating("ToggleState", startDelay, interval);
                }

            }
            else if (rndnum == 3 && arrow3 == false)
            {
                Blink();
            }

            if (arrow0 == false && arrow1 == false && arrow2 == false && arrow3 == false)
            {
                arrow0 = true;
                arrow1 = true;
                arrow2 = true;
                arrow3 = true;
            }
        }
        else
        {
            theClient.GetDirectionData(out buttons);
            switch (buttons)
            {
                case "Zero":
                    value = 0;
                    m_current_time = 0.0f;
                    m_Movement.Set(0f, 0.5f);
                    break;
                case "One":
                    value = 1;
                    m_current_time = 0.0f;
                    m_Movement.Set(0f, -0.5f);
                    break;
                case "Two":
                    value = 2;
                    cine.m_XAxis.Value = cine.m_XAxis.Value - 20.0f;
                    break;
                case "Three":
                    value = 3;
                    cine.m_XAxis.Value = cine.m_XAxis.Value + 20.0f;
                    break;
                default:
                    break;
            }
        }

    }
    public void ToggleState()
    {
        pubimg.enabled = !pubimg.enabled;
        count++;
        if (count == num_of_blink_arrow)
        {
            CancelInvoke();
            blinkcnt++;

            if (rndnum == 0) up++;
            else if (rndnum == 1) down++;
            else if (rndnum == 2) left++;
            else right++;

            count = 0;
            isBlinking = false;
            Invoke("Blink", timebetweenarrows);
        }
    }
}