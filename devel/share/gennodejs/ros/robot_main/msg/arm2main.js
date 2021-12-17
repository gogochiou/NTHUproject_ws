// Auto-generated. Do not edit!

// (in-package robot_main.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class arm2main {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.action = null;
      this.situation = null;
    }
    else {
      if (initObj.hasOwnProperty('action')) {
        this.action = initObj.action
      }
      else {
        this.action = '';
      }
      if (initObj.hasOwnProperty('situation')) {
        this.situation = initObj.situation
      }
      else {
        this.situation = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type arm2main
    // Serialize message field [action]
    bufferOffset = _serializer.string(obj.action, buffer, bufferOffset);
    // Serialize message field [situation]
    bufferOffset = _serializer.string(obj.situation, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type arm2main
    let len;
    let data = new arm2main(null);
    // Deserialize message field [action]
    data.action = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [situation]
    data.situation = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += object.action.length;
    length += object.situation.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'robot_main/arm2main';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '34e8372aba9fdf90a3e4bf2cfa63f7e3';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    string action
    string situation
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new arm2main(null);
    if (msg.action !== undefined) {
      resolved.action = msg.action;
    }
    else {
      resolved.action = ''
    }

    if (msg.situation !== undefined) {
      resolved.situation = msg.situation;
    }
    else {
      resolved.situation = ''
    }

    return resolved;
    }
};

module.exports = arm2main;
