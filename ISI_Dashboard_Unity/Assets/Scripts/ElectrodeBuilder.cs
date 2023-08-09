using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using Unity.VisualScripting;
using UnityEngine;

public class ElectrodeBuilder : MonoBehaviour
{
    ///<summary>
    /// The electrode builder class is attached to an electrode array object,
    /// and is responsible for initializing and updating the display state
    /// of each electrode array object
    ///</summary>

    public enum ElectrodeLocation{Caudal,Rostral}  
    public ElectrodeLocation electrodeLocation;    // handle behavior that with location.

    public ElectrodePinConversion conversion;
    public WSmessageParser messageParser;

    //sprite sheet definitions - no need to access by filename
    public Sprite[] OffSprites;
    public Sprite[] AnodeSprites;
    public Sprite[] CathodeSprites;
    public Sprite[] RefSprites;
    public Sprite[] GndSprites;

    private GameObject[] Electrodes;                // the visual electrodes - game objects
    private int nElectrodes = 32; 

    // Start is called before the first frame update
    void Start()
    {
        //initialize electrode array in the off state
        InitElectrodeArray();

    }

    // Update is called once per frame
    void Update()
    {
        UpdateElectrodeArray();
    }

    //draws the electrode array in the parent frame
    void InitElectrodeArray()
    /// for now this will draw just just the null instances, but we will modify it later.
    {
        // handle caudal vs. rostral electrode range. //maybe we don't need this, as we have designed code to felxably handle this using rostral shift.
        //IEnumerable<int> electrodeRange = Enumerable.Range(1, 32);  //caudal
        //if (electrodeLocation == ElectrodeLocation.Rostral) { electrodeRange = Enumerable.Range(129, 160); }

        // Init empty game objects with sprite renderers? // no, build them 

        // draw each gray dot at it's desired location
        IEnumerable<int> electrodeRange = Enumerable.Range(1, nElectrodes);
        Electrodes = new GameObject[nElectrodes];
        foreach (int pin in electrodeRange)
        {
            // initialize electrodes and sprite renderer
            Electrodes[pin - 1] = new GameObject();                                          // construct a new GO
            Electrodes[pin - 1].name = "Electrode: " + pin.ToString();                       // set name 
            Electrodes[pin - 1].transform.SetParent(this.GetComponent<Transform>());         // set parent
            Electrodes[pin - 1].AddComponent<SpriteRenderer>();                              // add a Sprite Renderer
            Electrodes[pin - 1].GetComponent<SpriteRenderer>().sprite = OffSprites[pin - 1];   // init with off sprite

            // set the position of each electrode
            float scaleFactor = .005f;
            float[] xy = PPM_2_XY((byte)pin, scaleFactor);
            var pos = new Vector3(xy[0], xy[1]);
            Electrodes[pin - 1].transform.localPosition = pos;
        }
    }

    ///<summary>
    /// takes a Prefered Pin Map Index and a scale factor, and calculates the coordinates in unity units.
    /// relative to the lower left corner rof the parent object, where the sprite should be placed. 
    /// 
    /// this includes added space for visual partitioning between the upper and lower blocks.
    /// </summary>
    public float[] PPM_2_XY(byte PreferedPin, float ScaleFactor)
    {
        //offsets from lower left corner, spacing
        float dx = -.50f;
        float dy = -.50f;
        float rowSpacing = 100;
        float colSpacing = 100;


        //calculate x and y
        byte rowNumber = (byte)((PreferedPin - 1) % 8);
        byte colNumber = (byte)((PreferedPin - 1) / 8);
        float visualGap = 0;
        if (rowNumber >= 4) { visualGap = colSpacing / 2; }  // visually separate upper electrode group from lower

        float x = ScaleFactor * (dx + colNumber * colSpacing);
        float y = ScaleFactor * (dy + rowNumber * rowSpacing + visualGap);
        return new float[] { x, y };
    }
    



    // ok, let's think through how to do this?
    // we will have an initial function that that Initializes drawing the elelctrode array with grays. 
    // in this function, we will create the initial sprites using sprite.create. this will set the initial appearance and location
    // of the sprint. the location for this animation never needs to change. 

    // in the update function, you won't be creating new sprites, but updating the texture that is being rendered. 
    // one question is whether you need to cache any local state, or if we can make our application functional / stateless. 
    // 
    // the core problem I'm thinking though right now
    // is it possible to efficiently update the state without a copy of the state, because then I have to maintain state
    // wait, are we going to have to read from disk everytime? that would be slow (probably fine for our application thought)

    // let's go with a stateless approach that is more costly but lower complexity, then add caching and complexity as needed.

    // ok, so we need a game object with a sprite renderer attached to it for each electrode, then we change out the sprite component / texture as required?? 
    // might be a good idea to load / cache all of the sprite? 
    // also, let's make the sprites way smaller...
    // the game object will let us move / position the sprite relative to the parent game object. 
    // so we need to create a bunch of child game objects, then position them. 

    // another question is how do I handle left vs. right behavior while keeping things dry?


    void UpdateElectrodeArray()
    {

    }
}



// notes and refs:
// https://gamedevbeginner.com/how-to-change-a-sprite-from-a-script-in-unity-with-examples/#:~:text=Creating%20a%20Sprite%20array%20is,declare%20it%20as%20an%20array.&text=Next%20we%20need%20to%20add%20the%20Sprites%20to%20the%20array.
// on loading sprite sheets