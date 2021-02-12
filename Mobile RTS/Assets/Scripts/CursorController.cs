using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CursorController : MonoBehaviour
{
    private bool willSelect = false;
    private Stack<Unit> selected = new Stack<Unit>();

    private float lastTouchDistance;
    private Vector2 lastTouchAveragePosition;

    [SerializeField] private LayerMask selectMask;

    [SerializeField] private float panSpeed = 1f;
    [SerializeField] private float zoomSpeed = 1f;

    private Camera mainCamera;

    private void Start()
    {
        mainCamera = Camera.main;
    }

    void Update()
    {
        if (Input.touchCount == 1)
        {
            Touch touch = Input.GetTouch(0);

            if (touch.phase == TouchPhase.Began || touch.phase == TouchPhase.Moved)
            {
                Physics.Raycast(mainCamera.ScreenPointToRay(touch.position), out RaycastHit hit, 1000, selectMask);

                transform.position = hit.point;

                willSelect = true;
            }
            else if (touch.phase == TouchPhase.Ended)
            {
                PositionField positions = new PositionField(transform.position, selected.Count, 1.7f);
                while (selected.Count > 0)
                {
                    Unit unit = selected.Pop();

                    unit.MoveTo(positions.AllocatePosition(unit.agent));
                    unit.Deselect();
                }

                willSelect = false;
                transform.position = new Vector3(0, -10, 0);
            }
        }

        else if (Input.touchCount >= 2)
        {
            willSelect = false;
            transform.position = new Vector3(0, -10, 0);

            Touch[] touches = { Input.GetTouch(0), Input.GetTouch(1) };

            if (touches[0].phase == TouchPhase.Began || touches[1].phase == TouchPhase.Began)
            {
                CalculateTouchVariables(touches[0].position, touches[1].position, out lastTouchDistance, out lastTouchAveragePosition);
            }

            else if (touches[0].phase == TouchPhase.Moved || touches[1].phase == TouchPhase.Moved)
            {
                CalculateTouchVariables(touches[0].position, touches[1].position, out float touchDistance, out Vector2 touchAveragePosition);

                Transform cameraTransform = mainCamera.transform;

                Vector2 deltaAveragePosition = (lastTouchAveragePosition - touchAveragePosition);
                cameraTransform.Translate(Quaternion.Euler(0, cameraTransform.rotation.eulerAngles.y, 0) * new Vector3(deltaAveragePosition.x, 0, deltaAveragePosition.y) * panSpeed, Space.World);  // Pan
                cameraTransform.Translate(new Vector3(0, 0, (lastTouchDistance - touchDistance) * -zoomSpeed), Space.Self);  // Zoom

                cameraTransform.position = new Vector3(cameraTransform.position.x, Mathf.Clamp(cameraTransform.position.y, 5, 15), cameraTransform.position.z);

                CalculateTouchVariables(touches[0].position, touches[1].position, out lastTouchDistance, out lastTouchAveragePosition);
            }
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        Unit otherUnit = other.GetComponent<Unit>();
        if (otherUnit && willSelect && otherUnit.Select())
        {
            selected.Push(otherUnit);
        }
    }

    private void CalculateTouchVariables(Vector2 position1, Vector2 position2, out float distance, out Vector2 averagePosition)
    {
        distance = Vector2.Distance(position1, position2);
        averagePosition = (position1 + position2) / 2;
    }
}
