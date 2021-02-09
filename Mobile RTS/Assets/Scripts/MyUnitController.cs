using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Unit))]
public class MyUnitController : MonoBehaviour
{
    [SerializeField] private Material normalMaterial;
    [SerializeField] private Material selectedMaterial;

    private Unit unit;

    private CursorController cursor;

    private void Start()
    {
        unit = GetComponent<Unit>();

        cursor = GameObject.FindObjectOfType<CursorController>();
    }

    private void Update()
    {
        if (unit.selected)
        {
            GetComponent<MeshRenderer>().material = selectedMaterial;
        }
        else
        {
            GetComponent<MeshRenderer>().material = normalMaterial;
        }
    }
}
