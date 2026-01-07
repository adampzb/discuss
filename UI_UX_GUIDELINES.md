# DiscussIt UI/UX Guidelines

**Version:** 1.0
**Last Updated:** 2024
**Status:** Draft

## Table of Contents

1. [Design Principles](#design-principles)
2. [Color Palette](#color-palette)
3. [Typography](#typography)
4. [Spacing & Layout](#spacing--layout)
5. [Components](#components)
6. [Authentication Pages](#authentication-pages)
7. [User Profile Pages](#user-profile-pages)
8. [Navigation](#navigation)
9. [Forms & Inputs](#forms--inputs)
10. [Responsive Design](#responsive-design)
11. [Accessibility](#accessibility)
12. [Performance](#performance)
13. [Animation & Transitions](#animation--transitions)
14. [Error States](#error-states)
15. [Loading States](#loading-states)
16. [Empty States](#empty-states)
17. [Internationalization](#internationalization)
18. [Dark Mode](#dark-mode)
19. [Code Standards](#code-standards)
20. [Resources](#resources)

## Design Principles

### 1. Consistency
- Maintain consistent styling across all pages and components
- Use the same patterns for similar functionality
- Follow established design systems and component libraries

### 2. Simplicity
- Keep interfaces clean and uncluttered
- Prioritize content over decoration
- Use whitespace effectively
- Avoid unnecessary complexity

### 3. Accessibility
- Follow WCAG 2.1 AA standards
- Ensure keyboard navigation works everywhere
- Provide proper contrast ratios
- Use semantic HTML
- Include ARIA attributes where needed

### 4. Responsiveness
- Mobile-first approach
- Design for all screen sizes (320px to 4K+)
- Test on multiple devices and orientations
- Use relative units (rem, %, vh/vw) over fixed units (px)

### 5. Performance
- Optimize asset loading
- Use lazy loading for images and non-critical resources
- Minimize render-blocking resources
- Keep bundle sizes small

### 6. User-Centric
- Put user needs first
- Provide clear feedback for user actions
- Make common tasks easy to accomplish
- Provide helpful error messages

## Color Palette

### Primary Colors
```css
--primary: #4285F4;       /* Google Blue */
--primary-dark: #3367D6;   /* Darker blue */
--primary-light: #D7E5FD;  /* Lighter blue */
--primary-hover: #3367D6;  /* Hover state */
```

### Secondary Colors
```css
--secondary: #34A853;     /* Google Green */
--secondary-dark: #2D8F47;
--secondary-light: #D5E8D4;
```

### Neutral Colors
```css
--white: #FFFFFF;
--black: #000000;
--gray-50: #FAFAFA;
--gray-100: #F5F5F5;
--gray-200: #EEEEEE;
--gray-300: #E0E0E0;
--gray-400: #BDBDBD;
--gray-500: #9E9E9E;
--gray-600: #757575;
--gray-700: #616161;
--gray-800: #424242;
--gray-900: #212121;
```

### Semantic Colors
```css
--success: #4CAF50;
--warning: #FF9800;
--error: #F44336;
--info: #2196F3;
```

### Status Colors
```css
--online: #4CAF50;
--away: #FFC107;
--busy: #F44336;
--offline: #9E9E9E;
```

### Dark Mode Colors
```css
--dark-bg: #121212;
--dark-surface: #1E1E1E;
--dark-text: #E0E0E0;
--dark-secondary: #B0B0B0;
--dark-disabled: #424242;
```

## Typography

### Font Families
```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-secondary: 'Roboto Mono', monospace;
--font-fallback: system-ui, -apple-system, sans-serif;
```

### Font Weights
```css
--font-weight-light: 300;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Font Sizes (rem based)
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
--text-5xl: 3rem;      /* 48px */
--text-6xl: 3.75rem;   /* 60px */
```

### Line Heights
```css
--leading-none: 1;
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
--leading-loose: 2;
```

### Typography Scale

| Element | Font Size | Font Weight | Line Height |
|---------|-----------|-------------|-------------|
| Body | 1rem (16px) | 400 | 1.5 |
| Headings | 3rem-1.5rem | 600-700 | 1.2-1.3 |
| Buttons | 1rem | 500 | 1.5 |
| Labels | 0.875rem | 500 | 1.5 |
| Captions | 0.75rem | 400 | 1.6 |

## Spacing & Layout

### Spacing Scale (rem based)
```css
--space-none: 0;
--space-xs: 0.25rem;    /* 4px */
--space-sm: 0.5rem;     /* 8px */
--space-md: 1rem;       /* 16px */
--space-lg: 1.5rem;     /* 24px */
--space-xl: 2rem;       /* 32px */
--space-2xl: 3rem;      /* 48px */
--space-3xl: 4rem;      /* 64px */
--space-4xl: 6rem;      /* 96px */
```

### Container Widths
```css
--container-sm: 540px;
--container-md: 720px;
--container-lg: 960px;
--container-xl: 1140px;
--container-2xl: 1320px;
```

### Breakpoints
```css
--breakpoint-xs: 360px;
--breakpoint-sm: 576px;
--breakpoint-md: 768px;
--breakpoint-lg: 992px;
--breakpoint-xl: 1200px;
--breakpoint-2xl: 1440px;
```

### Grid System
- 12-column responsive grid
- 16px gutter width (1rem)
- Mobile-first approach

## Components

### Buttons

**Primary Button:**
```html
<button class="btn btn-primary">Button</button>
```

**Secondary Button:**
```html
<button class="btn btn-secondary">Button</button>
```

**Variants:**
- `btn-primary` - Main action
- `btn-secondary` - Secondary action
- `btn-success` - Success action
- `btn-warning` - Warning action
- `btn-danger` - Danger action
- `btn-outline` - Outline variant
- `btn-text` - Text-only variant
- `btn-icon` - Icon-only button

**Sizes:**
- `btn-sm` - Small
- `btn-md` - Medium (default)
- `btn-lg` - Large

### Cards

**Basic Card:**
```html
<div class="card">
  <div class="card-header">Header</div>
  <div class="card-body">Content</div>
  <div class="card-footer">Footer</div>
</div>
```

**Variants:**
- `card-default` - Default card
- `card-hover` - Hover effects
- `card-clickable` - Clickable card
- `card-shadow` - Shadow effect

### Forms

**Form Group:**
```html
<div class="form-group">
  <label for="email">Email</label>
  <input type="email" id="email" class="form-control">
  <span class="form-help">Help text</span>
  <span class="form-error">Error message</span>
</div>
```

**Input Variants:**
- `form-control` - Default input
- `form-control-sm` - Small input
- `form-control-lg` - Large input
- `form-control-invalid` - Invalid state
- `form-control-disabled` - Disabled state

### Navigation

**Main Navigation:**
```html
<nav class="navbar">
  <div class="navbar-brand">Logo</div>
  <div class="navbar-menu">
    <a href="#" class="navbar-item">Home</a>
    <a href="#" class="navbar-item">Forums</a>
    <a href="#" class="navbar-item">Microblog</a>
  </div>
  <div class="navbar-actions">
    <button class="btn btn-icon">🔔</button>
    <button class="btn btn-icon">👤</button>
  </div>
</nav>
```

### Modals

**Basic Modal:**
```html
<div class="modal">
  <div class="modal-overlay"></div>
  <div class="modal-content">
    <div class="modal-header">
      <h3>Modal Title</h3>
      <button class="modal-close">×</button>
    </div>
    <div class="modal-body">Content</div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancel</button>
      <button class="btn btn-primary">OK</button>
    </div>
  </div>
</div>
```

## Authentication Pages

### Login Page

**Layout:**
- Centered card (max-width: 400px)
- Logo at top
- Email and password fields
- Remember me checkbox
- Login button (primary)
- Forgot password link
- Sign up link

**Design Requirements:**
- Clean, minimal design
- Clear error messages
- Password visibility toggle
- Loading state for button
- Responsive for mobile devices

### Signup Page

**Layout:**
- Multi-step form (optional)
- Email, password, name fields
- Password strength meter
- Terms and conditions checkbox
- Signup button (primary)
- Login link

**Design Requirements:**
- Progress indicator for multi-step
- Real-time validation
- Password requirements checklist
- Success message on completion

### Password Reset

**Layout:**
- Email input field
- Submit button
- Back to login link

**Design Requirements:**
- Clear instructions
- Success message with next steps
- Error handling for invalid emails

### Password Reset Confirmation

**Layout:**
- New password field
- Confirm password field
- Password strength meter
- Reset button

**Design Requirements:**
- Real-time password validation
- Success message with login prompt
- Error handling for invalid tokens

## User Profile Pages

### Profile Header

**Layout:**
- Profile background image
- Profile picture (circular, 120px)
- User name and bio
- Follow/Unfollow button
- Edit profile button (for own profile)
- Social links
- Stats (posts, followers, following)

**Design Requirements:**
- Responsive layout
- Hover effects on interactive elements
- Clear visual hierarchy
- Loading states for async actions

### Profile Tabs

**Layout:**
- Horizontal tab navigation
- Content area below
- Active tab indicator

**Tabs:**
- Posts
- Comments
- Activity
- Followers
- Following
- About

### Edit Profile

**Layout:**
- Form with all editable fields
- Profile picture upload
- Background image upload
- Save button
- Cancel button

**Design Requirements:**
- Real-time preview
- Image crop functionality
- Clear field labels
- Validation messages

## Navigation

### Main Navigation

**Desktop:**
- Horizontal navbar
- Logo on left
- Menu items center
- User actions right
- Dropdown menus for sub-items

**Mobile:**
- Hamburger menu
- Slide-out sidebar
- Bottom navigation bar
- Collapsible sections

### Breadcrumb Navigation

**Layout:**
```html
<nav class="breadcrumb">
  <a href="/">Home</a>
  <span class="breadcrumb-separator">></span>
  <a href="/forums">Forums</a>
  <span class="breadcrumb-separator">></span>
  <span class="breadcrumb-current">General</span>
</nav>
```

### Pagination

**Layout:**
```html
<div class="pagination">
  <button class="pagination-prev" disabled>Previous</button>
  <button class="pagination-item active">1</button>
  <button class="pagination-item">2</button>
  <button class="pagination-item">3</button>
  <span class="pagination-ellipsis">...</span>
  <button class="pagination-item">10</button>
  <button class="pagination-next">Next</button>
</div>
```

## Forms & Inputs

### Form Layout

**Best Practices:**
- Single column layout (mobile-friendly)
- Group related fields
- Clear labels above fields
- Help text below fields
- Error messages below fields
- Primary action button at bottom

### Input Fields

**Text Input:**
```html
<div class="form-group">
  <label for="name">Name</label>
  <input type="text" id="name" class="form-control" placeholder="Enter your name">
</div>
```

**Textarea:**
```html
<div class="form-group">
  <label for="bio">Bio</label>
  <textarea id="bio" class="form-control" rows="4" placeholder="Tell us about yourself"></textarea>
  <span class="form-help">Max 500 characters</span>
</div>
```

**Select Dropdown:**
```html
<div class="form-group">
  <label for="country">Country</label>
  <select id="country" class="form-control">
    <option value="">Select country</option>
    <option value="us">United States</option>
    <option value="uk">United Kingdom</option>
  </select>
</div>
```

**Checkbox:**
```html
<div class="form-group">
  <div class="checkbox">
    <input type="checkbox" id="terms">
    <label for="terms">I agree to the terms and conditions</label>
  </div>
</div>
```

**Radio Buttons:**
```html
<div class="form-group">
  <label>Gender</label>
  <div class="radio-group">
    <div class="radio">
      <input type="radio" id="male" name="gender" value="male">
      <label for="male">Male</label>
    </div>
    <div class="radio">
      <input type="radio" id="female" name="gender" value="female">
      <label for="female">Female</label>
    </div>
    <div class="radio">
      <input type="radio" id="other" name="gender" value="other">
      <label for="other">Other</label>
    </div>
  </div>
</div>
```

### Form Validation

**Client-side Validation:**
- Real-time validation on blur
- Show error messages immediately
- Disable submit button if form invalid
- Visual feedback for invalid fields

**Server-side Validation:**
- Always validate on server
- Show server errors clearly
- Maintain form state on error

## Responsive Design

### Mobile-First Approach
- Design for mobile first, then scale up
- Use relative units (rem, %, vh/vw)
- Test on multiple screen sizes
- Use media queries for breakpoints

### Breakpoint Examples

```css
/* Mobile */
@media (min-width: 360px) { /* Extra small devices */ }

/* Small devices */
@media (min-width: 576px) { }

/* Medium devices */
@media (min-width: 768px) { }

/* Large devices */
@media (min-width: 992px) { }

/* Extra large devices */
@media (min-width: 1200px) { }

/* 2K and above */
@media (min-width: 1440px) { }
```

### Responsive Patterns

**1. Stacked to Horizontal:**
```css
/* Mobile - stacked */
.item { width: 100%; }

/* Desktop - horizontal */
@media (min-width: 768px) {
  .item { width: 33.33%; float: left; }
}
```

**2. Hidden on Mobile:**
```css
.secondary-nav { display: none; }

@media (min-width: 992px) {
  .secondary-nav { display: block; }
}
```

**3. Mobile Menu:**
```css
.nav-menu { display: none; }

@media (min-width: 768px) {
  .nav-menu { display: flex; }
}
```

## Accessibility

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Logical tab order
- Visual focus indicators
- Skip to content link

### ARIA Attributes
- Use ARIA roles and properties
- `aria-label` for icon buttons
- `aria-hidden="true"` for decorative elements
- `aria-live` regions for dynamic content

### Color Contrast
- Minimum 4.5:1 contrast ratio for text
- Minimum 3:1 for large text (18.66px+)
- Use contrast checkers to verify

### Semantic HTML
- Use proper HTML5 elements
- `<button>` for buttons, not `<div>`
- `<nav>` for navigation
- `<main>` for main content
- `<article>`, `<section>`, `<aside>` appropriately

### Screen Reader Support
- Test with screen readers (NVDA, VoiceOver)
- Provide text alternatives for images
- Use proper heading hierarchy
- Avoid "click here" links

## Performance

### Image Optimization
- Use WebP format where possible
- Compress images (quality 80-85%)
- Use `srcset` for responsive images
- Lazy load offscreen images
- Use CDN for image delivery

### Code Optimization
- Minify CSS and JavaScript
- Bundle and tree-shake JavaScript
- Use code splitting
- Remove unused CSS
- Critical CSS in head

### Resource Loading
- Preload critical resources
- Defer non-critical JavaScript
- Use `async` for independent scripts
- Lazy load iframes and videos
- Use font-display: swap

### Caching
- Set proper cache headers
- Cache static assets aggressively
- Use service workers for offline caching
- Implement cache busting for updates

## Animation & Transitions

### Animation Principles
- Purposeful animations only
- Keep animations short (200-400ms)
- Use easing functions for natural motion
- Avoid animations on user preference (reduced motion)

### CSS Transitions
```css
.transition {
  transition: all 0.3s ease;
}

.fade-in {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.fade-in.visible {
  opacity: 1;
}
```

### Common Animations
- **Fade**: For modal appearances
- **Slide**: For drawer menus
- **Scale**: For button presses
- **Rotate**: For loading indicators
- **Bounce**: For attention (use sparingly)

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Error States

### Form Errors
- Clear error messages
- Visual indication of invalid fields
- Help text for correction
- Error summary at top

### API Errors
- User-friendly messages
- Retry options where appropriate
- Error codes for debugging
- Logging for development

### 404 Pages
- Helpful message
- Search functionality
- Navigation options
- Brand consistency

## Loading States

### Button Loading
```html
<button class="btn btn-primary" disabled>
  <span class="btn-text">Loading...</span>
  <span class="btn-spinner"></span>
</button>
```

### Page Loading
- Skeleton screens for content
- Progress indicators
- Loading spinners
- Estimated time remaining

### Lazy Loading
- Placeholder content
- Smooth transitions
- Loading indicators
- Error handling

## Empty States

### Empty Lists
- Friendly message
- Call to action
- Illustration or icon
- Example: "No posts yet. Create your first post!"

### Search Results
- "No results found"
- Search tips
- Related suggestions
- Option to clear filters

### Onboarding
- Welcome message
- Getting started guide
- Feature highlights
- Call to action

## Internationalization

### Language Support
- Right-to-left (RTL) language support
- Language switcher
- Localized content
- Date/time formatting

### Translation
- Use translation keys
- Avoid concatenated strings
- Provide context for translators
- Test with different languages

### Date & Time
- Localized formatting
- Timezone support
- Relative time ("2 hours ago")
- Absolute time with timezone

## Dark Mode

### Implementation
- CSS custom properties
- Media query detection
- User preference storage
- Smooth transitions

### Color Scheme
```css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-color: #121212;
    --text-color: #E0E0E0;
    --surface-color: #1E1E1E;
  }
}

.dark-mode {
  --bg-color: #121212;
  --text-color: #E0E0E0;
  --surface-color: #1E1E1E;
}
```

### Toggle
- Manual toggle in settings
- System preference detection
- Smooth transition between modes
- Persist user preference

## Code Standards

### React Components

**File Structure:**
```
components/
  Button/
    Button.jsx
    Button.module.css
    Button.test.js
    index.js
```

**Component Structure:**
```jsx
import React from 'react';
import PropTypes from 'prop-types';
import styles from './Button.module.css';

const Button = ({ children, variant = 'primary', size = 'medium', ...props }) => {
  const className = `${styles.button} ${styles[variant]} ${styles[size]}`;
  
  return (
    <button className={className} {...props}>
      {children}
    </button>
  );
};

Button.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary', 'text']),
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  onClick: PropTypes.func,
};

export default Button;
```

### CSS Methodology

**BEM-like Naming:**
```css
/* Block */
.card {}

/* Element */
.card__header {}
.card__body {}
.card__footer {}

/* Modifier */
.card--featured {}
.card--disabled {}

/* State */
.card.is-active {}
.card.is-loading {}
```

### JavaScript Standards

- Use ES6+ features
- Prefer arrow functions
- Use const/let, avoid var
- Destructure objects and arrays
- Use template literals
- Async/await for promises
- Proper error handling

### Testing

**Unit Tests:**
- Test individual components
- Mock dependencies
- Test edge cases

**Integration Tests:**
- Test component interactions
- Test API calls
- Test state management

**E2E Tests:**
- Test user flows
- Test authentication
- Test critical paths

## Resources

### Design Tools
- Figma for UI design
- Adobe XD for prototyping
- Whimsical for flowcharts
- Miro for collaboration

### Development Tools
- React Developer Tools
- Redux DevTools
- Chrome DevTools
- Lighthouse for audits
- Storybook for components

### Libraries
- **UI Components**: Material-UI, Chakra UI, or custom
- **Forms**: React Hook Form, Formik
- **Routing**: React Router
- **State**: Redux Toolkit, Context API
- **Styling**: CSS Modules, Styled Components, or Tailwind
- **Icons**: React Icons, Material Icons
- **Animation**: Framer Motion, React Spring
- **Internationalization**: react-i18next
- **Testing**: Jest, React Testing Library, Cypress

### Learning Resources
- React Documentation
- MDN Web Docs
- A11Y Project
- CSS Tricks
- Google Web Fundamentals

## Implementation Checklist

### For Developers
- [ ] Follow component structure guidelines
- [ ] Use proper naming conventions
- [ ] Implement responsive design
- [ ] Add proper accessibility attributes
- [ ] Write unit tests
- [ ] Document components
- [ ] Follow code review guidelines

### For Designers
- [ ] Use approved color palette
- [ ] Follow typography guidelines
- [ ] Maintain consistent spacing
- [ ] Design for all screen sizes
- [ ] Consider accessibility
- [ ] Provide design tokens
- [ ] Document design decisions

### For QA
- [ ] Test on multiple devices
- [ ] Verify accessibility compliance
- [ ] Test performance
- [ ] Check cross-browser compatibility
- [ ] Validate responsive behavior
- [ ] Test error states
- [ ] Verify internationalization

## Version History

### Version 1.0 (Current)
- Initial UI/UX guidelines
- Core design system
- Component patterns
- Responsive design principles
- Accessibility standards

## Contact

For UI/UX related questions:
- **Email**: ux-team@discussit.eu
- **Slack**: #ux-design channel
- **Figma**: discussit.figma.com

## License

This document is licensed under the MIT License. See the LICENSE file for details.