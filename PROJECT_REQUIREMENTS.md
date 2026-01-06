# DiscussIt - Project Requirements Document
*Last Updated: 2024-02-20*

---

## 1. Project Overview
**Name:** DiscussIt
**Type:** Unified Web App (Reddit-like forums + Twitter-like microblogging)
**Domain:** `discussit.eu`
**Deployment:** Scaleway Cloud

### Key Concept:
- **Single platform** with two core sections:
  1. **Forums:** `discussit.eu/Discuss/[subforum]` (e.g., `Discuss/technology`)
  2. **Microblogging:** `discussit.eu/profiles`
- **One account** for both sections.
- **Shared features:** Voting, replies, followers, hashtags.

---

## 2. Core Features

### A. Forum (Reddit-like)
| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| **Subforums**         | User-created communities (e.g., `Discuss/technology`).                      |
| **Privacy**           | Public (visible to all) or Private (invite-only).                           |
| **Posts**             | Text, links, images, videos.                                                |
| **Voting**            | Upvote/downvote posts and comments.                                         |
| **Comments**          | Nested replies (like Reddit).                                               |
| **Moderation**        | Rules, bans, post removal.                                                 |
| **Hashtags**          | Optional for posts (e.g., `#tech`).                                         |

### B. Microblogging (Twitter-like)
| Feature               | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| **Posts**             | Short text updates (**280-character limit**).                                |
| **Voting**            | Upvote/downvote (reusing forum logic).                                      |
| **Replies**           | Nested comments (same as forum).                                            |
| **Followers**         | Users can follow others (like Twitter).                                     |
| **Hashtags**          | Required for discoverability (e.g., `#news`).                                |
| **Feed**              | Algorithmic timeline (curated by engagement).                               |

### C. Shared Backend Logic
- **Voting System:** Unified upvote/downvote for forums and microblogging.
- **Comments/Replies:** Nested threading reused across both sections.
- **User Profiles:** Single profile page showing activity from both sections.
- **Authentication:** One login for all features.

---

## 3. Technical Stack

| Component       | Tech Stack                     |
|-----------------|---------------------------------|
| **Backend**     | Django + Django REST Framework  |
| **Frontend**    | React.js (SPA)                 |
| **Database**    | PostgreSQL                      |
| **Auth**        | Django Allauth + JWT            |
| **Styling**     | Tailwind CSS                    |
| **Deployment**  | Scaleway Cloud                  |

---

## 4. Development Roadmap

### Phase 1: Core Features (MVP)
- [ ] User authentication (signup, login, profiles).
- [ ] Forum (`Discuss/[subforum]`, public/private, posts, voting, comments).
- [ ] Microblogging (`/profiles`, posts, followers, algorithmic feed).
- [ ] Shared backend logic (voting, replies).

### Phase 2: Voice Chat (Future)
- [ ] Subforum-specific voice rooms (WebRTC or third-party API).
- [ ] Real-time moderation tools.

---

## 5. Open Questions (To Be Resolved)
1. **Voice Chat Tech:** WebRTC (self-hosted) or third-party (Agora/Twilio)?
2. **Monetization:** Ads, premium subforums, or tipping?
3. **Mobile App:** Future React Native adaptation?

---

## 6. Approval
**Status:** Approved ✅
**Next Steps:**
1. Set up Django backend (models, APIs).
2. Set up React frontend (routing, UI).
3. Deploy to Scaleway Cloud.