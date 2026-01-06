# DiscussIt - European Social Media Platform

## Project Structure

```
discussit/
├── backend/              # Django backend
│   ├── backend/          # Main Django project
│   ├── users/            # User authentication and profiles
│   ├── forums/           # Forum system (Reddit-like)
│   ├── microblogging/    # Microblogging system (Twitter-like)
│   └── shared/           # Shared components and utilities
│
├── frontend/            # React frontend
│   ├── src/             # React source code
│   ├── public/          # Public assets
│   └── ...
│
├── DETAILED_ROADMAP.md  # Comprehensive development roadmap
├── PROJECT_REQUIREMENTS.md # Professional requirements document
└── README.md            # This file
```

## Getting Started

### Backend Setup

1. **Install dependencies:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run migrations:**
```bash
python manage.py migrate
```

4. **Start development server:**
```bash
python manage.py runserver
```

### Frontend Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm start
```

## Development Roadmap

The project follows an 8-phase development plan:

1. **Phase 0: Project Setup** (2 weeks) ✅
2. **Phase 1: Core Authentication** (4 weeks)
3. **Phase 2: Forum System** (6 weeks)
4. **Phase 3: Microblogging** (5 weeks)
5. **Phase 4: Shared Features** (4 weeks)
6. **Phase 5: Beta Testing** (4 weeks)
7. **Phase 6: Launch Prep** (3 weeks)
8. **Phase 7: MVP Launch** (4 weeks)

See `DETAILED_ROADMAP.md` for complete timeline and specifications.

## Technology Stack

### Backend
- **Framework:** Django 6.0
- **API:** Django REST Framework
- **Authentication:** Django Allauth + JWT
- **Database:** PostgreSQL
- **Real-time:** Django Channels + Redis
- **Async Tasks:** Celery + Redis
- **Caching:** Redis

### Frontend
- **Framework:** React 18
- **State Management:** Redux Toolkit
- **Routing:** React Router 6
- **Styling:** Tailwind CSS
- **Forms:** React Hook Form
- **Real-time:** Socket.IO

## Key Features

### Forum System (Reddit-like)
- User-created subforums
- Text, image, video posts
- Nested comment system
- Upvote/downvote functionality
- Comprehensive moderation tools

### Microblogging System (Twitter-like)
- 280-character posts
- Real-time feed updates
- Follow system
- Hashtag discovery
- Algorithmic and chronological feeds

### Shared Features
- Unified authentication
- Cross-platform notifications
- Advanced search
- User profiles
- Accessibility compliance

## Contributing

Please follow the development roadmap and coding standards outlined in the project documentation.

## License

[License information to be determined]

## Contact

[Project contact information to be added]