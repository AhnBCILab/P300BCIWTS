using UnityEngine;
using System.Collections;
using UnityEngine.UI;
using System.IO;
using UnityEngine.Video;

public class SurveyScript : MonoBehaviour
{
    public GameObject[] questionGroupArr;
    public QAClass[] qaArr;
    public GameObject AnswerPanel;
    public GameObject StartPanel;
    public GameObject QuestionPanel;
    public GameObject QuestionPanel2;
    public GameObject QuestionPanel3;
    public GameObject VideoPanel;

    int first;
    string patient_name = "";
    // Start is called before the first frame update
    void Start()
    {
        first = 0;
        qaArr = new QAClass[questionGroupArr.Length];
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void SubmitAnswer()
    {
        for (int i = 0; i < qaArr.Length; i++)
        {
            qaArr[i] = ReadQuestionAndAnswer(questionGroupArr[i]);
        }

        DisplayResult();
    }
    QAClass ReadQuestionAndAnswer(GameObject questionGroup)
    {
        QAClass result = new QAClass();
        GameObject q = questionGroup.transform.Find("Question").gameObject;
        GameObject a = questionGroup.transform.Find("Answer").gameObject;

        result.Question = q.GetComponent<Text>().text;

        if (a.GetComponent<ToggleGroup>() != null)
        {
            for (int i = 0; i < a.transform.childCount; i++)
            {
                if (a.transform.GetChild(i).GetComponent<Toggle>().isOn)
                {
                    result.Answer = a.transform.GetChild(i).Find("Label").GetComponent<Text>().text;
                    break;
                }
            }
        }
        else if (a.GetComponent<InputField>() != null)
        {
            result.Answer = a.transform.Find("Text").GetComponent<Text>().text;
            if(first == 0)
            {
                patient_name = result.Answer;
                first++;
            }
        }
        else if (a.GetComponent<ToggleGroup>() == null && a.GetComponent<InputField>() == null)
        {
            string s = "";
            int counter = 0;

            for (int i = 0; i < a.transform.childCount; i++)
            {
                if (a.transform.GetChild(i).GetComponent<Toggle>().isOn)
                {
                    if (counter != 0)
                    {
                        s = s + ", ";
                    }
                    s = s + a.transform.GetChild(i).Find("Label").GetComponent<Text>().text;
                    counter++;
                }

                if(i == a.transform.childCount - 1)
                {
                    s = s + ".";
                }
            }

            result.Answer = s;
        }
        return result;
    }
    public void SurveyStart()
    {
        StartPanel.SetActive(false);
        QuestionPanel.SetActive(true);
    }
    public void NextSection()
    {
        QuestionPanel.SetActive(false);
        QuestionPanel2.SetActive(true);
    }
    public void LastSection()
    {
        QuestionPanel2.SetActive(false);
        QuestionPanel3.SetActive(true);
    }
    public void VideoSection()
    {
        AnswerPanel.SetActive(false);
        VideoPanel.SetActive(true);
    }

    void DisplayResult()
    {
        QuestionPanel3.SetActive(false);
        AnswerPanel.SetActive(true);

        string s = "";

        for(int i = 1; i < qaArr.Length; i++)
        {
            s = s + qaArr[i].Question + "\n";
            s = s + qaArr[i].Answer + "\n\n";
        }

        //AnswerPanel.transform.Find("Answer").GetComponent<Text>().text = s;

        FileStream f = new FileStream(Application.dataPath + "/StreamingAssets" + "/" + patient_name + ".txt", FileMode.Create, FileAccess.Write);

        StreamWriter writer = new StreamWriter(f, System.Text.Encoding.Unicode);
        writer.WriteLine(s);
        writer.Close();
    }

    public void Exit()
    {
        Application.Quit();
    }
}

[System.Serializable]
public class QAClass
{
    public string Question = "";
    public string Answer = "";
}