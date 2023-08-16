using Newtonsoft.Json;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Unity.Collections;
using Unity.VisualScripting;
using UnityEngine;

public class ElectrodeBuilder : MonoBehaviour
{
    ///<summary>
    /// The electrode builder class is attached to an electrode array object,
    /// and is responsible for initializing and updating the display state
    /// of each electrode array object
    ///</summary>

    // set electrode location
    public enum ElectrodeLocation { Caudal, Rostral }
    public ElectrodeLocation electrodeLocation;    // handle behavior that with location.

    // external objects passed in by reference
    public ElectrodePinConversion conversion;
    public WSmessageParser messageParser;
    public GameObject ElectrodeFrame;

    //sprite sheet definitions - no need to access by filename
    public Sprite OffSprite;
    public Sprite[] AnodeSprites;
    public Sprite[] CathodeSprites;
    public Sprite[] RefSprites;
    public Sprite[] GndSprites;

    // the visual electrode game objects
    private GameObject[] Electrodes;
    private int nElectrodes = 32;

    // Start is called before the first frame update
    void Start()
    {
        // initialize electrode array in the off state
        InitElectrodeArray();
    }

    // Update is called once per frame
    void Update()
    {
        UpdateElectrodeArray();
    }


    void InitElectrodeArray()
    /// draws the off electrodes on top of the frame, with the right spacing
    {
        // draw each gray dot at it's desired location
        IEnumerable<int> electrodeRange = Enumerable.Range(1, nElectrodes);
        Electrodes = new GameObject[nElectrodes];
        foreach (int pin in electrodeRange) // pin value is 1-indexed PPM value
        {
            // initialize electrodes and sprite renderer
            Electrodes[pin - 1] = new GameObject();                                          // construct a new GO
            Electrodes[pin - 1].name = "Electrode: " + pin.ToString();                       // set name 
            Electrodes[pin - 1].transform.SetParent(this.GetComponent<Transform>());         // set parent
            Electrodes[pin - 1].AddComponent<SpriteRenderer>();                              // add a Sprite Renderer
            Electrodes[pin - 1].GetComponent<SpriteRenderer>().sprite = OffSprite;           // init with off sprite
            Electrodes[pin - 1].GetComponent<SpriteRenderer>().sortingOrder = 1;             // put ontop of frame

            // parametrically position the electrodes relative to the Electroframe Sprite
            float xbound = ElectrodeFrame.GetComponent<SpriteRenderer>().bounds.size.x;
            float ybound = ElectrodeFrame.GetComponent<SpriteRenderer>().bounds.size.y;
            //Debug.Log(xbound.ToString() + " " + ybound.ToString());
            float unitWidth = 4;
            float unitHeight = 9;
            float[] ygrid = { 4f, 3f, 2f, 1f, -1f, -2f, -3f, -4f };
            float[] xgrid = { -1.5f, -.5f, .5f, 1.5f };

            byte[] ij = conversion.PPM_2_IJ((byte)pin);

            float x = ((xbound * xgrid[ij[1]]) / unitWidth);  // localScale;
            float y = ((ybound * ygrid[ij[0]]) / unitHeight); // localScale;

            Vector3 pos = new Vector3(x, y);
            Electrodes[pin - 1].transform.localPosition = pos + ElectrodeFrame.transform.position;

            // properly size the electrodes using a parameter relating the electrode radius to spacing.
            float rl_quotient = .4f;              // ratio of radius to electrode spacing l <0 , .5>  == <not there , tangential>
            float l = xbound / unitWidth;
            float targetRad = l * rl_quotient;       // [unity units]

            float currentDia = Electrodes[pin - 1].GetComponent<SpriteRenderer>().bounds.size.x;
            float scaleFactor = (targetRad / (currentDia / 2));   //[unity units]
            Electrodes[pin - 1].GetComponent<SpriteRenderer>().transform.localScale = Vector3.one * scaleFactor;

        }
    }

    void UpdateElectrodeArray()
    /// update electrode array graphic with pin information coming from the Websocket server.
    {
        // blank all electrodes to avoid maintaining duplicate state.
        foreach (GameObject electrode in Electrodes)
        {
            electrode.GetComponent<SpriteRenderer>().sprite = OffSprite;
        }


        // render anodes
        List<uint> anodes = new List<uint>();
        foreach (StimGroup sg in messageParser.stimGroups) { anodes.AddRange(sg.elecAno.ToList()); }
        uint[] _anodes = Should_I_render(anodes.ToArray());

        foreach (uint pin in _anodes)
        {
            uint _pin = (pin - 1) % 128; 
            Electrodes[_pin].GetComponent<SpriteRenderer>().sprite = AnodeSprites[conversion.PPM_2_UAS((byte)pin)];
        }

        // render cathodes
        List<uint> cathodes = new List<uint>();
        foreach (StimGroup sg in messageParser.stimGroups) { cathodes.AddRange(sg.elecCath.ToList()); }
        uint[] _cathodes = Should_I_render(cathodes.ToArray());

        foreach (uint pin in _cathodes)
        {
            uint _pin = (pin - 1) % 128;
            Electrodes[_pin].GetComponent<SpriteRenderer>().sprite = CathodeSprites[conversion.PPM_2_UAS((byte)pin)];
        }

        // render Gnds
        uint[] gnds = Should_I_render(messageParser.soh.Gnd);
        foreach (uint pin in gnds)
        {
            uint _pin = (pin - 1) % 128;
            Electrodes[_pin].GetComponent<SpriteRenderer>().sprite = GndSprites[conversion.PPM_2_UAS((byte)pin)];
        }

        // render Refs
        uint[] refs = Should_I_render(messageParser.soh.Ref);
        foreach (uint pin in refs)
        {
            uint _pin = (pin - 1) % 128;
            Electrodes[_pin].GetComponent<SpriteRenderer>().sprite = RefSprites[conversion.PPM_2_UAS((byte)pin)];
        }


    }

    uint[] Should_I_render(uint[] pins)
    // depending on if this electrode is caudal or rostral it either is or is not
    // the responsibility of this ElectrodeBuilder instanct to render the pin in the scene
    {
        //init return arrays
        List<uint> pinsToRender;
        List<uint> caudalPins = new List<uint>();
        List<uint> rostralPins = new List<uint>();

        //filter to appropriate list
        foreach (uint pin in pins)
        {
            if (pin > 128) { rostralPins.Add(pin); }
            else { caudalPins.Add(pin); }
        }

        if (electrodeLocation == ElectrodeLocation.Caudal)
        {
            pinsToRender = caudalPins;
        }
        else //rostral
        {
            pinsToRender = rostralPins;
        }

        return pinsToRender.ToArray();
    }
}



// notes and refs:
// https://gamedevbeginner.com/how-to-change-a-sprite-from-a-script-in-unity-with-examples/#:~:text=Creating%20a%20Sprite%20array%20is,declare%20it%20as%20an%20array.&text=Next%20we%20need%20to%20add%20the%20Sprites%20to%20the%20array.
// on loading sprite sheets