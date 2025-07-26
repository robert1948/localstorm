import { PreferenceModel } from '../models/preference.model';

export class PreferenceService {
    private preferences: PreferenceModel[];

    constructor() {
        this.preferences = [];
    }

    public async getUserPreferences(userId: string): Promise<PreferenceModel | null> {
        const userPreferences = this.preferences.find(pref => pref.userId === userId);
        return userPreferences || null;
    }

    public async updateUserPreferences(userId: string, newPreferences: Partial<PreferenceModel>): Promise<PreferenceModel | null> {
        const userPreferences = this.preferences.find(pref => pref.userId === userId);
        if (userPreferences) {
            Object.assign(userPreferences, newPreferences);
            return userPreferences;
        }
        return null;
    }

    public async createUserPreferences(userId: string, preferences: PreferenceModel): Promise<PreferenceModel> {
        const newPreference = { ...preferences, userId };
        this.preferences.push(newPreference);
        return newPreference;
    }

    public async deleteUserPreferences(userId: string): Promise<boolean> {
        const index = this.preferences.findIndex(pref => pref.userId === userId);
        if (index !== -1) {
            this.preferences.splice(index, 1);
            return true;
        }
        return false;
    }
}