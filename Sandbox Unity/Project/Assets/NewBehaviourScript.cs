using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour {

    public GameObject Box;
    public GameObject SideWallLeft;
    public GameObject SideWallRight;
    public GameObject BackWall;
    public GameObject FrontWall;
    public GameObject Ground;
    public GameObject Roof;
    public GameObject Sensor;

    public List<GameObject> BoxClones;
    public List<GameObject> SensorClones;
    public List<float> SensorReadings;

    public int NUM_SENSORS_X = 4;
    public int NUM_SENSORS_Z = 4;

    public float noise_mean = 0;
    public float noise_standard_deviation = 1;

    // Margin for boxes from the walls of the van
    float margin;
    // Half widths + margin
    float x2b;
    float y2b;
    float z2b;

    BoxCollider bc; // Box
    float VanHeight;

    bool loadingVan = false;
    bool fittingSensors = false;

    float total_volume = 0;

    // Use this for initialization
    void Start() {
        // y = height, x = depth, z = width

        BoxClones = new List<GameObject>();
        SensorClones = new List<GameObject>();
        SensorReadings = new List<float>();

        bc = Box.GetComponent<BoxCollider>();
        margin = 0.1f;
        x2b = (bc.bounds.size.x / 2) + margin;
        y2b = (bc.bounds.size.y / 2) + margin;
        z2b = (bc.bounds.size.z / 2) + margin;

        BoxCollider bc2 = BackWall.GetComponent<BoxCollider>();
        VanHeight = bc2.bounds.size.y;
    }

    /*
     * Load the van with a new random configuration of boxes
     */ 
    void loadTheVan()
    {
        // Remove all previous blocks
        foreach(GameObject go in BoxClones)
            Destroy(go);

        BoxClones.Clear();

        // Reduce the maximum number of boxes in the van by 5
        int height_fudge = (int)(5 * bc.bounds.size.y);

        float single_box_volume = bc.bounds.size.x * bc.bounds.size.y * bc.bounds.size.z;
        Debug.Log("Single box volume = " + single_box_volume);

        int max_num_boxes = (int)System.Math.Floor((Roof.transform.position.y - Ground.transform.position.y) / bc.bounds.size.y) - height_fudge;

        total_volume = 0;
        for (float z = SideWallLeft.transform.position.z + z2b; z < SideWallRight.transform.position.z; z += bc.bounds.size.z) // width
        {
            for (float x = BackWall.transform.position.x + x2b; x < FrontWall.transform.position.x; x += bc.bounds.size.x) // depth
            {
                int num_boxes = (int)Random.Range(0, max_num_boxes);

                for (float y = y2b; y < num_boxes; y += bc.bounds.size.y) // height
                {
                    Transform b = Instantiate(Box.transform, new Vector3(x, y, z), Quaternion.identity);
                    BoxClones.Add(b.gameObject);

                    total_volume += single_box_volume;
                }
            }
        }

        Debug.Log("Total occupied volume = " + total_volume);

        loadingVan = false;
    }

    /*
     * Add the sensors to the van and estimate the volume occupied
     */ 
    void fitSensors()
    {
        // Remove all previous blocks
        foreach (GameObject go in SensorClones)
            Destroy(go);

        SensorClones.Clear();

        // Remove all previous sensor readings
        SensorReadings.Clear();

        // Create a grid of sensors on the roof
        // --- TODO --- Center the grid of sensors
        float x_seperation = System.Math.Abs((BackWall.transform.position.x - FrontWall.transform.position.x) / NUM_SENSORS_X);
        float z_seperation = System.Math.Abs((SideWallRight.transform.position.z - SideWallLeft.transform.position.z) / NUM_SENSORS_Z);

        for (float z = SideWallLeft.transform.position.z + z2b; z < SideWallRight.transform.position.z; z += z_seperation) // width
        {
            for (float x = BackWall.transform.position.x + x2b; x < FrontWall.transform.position.x; x += x_seperation) // depth
            {
                Vector3 sensorPos = new Vector3(x, Roof.transform.position.y, z);
                Transform s = Instantiate(Sensor.transform, sensorPos, Quaternion.identity);
                SensorClones.Add(s.gameObject);

                // Calculate the distances from the sensors to the boxes
                RaycastHit hit;
                if (Physics.Raycast(sensorPos, Vector3.down, out hit, Mathf.Infinity))
                {
                    float noise = 0; //generateNormalRandom(noise_mean, noise_standard_deviation);
                    float measurement = hit.distance + noise;
                    Debug.Log(noise);

                    SensorReadings.Add(hit.distance);
                }

            }
        }

        // Estimate the occupied volume
        float occupied_volume_estimate = 0;
        for (int i = 0; i < SensorClones.Count; i++)
        {
            float box_height = (VanHeight - SensorReadings[i]); // How high are the stacked boxes below this sensor

            /*
             * This uses the assumption that all the boxes are of the same dimensions.
             * However, this is not the case, and so we could inject prior information on the distribution of
             * objects in the van to reduce the bias of the estimate at a tradeoff for higher variance. 
             * 
             * Aka formulating the problem in a bayesian context
             */ 
            occupied_volume_estimate += x_seperation * z_seperation * box_height;
        }

        Debug.Log("Estimated volume = " + occupied_volume_estimate);
        Debug.Log("Error = " + System.Math.Abs(occupied_volume_estimate - total_volume));
        fittingSensors = false;
    }

    /*void makeReadings()
    {
        // Calculate the distances from the sensors to the boxes
        RaycastHit hit;
        if (Physics.Raycast(sensorPos, Vector3.down, out hit, Mathf.Infinity))
        {
            float noise = 0; //generateNormalRandom(noise_mean, noise_standard_deviation);
            float measurement = hit.distance + noise;
            Debug.Log(noise);

            SensorReadings.Add(hit.distance);
        }
    }*/

    // Update is called once per frame
    void Update()
    {
        // The debug lines must be drawn every frame
        for (int i = 0; i < SensorClones.Count; i++)
        {
            Vector3 sensorPos = SensorClones[i].transform.position;
            Debug.DrawRay(sensorPos, Vector3.down * SensorReadings[i], Color.yellow);
        }

        if (loadingVan)
            loadTheVan();

        if (fittingSensors)
            fitSensors();

        if (Input.GetKeyDown(KeyCode.V))
        {
            Debug.Log("Loading the van...");
            loadingVan = true;
        }

        if (Input.GetKeyDown(KeyCode.S))
        {
            Debug.Log("Fitting the sensors...");
            fittingSensors = true;
        }
    }

    public static float generateNormalRandom(float mu, float sigma)
    {
        return Random.Range(-1, 1);

        // ---- TODO ----
        float rand1 = Random.Range(0, 1);
        float rand2 = Random.Range(0, 1);

        float n = Mathf.Sqrt(-2.0f * Mathf.Log(rand1)) * Mathf.Cos((2.0f * Mathf.PI) * rand2);

        return (mu + sigma * n);
    }

    } // End class
