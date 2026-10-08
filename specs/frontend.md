# Frontend Specification - PromptLab

## Overview

A React frontend for managing AI prompts. Users can create, edit, delete prompts, organize them into collections, and search through them. The UI should be simple and straightforward - no fancy animations, just functional and clean.

## Folder Structure Principle

**Components are organized by feature (prompts, collections, shared) with API calls in a separate api folder, keeping all backend communication isolated from UI components.**

## Screens

### 1. Dashboard (Home)
**Purpose:** Main screen where users see all their prompts and can search/filter them.

**What's on it:**
- Header with app name
- Search bar at top
- List of all prompts (cards)
- Sidebar showing collections
- Button to create new prompt

**API endpoints used:**
- `GET /prompts` - list all prompts
- `GET /prompts?search={query}` - search prompts
- `GET /prompts?collection_id={id}` - filter by collection
- `GET /collections` - list collections for sidebar

### 2. Prompt Detail View
**Purpose:** See full details of a single prompt and edit/delete it.

**What's on it:**
- Full prompt title, content, description
- Tags displayed
- Edit button
- Delete button (with confirmation)
- Back button

**API endpoints used:**
- `GET /prompts/{id}` - get single prompt
- `DELETE /prompts/{id}` - delete prompt

### 3. Create/Edit Prompt Form
**Purpose:** Form to create new prompt or edit existing one.

**What's on it:**
- Title field (required)
- Content textarea (required)
- Description field (optional)
- Collection dropdown (optional)
- Tags input (optional)
- Save button
- Cancel button

**API endpoints used:**
- `POST /prompts` - create new prompt
- `PUT /prompts/{id}` - update existing prompt
- `GET /collections` - populate dropdown

## Component Inventory

### Layout Components

**Layout.jsx**
- **Responsibility:** Main wrapper for all pages, includes header and sidebar
- **Props:** `children` - page content to display
- **Notes:** Always visible, provides consistent structure

**Header.jsx**
- **Responsibility:** Top navigation bar with app title
- **Props:** None
- **Notes:** Just shows "PromptLab" title, maybe a logo later

**Sidebar.jsx**
- **Responsibility:** Shows list of collections for filtering
- **Props:** `collections` - array of collection objects, `onSelectCollection` - callback when collection clicked
- **Notes:** Includes "All Prompts" option to clear filter

### Prompt Components

**PromptList.jsx**
- **Responsibility:** Displays grid/list of prompt cards
- **Props:** `prompts` - array of prompt objects, `onSelectPrompt` - callback when prompt clicked
- **Notes:** Shows loading spinner while fetching, "No prompts yet" message when empty

**PromptCard.jsx**
- **Responsibility:** Single prompt preview card
- **Props:** `prompt` - prompt object (id, title, content preview, tags)
- **Notes:** Shows first 100 chars of content, clickable to open detail view

**PromptDetail.jsx**
- **Responsibility:** Full prompt view with edit/delete options
- **Props:** `promptId` - ID of prompt to display
- **Notes:** Fetches prompt data itself, handles loading and error states

**PromptForm.jsx**
- **Responsibility:** Form for creating/editing prompts
- **Props:** `promptId` - ID if editing (null if creating), `onSuccess` - callback after save, `onCancel` - callback for cancel
- **Notes:** Validates required fields before submit, shows error if API call fails

### Collection Components

**CollectionList.jsx**
- **Responsibility:** List of collections in sidebar
- **Props:** `collections` - array of collections, `selectedId` - currently selected collection, `onSelect` - callback when clicked
- **Notes:** Shows collection name and count of prompts

**CollectionForm.jsx**
- **Responsibility:** Small form to create new collection
- **Props:** `onSuccess` - callback after creation
- **Notes:** Just name and description fields, keeps it simple

### Shared Components

**Button.jsx**
- **Responsibility:** Reusable button with consistent styling
- **Props:** `children` - button text, `onClick` - click handler, `variant` - primary/secondary/danger, `disabled` - boolean
- **Notes:** Different colors for different actions (red for delete, blue for save, etc)

**Modal.jsx**
- **Responsibility:** Popup overlay for confirmations and forms
- **Props:** `isOpen` - boolean, `onClose` - close handler, `title` - modal title, `children` - modal content
- **Notes:** Used for delete confirmations and showing forms

**SearchBar.jsx**
- **Responsibility:** Search input with submit
- **Props:** `onSearch` - callback with search query, `placeholder` - input placeholder text
- **Notes:** Calls onSearch after user stops typing (debounced)

**LoadingSpinner.jsx**
- **Responsibility:** Shows loading indicator
- **Props:** `message` - optional loading text
- **Notes:** Simple spinner, shows while data is being fetched

**ErrorMessage.jsx**
- **Responsibility:** Displays error messages to user
- **Props:** `message` - error text to show, `onDismiss` - optional close handler
- **Notes:** Red box with error text, used when API calls fail

## State Management

Using React's built-in `useState` and `useEffect` hooks. No Redux or other libraries needed - keeping it simple.

**What state lives where:**
- **App-level state:** Current collection filter, search query
- **Component state:** Form inputs, loading flags, error messages
- **No global state management:** Each component fetches its own data when needed

**Data fetching approach:**
- Components fetch data in `useEffect` when they mount
- Parent components pass data to children as props
- Forms trigger refetch in parent after successful save

## Loading States

Every async operation shows feedback:

- **Fetching prompts:** Show `LoadingSpinner` in place of `PromptList`
- **Fetching single prompt:** Show `LoadingSpinner` in `PromptDetail`
- **Saving form:** Disable submit button, show "Saving..." text
- **Deleting prompt:** Show "Deleting..." in button

## Error States

API failures show user-friendly messages:

- **Failed to load prompts:** Show `ErrorMessage` "Couldn't load prompts. Try refreshing."
- **Failed to load prompt detail:** Show `ErrorMessage` "Prompt not found or failed to load."
- **Failed to save:** Show `ErrorMessage` below form "Failed to save. Please try again."
- **Failed to delete:** Show `ErrorMessage` "Couldn't delete prompt. Try again."
- **Network error:** Generic message "Network error. Check your connection."

**Important:** Errors never result in blank screen or broken UI - always show message!

## Empty States

Clear messages when there's no data:

- **No prompts yet:** "No prompts yet. Create your first prompt to get started!"
- **No search results:** "No prompts match '{query}'. Try a different search."
- **No collections:** "No collections yet. All prompts will appear here."
- **Collection with no prompts:** "This collection is empty."

## Styling Approach

Using **Tailwind CSS** for styling because:
- Fast to write
- No separate CSS files to manage
- Consistent design tokens built-in
- Good responsive utilities

**Color scheme:**
- Primary: Blue (buttons, links)
- Danger: Red (delete buttons)
- Background: Light gray
- Cards: White with shadow
- Text: Dark gray

## Forms and Validation

**PromptForm validation:**
- Title: Required, show error "Title is required" if empty
- Content: Required, show error "Content is required" if empty
- Description: Optional, no validation
- Collection: Optional, no validation
- Tags: Optional, no validation

**Validation timing:**
- Check on form submit
- Show errors below each field
- Disable submit if errors present

**CollectionForm validation:**
- Name: Required, show error "Name is required" if empty
- Description: Optional, no validation

## Responsive Design

**Mobile (< 768px):**
- Hide sidebar by default (maybe add hamburger menu later)
- Stack prompt cards vertically
- Forms take full width
- Touch-friendly button sizes

**Desktop (>= 768px):**
- Sidebar always visible on left
- Prompt cards in grid (2-3 columns)
- Forms in centered modal
- Normal button sizes

## Keyboard Accessibility

Basic keyboard support:
- All buttons/links focusable with Tab
- Enter key submits forms
- Escape key closes modals
- Search bar auto-focuses when clicking search icon

Not worrying about screen readers for now - just making sure keyboard users can navigate.

## API Integration Details

**Base URL:**
- Development: `http://localhost:8000`
- Production: Set via `VITE_API_URL` environment variable

**Error handling:**
- 404: Show "Not found" message
- 400: Show "Invalid request" message
- 500: Show "Server error" message
- Network error: Show "Network error" message

**Headers:**
- `Content-Type: application/json` for all requests
- CORS already configured on backend

## User Flows

### Create Prompt Flow
1. Click "New Prompt" button
2. Modal opens with `PromptForm`
3. Fill in title and content (required)
4. Optionally add description, collection, tags
5. Click "Save"
6. Form validates and submits
7. On success: Modal closes, list refreshes, see new prompt
8. On error: Error message shows, form stays open

### Edit Prompt Flow
1. Click on prompt card to open detail view
2. Click "Edit" button
3. Modal opens with `PromptForm` pre-filled
4. Make changes
5. Click "Save"
6. On success: Modal closes, detail view updates
7. On error: Error message shows

### Delete Prompt Flow
1. In detail view, click "Delete" button
2. Confirmation modal appears: "Are you sure you want to delete this prompt?"
3. Click "Yes, Delete"
4. Prompt deletes
5. On success: Navigate back to dashboard
6. On error: Error message shows, stay on detail view

### Search Flow
1. Type in search bar
2. After 500ms of no typing, search executes
3. List updates to show matching prompts
4. If no results, show empty state

### Filter by Collection Flow
1. Click collection name in sidebar
2. List filters to show only prompts in that collection
3. Collection name highlights in sidebar
4. Click "All Prompts" to clear filter

## Development Notes

**Start simple:**
- Get basic list/create/delete working first
- Then add search and filter
- Then polish UI and error handling
- Don't try to do everything at once

**Testing approach:**
- Manually test each flow
- Check that errors display properly
- Test on mobile screen size
- Make sure keyboard navigation works

**Things we're NOT doing (to keep scope reasonable):**
- User authentication
- Real-time updates
- Drag and drop
- Fancy animations
- Offline support
- Multiple themes

Just focusing on core CRUD functionality with good error handling.
