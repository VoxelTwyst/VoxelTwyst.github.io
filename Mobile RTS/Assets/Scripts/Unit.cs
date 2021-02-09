using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;

[RequireComponent(typeof(NavMeshAgent))]
public class Unit : Entity
{
    public NavMeshAgent agent { get; private set; }
    public bool selected { get; private set; }

    private void Start()
    {
        agent = GetComponent<NavMeshAgent>();
    }

    public void MoveTo(Vector3 position)
    {
        agent.SetDestination(position);
    }

    public void Attack(Unit enemy)
    {
        Debug.Log("Tried to attack " + enemy.name);
    }

    public bool Select()  // Return true if unit can be selected
    {
        selected = true;
        return true;
    }

    public void Deselect()
    {
        selected = false;
    }
}
