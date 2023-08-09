using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//public class GlobalExceptionHandler : MonoBehaviour
/////<summary>
///// failing silently is terrible for development. Here I'm trying to 
///// develop and object to catch all global unhandled exceptions. 
/////</summary>
public class ExceptionManager : MonoBehaviour
{
    void OnEnable()
    {
        Application.logMessageReceived += LogCallback;
    }

    //Called when there is an exception
    void LogCallback(string condition, string stackTrace, LogType type)
    {
        Debug.Log(condition);
    }

    void OnDisable()
    {
        Application.logMessageReceived -= LogCallback;
    }

}


//{
//    void Awake()
//    {
//        Application.logMessageReceived += LogCaughtException;
//        DontDestroyOnLoad(gameObject);
//    }

//    void LogCaughtException(string logText, string stackTrace, LogType logType)
//    {
//        if (logType == LogType.Exception)
//        {
//            Debug.LogException(logType.);
//        }
//    }
//}



// alternative to try:



//{
//    void OnEnable()
//    {
//        Application.logMessageReceived += LogCallback;
//    }

//    //Called when there is an exception
//    void LogCallback(string condition, string stackTrace, LogType type)
//    {
//        //Send Email
//    }

//    void OnDisable()
//    {
//        Application.logMessageReceived -= LogCallback;
//    }
//}
