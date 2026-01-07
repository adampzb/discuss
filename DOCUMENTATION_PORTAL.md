# DiscussIt Documentation Portal

**Welcome to the DiscussIt Documentation Portal!**

This portal serves as the central hub for all technical documentation, guidelines, and resources for the DiscussIt platform development.

## 📚 Table of Contents

### 1. [Getting Started](#getting-started)
### 2. [Development Setup](#development-setup)
### 3. [API Documentation](#api-documentation)
### 4. [UI/UX Guidelines](#uiux-guidelines)
### 5. [Architecture](#architecture)
### 6. [Team Resources](#team-resources)
### 7. [Contributing](#contributing)
### 8. [FAQ](#faq)

## Getting Started

### Project Overview
- [Project Vision & Goals](PROJECT_REQUIREMENTS.md)
- [Detailed Roadmap](DETAILED_ROADMAP.md)
- [Technical Stack](PROJECT_REQUIREMENTS.md#technical-stack)

### Quick Start Guide
1. **Clone the repository:**
   ```bash
   git clone https://github.com/adampzb/discuss.git
   cd discuss
   ```

2. **Set up Docker environment:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Development Workflow
- [Git Workflow](CONTRIBUTING.md#git-workflow)
- [Code Review Process](CONTRIBUTING.md#code-review-process)
- [Branch Naming Convention](CONTRIBUTING.md#branch-naming)
- [Commit Message Guidelines](CONTRIBUTING.md#commit-messages)

## Development Setup

### Docker Development
- [Docker Setup Guide](DOCKER_README.md)
- [Docker Compose Configuration](docker-compose.yml)
- [Backend Dockerfile](backend/Dockerfile)
- [Frontend Dockerfile](frontend/Dockerfile)

### Local Development (without Docker)

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Environment Configuration
- [Backend Settings](backend/backend/settings.py)
- [Environment Variables](.env.example)
- [CORS Configuration](backend/backend/settings.py#L200)

## API Documentation

### API Specification
- [Complete API Specification](API_SPECIFICATION.md)
- [Authentication Endpoints](API_SPECIFICATION.md#authentication)
- [User Management](API_SPECIFICATION.md#user-management)
- [Profile Management](API_SPECIFICATION.md#profile-management)
- [Admin Management](API_SPECIFICATION.md#admin-management)

### API Reference

#### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/<uidb64>/<token>/` - Confirm password reset
- `POST /api/auth/logout/` - User logout

#### User Management
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `GET /api/auth/profiles/profile/` - Get extended profile
- `PUT /api/auth/profiles/profile/` - Update extended profile

#### Social Features
- `POST /api/auth/profiles/follow/` - Follow/unfollow user
- `POST /api/auth/profiles/block/` - Block/unblock user
- `GET /api/auth/profiles/search/` - Search users

#### Admin Features
- `GET /api/auth/management/users/` - List users
- `GET /api/auth/management/users/<id>/` - Get user details
- `PUT /api/auth/management/users/<id>/` - Update user
- `POST /api/auth/management/users/<id>/activate/` - Activate/deactivate user
- `DELETE /api/auth/management/users/<id>/` - Delete user
- `GET /api/auth/management/users/stats/` - User statistics
- `GET /api/auth/management/users/export/` - Export user data

### API Testing
- [Postman Collection](#) (Coming soon)
- [API Test Suite](backend/users/tests.py)
- [Testing Guidelines](CONTRIBUTING.md#testing)

## UI/UX Guidelines

### Design System
- [Complete UI/UX Guidelines](UI_UX_GUIDELINES.md)
- [Color Palette](UI_UX_GUIDELINES.md#color-palette)
- [Typography](UI_UX_GUIDELINES.md#typography)
- [Component Library](UI_UX_GUIDELINES.md#components)

### Page Templates
- [Authentication Pages](UI_UX_GUIDELINES.md#authentication-pages)
- [User Profile Pages](UI_UX_GUIDELINES.md#user-profile-pages)
- [Navigation Patterns](UI_UX_GUIDELINES.md#navigation)
- [Form Design](UI_UX_GUIDELINES.md#forms--inputs)

### Design Resources
- [Figma Design System](#) (Coming soon)
- [UI Kit Download](#) (Coming soon)
- [Icon Library](UI_UX_GUIDELINES.md#resources)

## Architecture

### System Architecture
```
┌───────────────────────────────────────────────────────────────┐
│                        DiscussIt Platform                      │
├─────────────────┬─────────────────┬─────────────────┬───────────┤
│   Frontend      │    Backend      │    Database     │   Cache   │
│  (React.js)     │   (Django)      │  (PostgreSQL)   │  (Redis)  │
├─────────────────┼─────────────────┼─────────────────┼───────────┤
│ - UI Components │ - REST API      │ - User Data     │ - Sessions│
│ - State Mgmt    │ - Authentication│ - Posts         │ - Caching │
│ - Routing       │ - Business Logic│ - Comments      │ - Rate Lim│
│ - Styling       │ - WebSockets    │ - Media         │ - Pub/Sub │
└─────────────────┴─────────────────┴─────────────────┴───────────┘
```

### Backend Architecture
- **Authentication**: JWT-based with Django REST Framework
- **User Management**: Custom User model with extended profiles
- **API Design**: RESTful with proper versioning
- **Real-time**: Django Channels for WebSocket support
- **Async Tasks**: Celery for background processing
- **Caching**: Redis for performance optimization

### Frontend Architecture
- **Framework**: React.js with functional components
- **State Management**: Redux Toolkit
- **Routing**: React Router
- **Styling**: CSS Modules / Styled Components
- **Forms**: React Hook Form
- **Internationalization**: react-i18next
- **Testing**: Jest + React Testing Library

### Database Schema
- [User Model](backend/users/models.py)
- [User Profile Model](backend/users/profile_models.py)
- [Database Migrations](backend/users/migrations/)

## Team Resources

### Development Guidelines
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CONTRIBUTING.md#code-of-conduct)
- [Code Style Guide](CONTRIBUTING.md#code-style)
- [Git Workflow](CONTRIBUTING.md#git-workflow)

### Team Structure
- **Product Manager**: Overall vision and roadmap
- **Backend Lead**: Django API and infrastructure
- **Frontend Lead**: React implementation
- **Full-stack Developers**: Cross-platform features
- **DevOps Engineer**: Deployment and scaling
- **QA Engineer**: Testing and quality assurance
- **UX Designer**: User experience and interface

### Communication
- **Slack Channels**:
  - `#general` - Team announcements
  - `#backend` - Backend development
  - `#frontend` - Frontend development
  - `#ux-design` - UI/UX discussions
  - `#support` - User support
  - `#random` - Off-topic conversations

- **Meetings**:
  - **Daily Standup**: 10:00 AM (15 minutes)
  - **Sprint Planning**: Monday 2:00 PM (60 minutes)
  - **Retrospective**: Friday 3:00 PM (30 minutes)
  - **Tech Review**: Wednesday 1:00 PM (60 minutes)

### Tools & Services
- **Version Control**: GitHub
- **Project Management**: Jira
- **Design**: Figma
- **Documentation**: GitHub Wiki, Notion
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry, Prometheus
- **Hosting**: Scaleway Cloud

## Contributing

### How to Contribute
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**
4. **Write tests** for your changes
5. **Update documentation** if needed
6. **Run tests**: `docker-compose exec backend python manage.py test`
7. **Commit your changes**: `git commit -m "Add your feature"`
8. **Push to your branch**: `git push origin feature/your-feature`
9. **Create a Pull Request**

### Pull Request Guidelines
- Reference the related issue (e.g., `Fixes #123`)
- Provide a clear description of changes
- Include screenshots for UI changes
- Ensure all tests pass
- Request review from appropriate team members
- Address all review comments

### Code Review Process
1. **Initial Review**: Assigned to relevant team member
2. **Automated Checks**: CI pipeline runs tests and linting
3. **Manual Review**: Code quality, architecture, and functionality
4. **Approvals**: Requires at least 2 approvals for major changes
5. **Merge**: After approvals and successful CI checks

## FAQ

### General Questions

**Q: What is DiscussIt?**
A: DiscussIt is a modern social media platform combining forum discussions and microblogging features with a focus on user privacy and community building.

**Q: What technologies does DiscussIt use?**
A: Backend: Django, PostgreSQL, Redis. Frontend: React.js, Redux. Infrastructure: Docker, Nginx, Celery.

**Q: How can I contribute to DiscussIt?**
A: Check out our [Contributing Guide](CONTRIBUTING.md) for detailed instructions on how to contribute.

### Development Questions

**Q: How do I set up the development environment?**
A: Follow our [Docker Setup Guide](DOCKER_README.md) for the easiest way to get started.

**Q: Where can I find the API documentation?**
A: The complete API specification is available in [API_SPECIFICATION.md](API_SPECIFICATION.md).

**Q: What are the coding standards?**
A: We follow PEP 8 for Python and standard JavaScript/React best practices. See our [UI/UX Guidelines](UI_UX_GUIDELINES.md#code-standards) for more details.

**Q: How do I run tests?**
A: Use the Docker setup: `docker-compose exec backend python manage.py test`

### Troubleshooting

**Q: I'm getting database connection errors**
A: Make sure your Docker containers are running: `docker-compose ps`. If the database container isn't healthy, try `docker-compose restart db`.

**Q: My changes aren't reflecting in the browser**
A: If using Docker, make sure you're not seeing cached content. Try a hard refresh (Ctrl+Shift+R) or clear your browser cache.

**Q: How do I debug backend issues?**
A: Access the backend container: `docker-compose exec backend sh`, then use Django's debug tools or check logs with `docker-compose logs backend`.

**Q: Where can I ask for help?**
A: Ask in the appropriate Slack channel or create an issue in GitHub with the `help-wanted` label.

## Documentation Index

### Core Documentation
- [📋 Project Requirements](PROJECT_REQUIREMENTS.md)
- [🗺️ Detailed Roadmap](DETAILED_ROADMAP.md)
- [🤝 Contributing Guide](CONTRIBUTING.md)
- [🐳 Docker Setup](DOCKER_README.md)

### Technical Documentation
- [🔌 API Specification](API_SPECIFICATION.md)
- [🎨 UI/UX Guidelines](UI_UX_GUIDELINES.md)
- [📁 Backend Structure](backend/README.md) (Coming soon)
- [🖥️ Frontend Structure](frontend/README.md) (Coming soon)

### Development Resources
- [📦 Backend Dependencies](backend/requirements.txt)
- [📦 Frontend Dependencies](frontend/package.json)
- [🔧 Backend Settings](backend/backend/settings.py)
- [🧪 Test Suite](backend/users/tests.py)

## Version History

### Documentation Portal
- **v1.0** (Current): Initial documentation portal structure
- **v1.1** (Planned): Interactive documentation with search
- **v1.2** (Planned): API playground and testing tools

### Project Versions
- **Backend**: Django 5.2.9
- **Frontend**: React 18.x
- **API**: v1.0

## Support

### Getting Help
1. **Check the FAQ** above
2. **Search existing issues** in GitHub
3. **Ask in Slack** in the appropriate channel
4. **Create a new issue** in GitHub
5. **Contact the team** via email: support@discussit.eu

### Reporting Issues
When reporting issues, please include:
- Detailed description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment information (OS, browser, versions)
- Logs or error messages

### Feature Requests
For feature requests:
- Describe the feature and its benefits
- Provide use cases and examples
- Explain how it fits with the project vision
- Include mockups or designs if available

## License

The DiscussIt project and documentation are licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## Roadmap

### Documentation Portal Roadmap

#### Phase 1: Basic Documentation (✅ Completed)
- [x] Create core documentation files
- [x] Set up API specification
- [x] Establish UI/UX guidelines
- [x] Create contributing guide
- [x] Set up Docker documentation

#### Phase 2: Interactive Documentation (🚧 In Progress)
- [ ] Set up documentation portal structure
- [ ] Create navigation and index
- [ ] Add search functionality
- [ ] Implement versioning
- [ ] Add interactive examples

#### Phase 3: Advanced Features (📅 Planned)
- [ ] API playground with live testing
- [ ] Interactive component library
- [ ] Design system showcase
- [ ] Automated documentation generation
- [ ] User feedback and analytics

#### Phase 4: Integration (🎯 Future)
- [ ] Integrate with main application
- [ ] Add in-app documentation viewer
- [ ] Contextual help system
- [ ] Onboarding tutorials
- [ ] Interactive guides

## Contributors

### Documentation Team
- **Lead**: [Your Name] - Overall documentation architecture
- **API Docs**: [Your Name] - API specification and reference
- **UI/UX Docs**: [Your Name] - Design system and guidelines
- **Dev Docs**: [Your Name] - Development setup and guides

### How to Contribute to Documentation
1. **Identify gaps** in existing documentation
2. **Create an issue** for documentation improvements
3. **Fork the repository** and make changes
4. **Follow documentation standards**
5. **Submit a Pull Request**

## Feedback

We welcome feedback on our documentation! Please:
- **Create issues** for documentation improvements
- **Suggest new topics** that should be covered
- **Report errors** or outdated information
- **Provide examples** that would be helpful

## Changelog

### Documentation Portal

**v1.0.0** (2024-02-20)
- Initial documentation portal structure
- Comprehensive API specification
- Detailed UI/UX guidelines
- Docker setup documentation
- Contributing guide
- FAQ and support sections

**v0.1.0** (2024-02-15)
- Basic documentation structure
- Initial API endpoints documentation
- Development setup guide
- Contributing guidelines

## Related Resources

### External Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [React Documentation](https://react.dev/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/docs/)

### Learning Resources
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS Tricks](https://css-tricks.com/)
- [Google Web Fundamentals](https://developers.google.com/web/fundamentals)
- [Web Accessibility Initiative](https://www.w3.org/WAI/)

## Contact

For documentation-related questions:
- **Email**: docs@discussit.eu
- **Slack**: #documentation channel
- **GitHub Issues**: https://github.com/adampzb/discuss/issues

## Status

This documentation portal is actively maintained and updated as the project evolves. Last updated: 2024-02-20

**Current Status**: 🚧 Under active development

**Next Update**: Adding interactive API playground and search functionality

---

*This documentation portal is generated and maintained by the DiscussIt team. Contributions are welcome!*