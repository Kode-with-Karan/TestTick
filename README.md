## 🎓 TESTTICK — Advanced Quiz & Testing Platform

**TESTTICK** is a full-stack, production-ready Django web application tailored for **schools**, **coaching centers**, and **colleges** to manage and conduct multiple-choice quizzes and test series efficiently.

---

### 🚀 Key Features

- 🔐 **Authentication System**
  - Email verification and profile images
  - Role-based access: Admins, Institutions, Students

- 🏫 **Institution Dashboard**
  - Separate panels for Schools, Coaching, Colleges
  - Manage tests, view results, accept/reject student requests

- 📤 **Question Upload**
  - Upload MCQs via Word or Excel files
  - Smart parser detects questions and options
  - Manual question creation supported

- 🔄 **Test Management**
  - Shuffle questions option
  - Schedule tests with time limits and access control
  - Live test series with price tiers

- 📊 **Result System**
  - Downloadable Excel/PDF reports
  - Auto-grading system with analytics

- 📈 **Analytics Module**
  - Student performance tracking
  - Question difficulty stats
  - Institution-wise reporting

- 📧 **Email Notifications**
  - Welcome, test schedules, results, password resets

- 🌐 **Public & Private Tests**
  - Public tests open to all users
  - Private tests restricted to enrolled students only

- 📎 **CSV/PDF Export**
  - Download results, submissions, analytics reports

- 🧠 **Real-Time Insights**
  - Live submissions and result updates via Django Channels

- 🎨 **Modern UI**
  - Tailwind CSS, dark/light mode toggle
  - Responsive design with accessibility support

---

### 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework, Channels
- **Frontend**: Tailwind CSS, Vanilla JS, AJAX
- **Database**: PostgreSQL / SQLite (dev)
- **Auth**: Custom user model with role handling
- **Media Handling**: Python-docx, pandas, openpyxl
- **Deployment**: Gunicorn, Nginx, Docker (optional)

---

### 📂 Modules

- `users`: Auth, profile, registration
- `institutions`: Manage schools/coaching/colleges
- `dashboard`: Institution-specific control panels
- `quiz`: Upload/parse questions
- `testsystem`: Schedule and conduct tests
- `results`: Score calculation and downloads
- `analytics`: Insights and student progress

---

### ✅ Perfect For:

- Educational Institutions
- EdTech Startups
- Online Coaching Platforms
- Internal Corporate Training

---