# LocalStorm AI Project

## Overview
The LocalStorm AI Project is a comprehensive application designed to integrate advanced AI features, user management, and real-time analytics. This project consists of a backend service, a frontend web application, and a mobile application, all working together to provide a seamless user experience.

## Project Structure
The project is organized into several key directories:

- **backend**: Contains the server-side code, including API routes, controllers, services, and models.
- **frontend**: Contains the web application code, including components, pages, and services.
- **mobile**: Contains the mobile application code, designed for both iOS and Android platforms.
- **shared**: Contains shared types and utility functions used across the backend, frontend, and mobile applications.
- **docs**: Contains documentation for API, deployment, and development processes.
- **scripts**: Contains shell scripts for setting up, deploying, and testing the project.

## Features
- **AI Integration**: Supports multiple AI models and provides functionalities for AI interactions.
- **User Management**: Allows users to register, log in, and manage their profiles.
- **Real-time Analytics**: Provides insights into user engagement and application performance.
- **Voice Features**: Integrates voice recognition and synthesis capabilities.
- **Mobile Compatibility**: Offers a mobile application with a responsive design and offline capabilities.

## Getting Started
To get started with the project, follow these steps:

1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd localstorm-ai-project
   ```

2. **Set Up Environment Variables**:
   Copy the `.env.example` file to `.env` and configure your environment variables.

3. **Install Dependencies**:
   For the backend:
   ```
   cd backend
   npm install
   ```

   For the frontend:
   ```
   cd frontend
   npm install
   ```

   For the mobile app:
   ```
   cd mobile
   npm install
   ```

4. **Run the Application**:
   You can run the entire application stack using Docker:
   ```
   docker-compose up
   ```

   Alternatively, you can run each part separately:
   - Backend: `npm start` in the backend directory.
   - Frontend: `npm start` in the frontend directory.
   - Mobile: Use the appropriate command for your mobile development environment.

## Testing
The project includes unit, integration, security, and performance tests. To run the tests, use the following command in the backend directory:
```
npm test
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.