using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Entity : MonoBehaviour
{
    public void RecieveDamage(int damage)
    {
        Debug.Log("Took " + damage.ToString() + " damage");
    }
}
