import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';

const ProjectsScreen = () => {
    const projects = [
        { id: '1', name: 'Project Alpha' },
        { id: '2', name: 'Project Beta' },
        { id: '3', name: 'Project Gamma' },
    ];

    const renderItem = ({ item }) => (
        <View style={styles.projectItem}>
            <Text style={styles.projectName}>{item.name}</Text>
        </View>
    );

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Projects</Text>
            <FlatList
                data={projects}
                renderItem={renderItem}
                keyExtractor={item => item.id}
            />
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 16,
    },
    projectItem: {
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
    },
    projectName: {
        fontSize: 18,
    },
});

export default ProjectsScreen;