import { Schema, model } from 'mongoose';

const conversationSchema = new Schema({
    userId: {
        type: String,
        required: true,
    },
    messages: [
        {
            sender: {
                type: String,
                required: true,
            },
            content: {
                type: String,
                required: true,
            },
            timestamp: {
                type: Date,
                default: Date.now,
            },
        },
    ],
    createdAt: {
        type: Date,
        default: Date.now,
    },
    updatedAt: {
        type: Date,
        default: Date.now,
    },
});

const Conversation = model('Conversation', conversationSchema);

export default Conversation;