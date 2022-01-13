//Do not edit! This file was generated by Unity-ROS MessageGeneration.
using System;
using System.Linq;
using System.Collections.Generic;
using System.Text;
using Unity.Robotics.ROSTCPConnector.MessageGeneration;

namespace RosMessageTypes.RosMessages
{
    [Serializable]
    public class GeometryMessageMsg : Message
    {
        public const string k_RosMessageName = "RosMessages/GeometryMessage";
        public override string RosMessageName => k_RosMessageName;

        public Vector3Msg linear;
        public Vector3Msg angular;

        public GeometryMessageMsg()
        {
            this.linear = new Vector3Msg();
            this.angular = new Vector3Msg();
        }

        public GeometryMessageMsg(Vector3Msg linear, Vector3Msg angular)
        {
            this.linear = linear;
            this.angular = angular;
        }

        public static GeometryMessageMsg Deserialize(MessageDeserializer deserializer) => new GeometryMessageMsg(deserializer);

        private GeometryMessageMsg(MessageDeserializer deserializer)
        {
            this.linear = Vector3Msg.Deserialize(deserializer);
            this.angular = Vector3Msg.Deserialize(deserializer);
        }

        public override void SerializeTo(MessageSerializer serializer)
        {
            serializer.Write(this.linear);
            serializer.Write(this.angular);
        }

        public override string ToString()
        {
            return "GeometryMessageMsg: " +
            "\nlinear: " + linear.ToString() +
            "\nangular: " + angular.ToString();
        }

#if UNITY_EDITOR
        [UnityEditor.InitializeOnLoadMethod]
#else
        [UnityEngine.RuntimeInitializeOnLoadMethod]
#endif
        public static void Register()
        {
            MessageRegistry.Register(k_RosMessageName, Deserialize);
        }
    }
}