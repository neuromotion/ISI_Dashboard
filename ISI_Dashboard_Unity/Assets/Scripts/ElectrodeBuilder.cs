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
    public enum ElectrodeLocation{Caudal,Rostral}  
    public ElectrodeLocation electrodeLocation;    // handle behavior that with location.

    // external objects passed in by reference
    public ElectrodePinConversion conversion;
    public WSmessageParser messageParser;
    public GameObject ElectrodeFrame; 

    //sprite sheet definitions - no need to access by filename
    public Sprite[] OffSprites;
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

    //draws the electrode array in the parent frame
    void InitElectrodeArray()
    /// for now this will draw just just the null instances, but we will modify it later.
    {
        // handle caudal vs. rostral electrode range. //maybe we don't need this, as we have designed code to felxably handle this using rostral shift.
        //IEnumerable<int> electrodeRange = Enumerable.Range(1, 32);  //caudal
        //if (electrodeLocation == ElectrodeLocation.Rostral) { electrodeRange = Enumerable.Range(129, 160); }

        // you have to account for the local scale in all positioning and scaling operations
        //float localScale = this.GetComponent<Transform>().localScale.x;

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
            Electrodes[pin - 1].GetComponent<SpriteRenderer>().sprite = OffSprites[pin - 1]; // init with off sprite
            Electrodes[pin - 1].GetComponent<SpriteRenderer>().sortingOrder = 1;             // put ontop of frame

            // parametrically position the electrodes relative to the Electroframe Sprite
            float xbound = ElectrodeFrame.GetComponent<SpriteRenderer>().bounds.size.x;
            float ybound = ElectrodeFrame.GetComponent<SpriteRenderer>().bounds.size.y;
            Debug.Log(xbound.ToString() + " " + ybound.ToString());
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


    //// You could also use Sprite.bounds for this.
    //float spriteHeight = spriteRenderer.sprite.rect.height
    //                   / spriteRenderer.sprite.pixelsPerUnit;

    //// How many times bigger (or smaller) is the height we want to fill?
    //float scaleFactor = visibleHeightAtDepth / spriteHeight;

    //// Scale to fit, uniformly on all axes.
    //spriteRenderer.transform.localScale = Vector3.one* scaleFactor;


    /// can we position the electrodes parametrically???

    public  void positionElectrodes()

    {

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