import { Request, Response } from 'express';
import ProjectService from '../services/project.service';

class ProjectController {
    private projectService: ProjectService;

    constructor() {
        this.projectService = new ProjectService();
    }

    public async createProject(req: Request, res: Response): Promise<Response> {
        try {
            const projectData = req.body;
            const newProject = await this.projectService.createProject(projectData);
            return res.status(201).json(newProject);
        } catch (error) {
            return res.status(500).json({ message: 'Error creating project', error });
        }
    }

    public async getProject(req: Request, res: Response): Promise<Response> {
        try {
            const projectId = req.params.id;
            const project = await this.projectService.getProjectById(projectId);
            if (!project) {
                return res.status(404).json({ message: 'Project not found' });
            }
            return res.status(200).json(project);
        } catch (error) {
            return res.status(500).json({ message: 'Error retrieving project', error });
        }
    }

    public async updateProject(req: Request, res: Response): Promise<Response> {
        try {
            const projectId = req.params.id;
            const projectData = req.body;
            const updatedProject = await this.projectService.updateProject(projectId, projectData);
            if (!updatedProject) {
                return res.status(404).json({ message: 'Project not found' });
            }
            return res.status(200).json(updatedProject);
        } catch (error) {
            return res.status(500).json({ message: 'Error updating project', error });
        }
    }

    public async deleteProject(req: Request, res: Response): Promise<Response> {
        try {
            const projectId = req.params.id;
            const deleted = await this.projectService.deleteProject(projectId);
            if (!deleted) {
                return res.status(404).json({ message: 'Project not found' });
            }
            return res.status(204).send();
        } catch (error) {
            return res.status(500).json({ message: 'Error deleting project', error });
        }
    }
}

export default new ProjectController();