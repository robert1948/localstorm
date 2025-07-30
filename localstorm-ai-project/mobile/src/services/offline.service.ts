import AsyncStorage from '@react-native-async-storage/async-storage';

class OfflineService {
    async saveData(key, value) {
        try {
            const jsonValue = JSON.stringify(value);
            await AsyncStorage.setItem(key, jsonValue);
        } catch (e) {
            console.error('Error saving data', e);
        }
    }

    async getData(key) {
        try {
            const jsonValue = await AsyncStorage.getItem(key);
            return jsonValue != null ? JSON.parse(jsonValue) : null;
        } catch (e) {
            console.error('Error retrieving data', e);
        }
    }

    async removeData(key) {
        try {
            await AsyncStorage.removeItem(key);
        } catch (e) {
            console.error('Error removing data', e);
        }
    }

    async clearStorage() {
        try {
            await AsyncStorage.clear();
        } catch (e) {
            console.error('Error clearing storage', e);
        }
    }
}

export default new OfflineService();