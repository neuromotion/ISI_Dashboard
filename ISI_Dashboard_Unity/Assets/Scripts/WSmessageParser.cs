using System;
using System.Collections;
using System.Collections.Generic;
//using UnityEditor.Experimental.GraphView;
using UnityEngine;
using WebSocketSharp;           //installed with NuGetForUnity
using Newtonsoft.Json.Linq;     //installed with NuGetForUnity
using Newtonsoft.Json;


/// <summary>
/// outline general approach 
/// recieve the string representation of the JSON.
/// what we have is a message in a message. so the outer wrapper has information about the message type,
/// and then depending on the message type, we need to handle the deserializtaion differently, by passing
/// in a different object.
/// the approach will be to read the string parse it into a json object, then use the message type as a switch to change the 
/// behavior. we will used side effects of the deserialzation callback to update system state, and then objects will rely on this. 
/// </summary>
/// 


// could also call this a descerializer, because that is more accurate. 


public class WSmessageParser : MonoBehaviour
/// <summary>
/// the WS (WebSocket Client) message Parser talks to the websockets server located
/// on the box and parses the messages out into accessable datastructures within
/// unity. Objects within Unity then access this data as changes trickle in and
/// update what they display. 
/// </summary>
{
    public SOH soh;
    public List<StimGroup> stimGroups;
    private WebSocket ws;

    private void Start()
    {
        // Initialize objects
        InitObjs();

        // Establish WebSocket connection
        //string ip_addr = "192.168.42.1";
        string ip_addr = "192.168.42.150";
        string port = "7890";
        string url = "ws://" + ip_addr + ":" + port;
        ws = new WebSocket(url);
        ws.Connect();

        // perform handshake with the box server to become a listener on reciept of first message
        ws.OnMessage += ShakeHands;

        //ws.OnMessage += (sender, e) =>
        //{
        //    Debug.Log("Message Received from " + ((WebSocket)sender).Url + ", Data : " + e.Data);
        //};
    }


    private void ShakeHands(object sender, MessageEventArgs e)
    ///<summary>
    /// have to shake hands with the box server and request / subscribe to be a listener
    ///</summary>
    {
        if (e.Data == "ID_REQ")
        {
            // request to be a logger
            string loggerID = "1";
            ws.Send(loggerID);
            Debug.Log("Message Received from " + ((WebSocket)sender).Url + ", Data : " + e.Data);
            
            // deregister this event handler - done shaking hands
            ws.OnMessage -= ShakeHands;

            // register parse message event listener.
            ws.OnMessage += DeserializeMessage;
        }

        // don't currently recieve an ID_ACK, could debug in future, but for now just leave it.
        //if (e.Data == "ID_ACK")
        //{
        //    // check if we are listener before we break.
        //}
    }

    private void DeserializeMessage(object sender, MessageEventArgs e)
    ///<summary>
    /// parse the incoming server message into a set of data objects
    /// that will be used to update Dashboard behavior.
    ///</summary>
    {
        //Log recieved data to console.
        //Debug.Log("Message Received from " + ((WebSocket)sender).Url + ", Data : " + e.Data);

        // parse input json string into a json object
        JObject jsonMsg = JObject.Parse(e.Data);
        Debug.Log("JSON message type:" + jsonMsg["msg_type"]);

        // deserialize SOH packet
        if ((string)jsonMsg["msg_type"] == "soh_json")
        {
            try
            {
                soh = JsonConvert.DeserializeObject<SOH>(jsonMsg["msg"].ToString());
                //Debug.Log(soh.aspectRatio);
            }
            catch (Exception ex)
            {
                Debug.LogException(ex, this);
            }
        }

        //deserialize stim_ack_json packet
        else if ((string)jsonMsg["msg_type"] == "stim_ack_json")
        {
            try
            {
                stimGroups = JsonConvert.DeserializeObject<List<StimGroup>>(jsonMsg["msg"].ToString());
                //Debug.Log(JsonConvert.SerializeObject(stimGroups[0]));
            }
            catch (Exception ex)
            {
                Debug.LogException(ex, this);
            }
        }

        else
        {
            //Debug.LogError("message type deserializer not yet defined.(check spelling)"); 
        }

    }

    void InitObjs()
    // place empty values into some of the deserialized objects to avoid
    // "Object Reference not set to instance of object" errors
    // is there a better way to do this>?
    {
        soh = new SOH();
        soh.Gnd = new uint[0];
        soh.Ref = new uint[0];
        
        stimGroups = new List<StimGroup>();
    }

    void OnApplicationQuit()
    {
        ws.Close();  //gracefully close out the websocket connection.
    }
}



/// deserialized objects: 
// deserialize handles the following 2 senarios gracefully:
//      incomplete reading of the JSON object (forgetting a field)
//      asking to fill in a field that doesn't exist in the JSON (it instantiates the field as Null)
// problems arise only when the datatype specified in the class object is incompatable with what is present in the JSON

public class SOH
/// <summary>
/// the deserialized version of the soh_json message string. 
/// </summary>
{
    public ulong curTime_ns {get; set; }
    public float unixTime {get; set; }
    public ulong nipTime_30k {get; set; }

    //public string fieldIknowIsNotThere { get; set; } 
    public string[] connectedLoggers {get; set; }
    public string[] connectedReadOnly {get; set; }
    public string[] connectedReadWrite {get; set; }

    public int stimResCaud {get; set; }
    public int StimResRost {get; set; }

    [JsonProperty(PropertyName = "gnd")] 
    public uint[] Gnd {get; set; }
    [JsonProperty(PropertyName = "ref")]    //this decorator is required because ref is a C# keyword
    public uint[] Ref {get; set; }

    public float aspectRatio {get; set; }

}

public class StimGroup
{
    public uint[] elecCath { get; set; }
    public uint[] elecAno { get; set; }
    public float amp { get; set; }
    public float freq { get; set; }
    public float pulseWidth { get; set; }
    public uint isContinuous { get; set; }
}


//{"client_ip": "192.168.42.150", "client_id": 0, "msg_type": "stim_ack_json", "msg": "[{\"elecCath\": [1, 12], \"elecAno\": [3, 4], \"amp\": 300, \"freq\": 20, \"pulseWidth\": 100, \"isContinuous\": 0, \"res\": 0, \"nipTime\": 0, \"time\": 13317421304400}, {\"elecCath\": [7, 8], \"elecAno\": [9, 10], \"amp\": 200, \"freq\": 30, \"pulseWidth\": 167, \"isContinuous\": 0, \"res\": 0, \"nipTime\": 0, \"time\": 13317421304400}]"}





// notes and refs: 
// https://medium.com/unity-nodejs/websocket-client-server-unity-nodejs-e33604c6a006 //good intro to using WS with Unity
// https://github.com/GlitchEnzo/NuGetForUnity   // how to get NuGet packages into unity
// https://github.com/sta/websocket-sharp       // a websocket package for C# 

// https://code-maze.com/csharp-read-and-process-json-file/ for deserializing example. 

// Requirement 5.2.13:  Device Set Embedded Configuration