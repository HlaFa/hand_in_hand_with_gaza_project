🤝 HandInHand with Gaza

HandInHand with Gaza is a compassionate and user-friendly Django-based web platform designed to connect donors with families in Gaza in need of essential support such as food, medicine, and other necessities.

The website provides role-based access for donors, recipients, and administrators, ensuring secure interactions, transparent case management, and seamless donation workflows.

✨ Features
👥 User Roles & Permissions

1. Admin

Manage all users, cases, donations, categories, and attachments.
Approve/reject attachments.

2. Donor

Browse cases and donate.
View donation history.

3. Recipient

Create and manage personal cases.
Upload and manage attachments.
Track donation status.
🛠️ CRUD Operations
Admin: Full CRUD on all cases and categories.
Recipient: CRUD only on their own cases.
Donor: Read-only access to cases & categories.
📎 Attachments
Recipients upload documents/images for cases.
Admin approves/rejects attachments.
🔐 Authentication & Security
Secure registration and login with hashed passwords.
Form validation on both frontend and backend.
Session-based authentication for role-based redirects.
📱 Responsive UI
Material-UI for buttons, dialogs, and alerts.
Bootstrap 5 for layouts, navigation, and responsiveness.
Optimized for desktop, tablet, and mobile devices.
🖥️ Tech Stack
Backend: Django, Python
Frontend: Bootstrap 5, Material-UI, CSS, JS

Database: MySQL
Authentication: Django’s session-based auth with password hashing
Deployment: AWS (planned)
