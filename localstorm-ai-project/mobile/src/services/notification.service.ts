import { Notifications } from 'react-native';

class NotificationService {
    static async requestPermission() {
        const { status } = await Notifications.requestPermissionsAsync();
        return status === 'granted';
    }

    static async scheduleNotification(title, body, data) {
        await Notifications.scheduleNotificationAsync({
            content: {
                title: title,
                body: body,
                data: data,
            },
            trigger: {
                seconds: 1,
            },
        });
    }

    static async cancelAllNotifications() {
        await Notifications.cancelAllScheduledNotificationsAsync();
    }
}

export default NotificationService;