export class Preference {
    constructor(
        public id: string,
        public userId: string,
        public preferences: Record<string, any>,
        public createdAt: Date,
        public updatedAt: Date
    ) {}
}

export const preferenceSchema = {
    id: { type: String, required: true },
    userId: { type: String, required: true },
    preferences: { type: Object, required: true },
    createdAt: { type: Date, default: Date.now },
    updatedAt: { type: Date, default: Date.now }
};