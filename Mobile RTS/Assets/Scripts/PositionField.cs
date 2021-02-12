using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

public class PositionField
{
    public List<Vector3> Positions { get; private set; } = new List<Vector3>();

    public PositionField(Vector3 target, int count, float spacing)
    {
        Positions.Add(target);

        Vector3 deviation = Vector3.zero;

        for (int i = 0; i < count-1; i++)
        {
            Vector3 direction = Quaternion.Euler(0, 90 * (i % 4), 0) * Vector3.right;
            deviation += direction * spacing * ((i - 1) / 2 + 1);

            Positions.Add(target + deviation);
        }
    }

    public Vector3 AllocatePosition(NavMeshAgent agent)
    {
        Vector3 agentPosition = agent.transform.position;

        float shortestDistance = float.PositiveInfinity;
        Vector3 nearestPosition = Positions[0];

        foreach (Vector3 i in Positions)
        {
            float distance = Vector3.Distance(agentPosition, i);

            if (distance < shortestDistance)
            {
                shortestDistance = distance;
                nearestPosition = i;
            }
        }

        Positions.Remove(nearestPosition);

        return nearestPosition;
    }
}
