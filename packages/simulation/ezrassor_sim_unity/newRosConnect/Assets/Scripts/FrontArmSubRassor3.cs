using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using frontArm = RosMessageTypes.RosMessages.StdMessageMsg;

public class FrontArmSubRassor3 : MonoBehaviour
{
    float armMsg;

    void Start()
    {
        // create subscriber instance
        ROSConnection.instance.Subscribe<frontArm>("/ezrassor3/front_arm_instructions", armMove);
    }

    void armMove(frontArm msg)
    {
        // grab value from msg
        armMsg = msg.data;
        HingeJoint hinge = GetComponent<HingeJoint>();
        JointMotor motor = hinge.motor;

        if(armMsg == 1f) // idle
        {
            motor.targetVelocity = 15;
            hinge.motor = motor;
        }
        if(armMsg == -1f) // digging
        { 
            motor.targetVelocity = -15;
            hinge.motor = motor;
        }
    }

}