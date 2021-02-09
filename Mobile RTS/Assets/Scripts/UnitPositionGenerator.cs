using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UnitPositionGenerator
{
    private Vector3 target;
    private Vector3 deviation = Vector3.zero;
    private float spacing;
    public int Index { get; private set; } = -1;

    public UnitPositionGenerator(Vector3 target, float spacing)
    {
        this.target = target;
        this.spacing = spacing;
    }

    public Vector3 Next()
    {
        Vector3 direction = Quaternion.Euler(0, 90 * (Index % 4), 0) * Vector3.right;
        deviation += direction * spacing * ((Index - 1) / 2 + 1);

        Index++;

        return target + deviation;
    }
}
