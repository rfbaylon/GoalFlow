# Summer 2 2025 CS 3200 Project - What is Goal Planner (Global GoalFlow)?

Goal Planner is a comprehensive goal and habit management platform that transforms how people approach long-term achievement by making data work for them, not against them. Unlike traditional to-do apps that leave users drowning in endless lists, Goal Planner intelligently breaks down ambitious projects into manageable phases, automatically suggests next tasks when you complete something, and seamlessly integrates daily habits with major milestones.

By collecting and analyzing user progress patterns, deadline adherence, and completion rates, our app provides personalized insights that help users understand their productivity patterns and optimize their approach to goal achievement.

We're building this for four distinct user types: individual achievers like freelancers and students who juggle multiple projects, professionals and researchers who need structured approaches to complex work, business analysts who require data-driven insights into team performance and goal completion rates, and system administrators who need robust, scalable platforms for managing user communities.

This repo includes the infrastrucure setup, a MySQL database along with mock data, and example UI pages.

### Project Members

- Ryan Baylon  
- Hyeyeon Seo
- Jaden Hu
- Rishik Kellar
- Fabrizio Flores

---

## Prerequisites

Before starting, make sure you have:

- A GitHub account  
- Git client (terminal or GUI such as GitHub Desktop or Git plugin for VSCode)  
- VSCode with the Python Plugin or your preferred IDE  
- Docker and Docker Compose installed on your machine  

---

## Repo Structure
The repo is organized into five main directories:

- `./app` – Frontend Streamlit app for user interaction.
- `./api` – Backend REST API (Flask) to handle business logic and database communication.
- `./database-files` – SQL scripts to initialize and seed the MySQL database with mock data.  
- `./datasets` – Folder for datasets (if needed).
- `docker-compose.yaml` – Configuration to start the app, API, and MySQL database containers.

---

## Database Setup

We use a MySQL database named `global-GoalFlow`. The schema includes tables to manage users, goals, tasks, posts, tags, bug reports, and more, supporting the core functionality of Goal Planner.

### Key Tables Overview

- **users**: Stores user profiles, roles, contact info, and management relationships.
- **tags**: Categories for goals, posts, and tasks.
- **posts** & **post_reply**: Community forum posts and replies.
- **user_data**: Tracks user activity, devices, and login info.
- **bug_reports**: For tracking issues submitted by users.
- **consistent_tasks**, **daily_tasks**: Task management for recurring and daily items.
- **goals** & **subgoals**: Hierarchical goal tracking with status, priority, and deadlines.

The database schema is designed to support role-based access, data integrity, and efficient queries with proper indexes and foreign keys.

---

## How to Build and Run

### 1. Clone the Repository

```bash
git clone <YOUR_REPO_URL>
cd <REPO_FOLDER>
```

### 2. Set up Environment Variables
Copy the **.env.template** file inside the **api** folder and rename it to **.env**. Edit the .env file to include your database credentials and secrets. Make sure passwords are secure and unique.

### 3. Start Docker Containers
Use Docker Compose to start the full stack:

```bash
docker compose up -d
```
This will start:
   - MySQL database container
   - Flask REST API backend
   - Streamlit frontend app

To stop and remove containers:
```bash
docker compose down
```

### 4. Initialize the Database
Run the SQL scripts inside ./database-files to create tables and insert initial data:

```bash
mysql -u <username> -p < ./database-files/schema.sql
```
Or connect to the running MySQL container and execute the scripts.

---

## User Personas & Stories

Persona 1: Avery - Freelance Designer
   - Juggles client and personal projects.
   - Needs task automation and habit tracking to stay consistent.
   - Wants a visual dashboard for progress and deadlines.
   - Requires space for creative ideas and manageable workflows.

Persona 2: Dr. Alan - Professor
   - Math professor balancing research and teaching.
   - Needs categorized projects, priority control, and deadline management.
   - Wants completed projects archived but accessible for reference.

Persona 3: Jose – System Administrator
   - Oversees app scalability, user support, and community engagement.
   - Requires bug tracking dashboard, user analytics, and payment plan insights.

Persona 4: Jack – Financial Analyst
   - Tracks company goals and employee task completion.
   - Needs subgoal checkboxes, deadlines, and aggregated progress reports.

---

### Features
   - Automatic project phase generation prevents overwhelming long-term goals
   - Intelligent task queuing surfaces next actionable items automatically
   - Comprehensive analytics dashboards provide insights into productivity patterns
   - Role-based access control supports users with distinct permissions and views
   - Community forum for user discussions, bug reports, and feedback
   - Task and goal hierarchy with tags, priorities, and scheduling

---

## Notes on User Roles and Access Control
Our platform implements a simple Role-Based Access Control (RBAC) system, differentiating between:
    - Individual users (freelancers, researchers)
    - Business analysts and managers
    - System administrators

Each role experiences a customized view with access to features relevant to their needs and permissions.

---

## Contact & Support
For questions or bug reports, please open an issue in the GitHub repository or contact the system administrator (Ryan).