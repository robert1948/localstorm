export class Project {
    constructor(
        public phase: string,
        public taskId: string,
        public taskName: string,
        public priority: string,
        public status: string,
        public assignee: string,
        public estimatedHours: number,
        public startDate: Date,
        public dueDate: Date,
        public progress: number,
        public dependencies: string,
        public category: string,
        public successMetrics: string
    ) {}
}