export interface Project {
    id: string;
    name: string;
    description: string;
    startDate: Date;
    endDate: Date;
    status: 'Not Started' | 'In Progress' | 'Completed';
    priority: 'Low' | 'Medium' | 'High' | 'Critical';
    assignee: string;
    progress: number; // percentage from 0 to 100
    createdAt: Date;
    updatedAt: Date;
}

export interface ProjectUpdate {
    name?: string;
    description?: string;
    startDate?: Date;
    endDate?: Date;
    status?: 'Not Started' | 'In Progress' | 'Completed';
    priority?: 'Low' | 'Medium' | 'High' | 'Critical';
    assignee?: string;
    progress?: number; // percentage from 0 to 100
}