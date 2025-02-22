class MessageCommand {
  constructor(senderId, receiverId, content) {
    this.messageId = `msg_${Date.now()}`; // Identificador único del mensaje
    this.senderId = senderId;
    this.receiverId = receiverId;
    this.content = content;
    this.timestamp = new Date().toISOString();
    this.type = 'NEW_MESSAGE_NOTIFICATION';
  }

  toJSON() {
    return {
      messageId: this.messageId,
      senderId: this.senderId,
      receiverId: this.receiverId,
      content: this.content,
      timestamp: this.timestamp,
      type: this.type
    };
  }
}

module.exports = MessageCommand;