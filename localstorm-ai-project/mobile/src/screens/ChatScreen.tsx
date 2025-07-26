import React, { useEffect, useState } from 'react';
import { View, Text, TextInput, Button, FlatList, StyleSheet } from 'react-native';
import { fetchMessages, sendMessage } from '../services/api.service';

const ChatScreen = () => {
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');

    useEffect(() => {
        const loadMessages = async () => {
            const fetchedMessages = await fetchMessages();
            setMessages(fetchedMessages);
        };

        loadMessages();
    }, []);

    const handleSendMessage = async () => {
        if (inputMessage.trim()) {
            const newMessage = await sendMessage(inputMessage);
            setMessages(prevMessages => [...prevMessages, newMessage]);
            setInputMessage('');
        }
    };

    return (
        <View style={styles.container}>
            <FlatList
                data={messages}
                keyExtractor={(item) => item.id.toString()}
                renderItem={({ item }) => (
                    <View style={styles.messageContainer}>
                        <Text style={styles.messageText}>{item.text}</Text>
                    </View>
                )}
            />
            <TextInput
                style={styles.input}
                value={inputMessage}
                onChangeText={setInputMessage}
                placeholder="Type your message..."
            />
            <Button title="Send" onPress={handleSendMessage} />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
        backgroundColor: '#fff',
    },
    messageContainer: {
        marginVertical: 4,
        padding: 10,
        borderRadius: 5,
        backgroundColor: '#f1f1f1',
    },
    messageText: {
        fontSize: 16,
    },
    input: {
        height: 40,
        borderColor: 'gray',
        borderWidth: 1,
        borderRadius: 5,
        paddingHorizontal: 10,
        marginVertical: 10,
    },
});

export default ChatScreen;