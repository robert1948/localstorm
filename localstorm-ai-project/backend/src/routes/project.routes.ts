import { Router } from 'express';
import { 
    createProject, 
    getProjectById, 
    updateProject, 
    deleteProject, 
    getAllProjects 
} from '../controllers/project.controller';

const router = Router();

// Route to create a new project
router.post('/', createProject);

// Route to get a project by ID
router.get('/:id', getProjectById);

// Route to update a project
router.put('/:id', updateProject);

// Route to delete a project
router.delete('/:id', deleteProject);

// Route to get all projects
router.get('/', getAllProjects);

export default router;