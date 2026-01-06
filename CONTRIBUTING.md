# Contributing to DiscussIt

Welcome to DiscussIt! We're excited that you want to contribute to our European social media platform. This guide will help you get started with development and contribute effectively.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Project Structure](#project-structure)
- [Contact](#contact)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the expectations for all contributors.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

**Backend Requirements:**
- Python 3.12+
- PostgreSQL 15+
- Redis 7+
- pip (Python package manager)

**Frontend Requirements:**
- Node.js 18+
- npm 9+

**Recommended Tools:**
- Git
- Docker (optional, for containerized development)
- VS Code or similar IDE

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/adampzb/discuss.git
cd discuss
```

2. **Set up the backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up the frontend:**
```bash
cd ../frontend
npm install
```

4. **Configure environment variables:**
```bash
cd ../backend
cp .env.example .env
# Edit .env with your local configuration
```

## Development Workflow

### Branching Strategy

We use a feature branch workflow:

1. **Create a feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes** and commit them with descriptive messages:
```bash
git commit -m "Add user authentication feature"
```

3. **Push your branch:**
```bash
git push origin feature/your-feature-name
```

4. **Create a Pull Request** targeting the `master` branch

### Branch Naming Conventions

- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Critical production fixes
- `docs/*` - Documentation updates
- `refactor/*` - Code refactoring
- `test/*` - Testing improvements

### Commit Message Guidelines

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - A new feature
- `fix:` - A bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, missing semicolons, etc.)
- `refactor:` - Code refactoring (no functional changes)
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `chore:` - Build process or auxiliary tool changes

Example:
```
feat(auth): implement JWT token authentication
fix(forums): resolve nested comment display issue
```

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use type hints where appropriate
- Write docstrings for all public modules, classes, and functions
- Keep lines under 120 characters
- Use snake_case for variable and function names
- Use CamelCase for class names

### JavaScript/React (Frontend)

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Follow React naming conventions (PascalCase for components)
- Use Redux Toolkit for state management
- Write PropTypes for all component props
- Keep components small and focused

### General Practices

- Write clean, readable, and maintainable code
- Add comments for complex logic
- Keep functions small and single-purpose
- Write unit tests for all new functionality
- Follow the existing code style in the project
- Document your code appropriately

## Testing

### Backend Testing

Run Django tests:
```bash
cd backend
python manage.py test
```

Run specific app tests:
```bash
python manage.py test users
python manage.py test forums
```

### Frontend Testing

Run React tests:
```bash
cd frontend
npm test
```

### Test Coverage

We aim for 90%+ test coverage. Run coverage analysis:
```bash
# Backend
cd backend
pip install coverage
coverage run manage.py test
coverage report

# Frontend
cd frontend
npm test -- --coverage
```

## Pull Request Process

1. **Ensure your code follows our coding standards**
2. **Write tests** for your changes
3. **Update documentation** if needed
4. **Run all tests locally** to ensure nothing breaks
5. **Create a descriptive Pull Request** with:
   - Clear title and description
   - Reference to related issues (if any)
   - Screenshots for UI changes
   - Testing instructions
6. **Request reviews** from at least 2 team members
7. **Address feedback** and make necessary changes
8. **Merge** once approved

## Issue Reporting

When reporting issues, please include:

- **Description** of the problem
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, browser, versions)
- **Log files** (if applicable)

## Project Structure

```
discussit/
├── backend/              # Django backend
│   ├── backend/          # Main Django project
│   │   ├── settings.py   # Project settings
│   │   ├── urls.py       # Main URL routing
│   │   ├── asgi.py       # ASGI configuration
│   │   └── wsgi.py       # WSGI configuration
│   ├── users/            # User authentication and profiles
│   ├── forums/           # Forum system (Reddit-like)
│   ├── microblogging/    # Microblogging system (Twitter-like)
│   └── shared/           # Shared components and utilities
│
├── frontend/            # React frontend
│   ├── src/             # React source code
│   │   ├── components/   # Reusable components
│   │   ├── pages/        # Page components
│   │   ├── store/        # Redux store
│   │   ├── api/          # API services
│   │   ├── utils/        # Utility functions
│   │   └── App.js        # Main app component
│   ├── public/          # Public assets
│   └── package.json     # Frontend dependencies
│
├── .gitignore           # Git ignore rules
├── README.md            # Project overview
├── CONTRIBUTING.md      # Contribution guidelines
├── LOCAL_TESTING.md     # Local testing instructions
├── DETAILED_ROADMAP.md  # Development roadmap
└── PROJECT_REQUIREMENTS.md # Requirements document
```

## Development Tips

### Backend Development

- Use Django's built-in development server:
```bash
cd backend
python manage.py runserver
```

- Create and apply migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

- Access Django admin at `/admin` (create superuser first)

### Frontend Development

- Start React development server:
```bash
cd frontend
npm start
```

- The frontend will be available at `http://localhost:3000`

### API Testing

- Use Postman or curl to test API endpoints
- API documentation will be available at `/api/docs/` (when implemented)

## Contact

For questions or support:

- **Slack:** [Team Slack Channel](#)
- **Email:** [team@discussit.eu](#)
- **Project Lead:** [Lead Name](#)

## License

By contributing to DiscussIt, you agree that your contributions will be licensed under the project's [LICENSE](LICENSE) file.

Thank you for contributing to DiscussIt! Together we can build a great European alternative to US social media platforms.