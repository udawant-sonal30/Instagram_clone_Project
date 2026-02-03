# Instagram Clone Project
A full-stack Instagram Clone application that replicates core features of Instagram such as user authentication, posting images, liking posts, following users, and viewing personalized feeds.
This project is built for learning purposes and to demonstrate real-world full-stack development skills.

## 🚀 Features:
-🔐 User Authentication (Login & Signup)
-🖼️ Upload Photos 
-❤️ Like & Unlike Posts
-💬 Comment on Posts
-🧑 User Profiles
-➕ Follow & Unfollow Users
-🏠 Home Feed
-🔍 Explore Users
-👥 Followers & Following List

## Project Structure:
Instagram_clone/
├── accounts/         # User authentication and profiles
├── insta/            # Main app configuration
├── media/            # Uploaded images
├── venv/             # Virtual environment (ignored in git)
├── .gitignore
├── db.sqlite3        # Database (ignored in git)
└── manage.py


## Installation:

1. Clone the repository:
   git clone https://github.com/udawant-sonal30/Instagram_clone.git
2. Navigate to project folder:
   cd Instagram_clone
3. Create virtual environment:
   python -m venv venv
4. Activate virtual environment:
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
5. Install dependencies:
   pip install -r requirements.txt
6. Apply migrations:
   python manage.py migrate
7. Run server:
   python manage.py runserver

## Technologies Used:
- Django
- Python 3.x
- HTML/CSS
- SQLite3
- JavaScript    

## Learning Outcomes

- Gained hands-on experience in building a full-stack web application using Django.
- Implemented user authentication, authorization, and profile management.
- Learned to design and manage relational data models using Django ORM.
- Developed features such as posts, likes, comments, and follow/unfollow functionality.
- Worked with media file uploads and static file handling in Django.
- Understood Django project structure, apps, views, templates, and URL routing.
- Practiced version control using Git and GitHub, including proper use of .gitignore.
- Improved problem-solving skills by implementing real-world social media features.
