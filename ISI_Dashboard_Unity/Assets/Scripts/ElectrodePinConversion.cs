using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices.WindowsRuntime;
using UnityEngine;

public class ElectrodePinConversion : MonoBehaviour
{
    /// <summary>
    /// The ElectrodePinConversion class performs conversions from 
    /// one pin representation into another. 
    /// 
    /// the input to the pin conversion class will always be the 
    /// Preferend_pin_map, as this is what is passed in over websockets 
    /// from the box. 
    /// 
    /// 2 coordinate representations include: 
    ///     I,J - the array representation of the PPM
    ///     X,Y - where a PPM centerpoint should land on the screen, relative to an origin in the lower left hand corner. 
    ///     
    /// 1 coordinate represenations include:
    ///     PPM - this is the pefered pin mapping used by the ISI team
    ///     UAS - Unity_Auto_Slicer, when sprite sheets are read in automatically form Inkscape into Unity, Unity uses a rigth to left raster pattern. 
    ///     
    /// while we could use a function based approach, we will in general prefer the more explicit indexing based approach. 
    /// </summary>
    /// 

    //Prefered_Pin_Mapping
    private readonly byte rostral_shift = 128;
    private readonly byte[,] PPM = new byte[8,4] {{ 8 , 16 , 24 , 32 },
                                                  { 7 , 15 , 23 , 31 },
                                                  { 6 , 14 , 22 , 30 },
                                                  { 5 , 13 , 21 , 29 },
                                                  { 4 , 12 , 20 , 28 },
                                                  { 3 , 11 , 19 , 27 },
                                                  { 2 , 10 , 18 , 26 },
                                                  { 1 ,  9 , 17 , 25 }};

    //Unity Auto Slicer
    private readonly byte[,] UAS = new byte[8,4] {{  0 ,  1 ,  2 ,  3 },
                                                  {  4 ,  5 ,  6 ,  7 },
                                                  {  8 ,  9 , 10 , 11 },
                                                  { 12 , 13 , 14 , 15 },
                                                  { 16 , 17 , 18 , 19 },
                                                  { 20 , 21 , 22 , 23 },
                                                  { 24 , 25 , 26 , 27 },
                                                  { 28 , 29 , 30 , 31 }};

    ///<summary>
    /// takes a Prefered_Pin index and calculates the I and J indicies that would
    /// retrieve the pin number from the PPM matrix.
    /// </summary>
    public byte[] PPM_2_IJ(byte PreferedPin) 
    {
        //handle if PPM is for a rostral array
        if (PreferedPin > rostral_shift){ PreferedPin -= 128;}

        //calculate I and J with formulat
        byte I = (byte)(7 - ((PreferedPin - 1) % 8));     // find the row
        byte J = (byte)((PreferedPin - 1) / 8);           // find col
        return new byte[] { I, J };
    }

    ///<summary>
    /// takes a Prfered Pin Map Index and calculates the Unity_Auto_Slicer that will 
    /// retrieve the proper sprite from the sprite sheet.
    /// </summary>
    public byte PPM_2_UAS(byte PreferedPin)
    {
        byte[] IJ = PPM_2_IJ(PreferedPin);
        return UAS[IJ[0], IJ[1]];
    }
}
