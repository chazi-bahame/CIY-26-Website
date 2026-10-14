from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
from database import engine, Base
from models import Project, ContactMessage, Gallery, Announcement, TeamMember, News, Event,  JoinApplication
from database import engine, Base
from models import Project
from werkzeug.security import generate_password_hash

load_dotenv()

app = Flask(__name__)

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_TIMEOUT"] = 10
mail = Mail(app)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app.secret_key = os.getenv("SECRET_KEY", "ciy26-development-secret")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            return redirect("/admin")

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect("/admin/login")



# Create database tables
Base.metadata.create_all(bind=engine)


@app.route("/")
def home():
    from database import SessionLocal

    db = SessionLocal()

    projects = db.query(Project).all()
    gallery = db.query(Gallery).all()
    announcements = db.query(Announcement).all()
    team_members = db.query(TeamMember).all()
    news = db.query(News).all()
    events = db.query(Event).all()

    db.close()

    return render_template(
        "index.html",
        projects=projects,
        gallery=gallery,
        announcements=announcements,
        team_members=team_members,
        news=news,
        events=events
    )

@app.route("/news/<int:news_id>")
def news_details(news_id):

    from database import SessionLocal

    db = SessionLocal()

    news_item = db.query(News).filter(
        News.id == news_id
    ).first()

    if not news_item:
        db.close()
        return "News not found", 404

    db.close()

    return render_template(
        "news_details.html",
        news=news_item
    )

@app.route("/project/<int:project_id>")
def project_details(project_id):

    from database import SessionLocal

    db = SessionLocal()

    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        db.close()
        return "Project not found", 404

    db.close()

    return render_template(
        "project_details.html",
        project=project
    )
@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    projects = db.query(Project).all()
    messages = db.query(ContactMessage).all()
    gallery = db.query(Gallery).all()
    announcements = db.query(Announcement).all()
    team_members = db.query(TeamMember).all()
    news = db.query(News).all()
    events = db.query(Event).all()
    join_applications = db.query(JoinApplication).order_by(
    JoinApplication.created_at.desc()
).all()
    total_messages = len(messages)
    unread_messages = db.query(ContactMessage).filter(
        ContactMessage.is_read == 0
    ).count()

    categories = set(project.category for project in projects)

    latest_project = projects[-1] if projects else None

    print("ADMIN PROJECTS:", len(projects))

    db.close()

    return render_template(
        "admin.html",
        projects=projects,
        gallery=gallery,
        announcements=announcements,
        team_members=team_members,
        news=news,
        events=events,
        categories=categories,
        messages=messages,
        total_messages=total_messages,
        unread_messages=unread_messages,
        latest_project=latest_project,
        join_applications=join_applications
    )

@app.route("/admin/add-gallery", methods=["POST"])
def add_gallery():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    title = request.form.get("title")
    description = request.form.get("description")
    image_file = request.files.get("image")

    if not image_file or image_file.filename == "":
        return "Please select an image!"

    image_filename = image_file.filename

    image_path = os.path.join(
        "static",
        "images",
        image_filename
    )

    image_file.save(image_path)

    db = SessionLocal()

    gallery = Gallery(
        title=title,
        description=description,
        image=image_filename
    )

    db.add(gallery)
    db.commit()
    db.close()

    return redirect("/admin")

@app.route("/admin/add-announcement", methods=["POST"])
def add_announcement():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    title = request.form.get("title")
    content = request.form.get("content")

    image_file = request.files.get("image")

    image_filename = None

    if image_file and image_file.filename != "":
        image_filename = image_file.filename

        image_path = os.path.join(
            "static",
            "images",
            image_filename
        )

        image_file.save(image_path)

    db = SessionLocal()

    announcement = Announcement(
        title=title,
        content=content,
        image=image_filename
    )

    db.add(announcement)
    db.commit()
    db.close()

    return redirect("/admin")

@app.route("/admin/add-team-member", methods=["POST"])
def add_team_member():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    name = request.form.get("name")
    position = request.form.get("position")
    description = request.form.get("description")

    image_file = request.files.get("image")

    image_filename = None

    if image_file and image_file.filename != "":
        image_filename = image_file.filename

        image_path = os.path.join(
            "static",
            "images",
            image_filename
        )

        image_file.save(image_path)

    db = SessionLocal()

    team_member = TeamMember(
        name=name,
        position=position,
        description=description,
        image=image_filename
    )

    db.add(team_member)
    db.commit()
    db.close()

    return redirect("/admin")

@app.route("/admin/add-news", methods=["POST"])
def add_news():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    title = request.form.get("title")
    content = request.form.get("content")

    image_file = request.files.get("image")

    image_filename = None

    if image_file and image_file.filename != "":
        image_filename = image_file.filename

        image_path = os.path.join(
            "static",
            "images",
            image_filename
        )

        image_file.save(image_path)

    db = SessionLocal()

    news = News(
        title=title,
        content=content,
        image=image_filename
    )

    db.add(news)
    db.commit()
    db.close()

    return redirect("/admin")

@app.route("/admin/add-event", methods=["POST"])
def add_event():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal
    from datetime import datetime

    title = request.form.get("title")
    description = request.form.get("description")
    event_date = request.form.get("event_date")

    image_file = request.files.get("image")

    image_filename = None

    if image_file and image_file.filename != "":

        image_filename = image_file.filename

        image_path = os.path.join(
            "static",
            "images",
            image_filename
        )

        image_file.save(image_path)

    event_date = datetime.fromisoformat(event_date)

    db = SessionLocal()

    event = Event(
        title=title,
        description=description,
        event_date=event_date,
        image=image_filename
    )

    db.add(event)
    db.commit()
    db.close()

    return redirect("/admin")

@app.route("/admin/delete-event/<int:event_id>", methods=["POST"])
def delete_event(event_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    event = db.query(Event).filter(
        Event.id == event_id
    ).first()

    if event:

        db.delete(event)
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/delete-news/<int:news_id>", methods=["POST"])
def delete_news(news_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    news = db.query(News).filter(
        News.id == news_id
    ).first()

    if news:

        db.delete(news)
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/edit-news/<int:news_id>", methods=["GET", "POST"])
def edit_news(news_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    news = db.query(News).filter(
        News.id == news_id
    ).first()

    if not news:
        db.close()
        return "News not found", 404

    if request.method == "POST":

        news.title = request.form.get("title")
        news.content = request.form.get("content")

        image_file = request.files.get("image")

        if image_file and image_file.filename != "":

            image_filename = image_file.filename

            image_path = os.path.join(
                "static",
                "images",
                image_filename
            )

            image_file.save(image_path)

            if news.image:

                old_image_path = os.path.join(
                    "static",
                    "images",
                    news.image
                )

                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            news.image = image_filename

        db.commit()
        db.close()

        return redirect("/admin")

    db.close()

    return render_template(
        "edit_news.html",
        news=news
    )

@app.route("/admin/delete-gallery/<int:gallery_id>", methods=["POST"])
def delete_gallery(gallery_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    gallery = db.query(Gallery).filter(
        Gallery.id == gallery_id
    ).first()

    if gallery:

        db.delete(gallery)
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/delete-announcement/<int:announcement_id>", methods=["POST"])
def delete_announcement(announcement_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    announcement = db.query(Announcement).filter(
        Announcement.id == announcement_id
    ).first()

    if announcement:

        db.delete(announcement)
        db.commit()

    db.close()

    return redirect("/admin")
@app.route("/admin/delete-team-member/<int:member_id>", methods=["POST"])
def delete_team_member(member_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    member = db.query(TeamMember).filter(
        TeamMember.id == member_id
    ).first()

    if member:

        db.delete(member)
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/edit-team-member/<int:member_id>", methods=["GET", "POST"])
def edit_team_member(member_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    member = db.query(TeamMember).filter(
        TeamMember.id == member_id
    ).first()

    if not member:
        db.close()
        return "Team member not found", 404

    if request.method == "POST":

        member.name = request.form.get("name")
        member.position = request.form.get("position")
        member.description = request.form.get("description")

        image_file = request.files.get("image")

        if image_file and image_file.filename != "":

            image_filename = image_file.filename

            image_path = os.path.join(
                "static",
                "images",
                image_filename
            )

            image_file.save(image_path)

            if member.image:

                old_image_path = os.path.join(
                    "static",
                    "images",
                    member.image
                )

                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            member.image = image_filename

        db.commit()
        db.close()

        return redirect("/admin")

    db.close()

    return render_template(
        "edit_team_member.html",
        member=member
    )

@app.route("/admin/edit-announcement/<int:announcement_id>", methods=["GET", "POST"])
def edit_announcement(announcement_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    announcement = db.query(Announcement).filter(
        Announcement.id == announcement_id
    ).first()

    if not announcement:
        db.close()
        return "Announcement not found", 404

    if request.method == "POST":

        announcement.title = request.form.get("title")
        announcement.content = request.form.get("content")

        image_file = request.files.get("image")

        if image_file and image_file.filename != "":

            image_filename = image_file.filename

            image_path = os.path.join(
                "static",
                "images",
                image_filename
            )

            image_file.save(image_path)

            if announcement.image:

                old_image_path = os.path.join(
                    "static",
                    "images",
                    announcement.image
                )

                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            announcement.image = image_filename

        db.commit()
        db.close()

        return redirect("/admin")

    db.close()

    return render_template(
        "edit_announcement.html",
        announcement=announcement
    )

@app.route("/admin/add-project", methods=["POST"])
def add_project():

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")
    
    from database import SessionLocal

    name = request.form.get("name")
    category = request.form.get("category")
    description = request.form.get("description")

    image_file = request.files.get("image")

    if not image_file or image_file.filename == "":
        return "Please select an image!"

    image_filename = image_file.filename

    image_path = os.path.join(
        "static",
        "images",
        image_filename
    )

    image_file.save(image_path)

    db = SessionLocal()

    project = Project(
        name=name,
        category=category,
        description=description,
        image=image_filename
    )

    db.add(project)
    db.commit()
    db.close()

    return redirect("/admin")
@app.route("/admin/delete-project/<int:project_id>", methods=["POST"])
def delete_project(project_id):

    if not session.get("admin_logged_in"):
         return redirect("/admin/login")
        

    from database import SessionLocal

    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if project:
        db.delete(project)
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/delete-message/<int:message_id>", methods=["POST"])
def delete_message(message_id):

    if not session.get("admin_logged_in"):
         return redirect("/admin/login")
    
    from database import SessionLocal

    db = SessionLocal()

    message = db.query(ContactMessage).filter(
        ContactMessage.id == message_id
    ).first()

    if message:
        db.delete(message)
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/delete-join-application/<int:application_id>", methods=["POST"])
def delete_join_application(application_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    application = db.query(JoinApplication).filter(
        JoinApplication.id == application_id
    ).first()

    if application:
        db.delete(application)
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/accept-join-application/<int:application_id>", methods=["POST"])
def accept_join_application(application_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    application = db.query(JoinApplication).filter(
        JoinApplication.id == application_id
    ).first()

    if application:
        application.status = "Accepted"
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/reject-join-application/<int:application_id>", methods=["POST"])
def reject_join_application(application_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    application = db.query(JoinApplication).filter(
        JoinApplication.id == application_id
    ).first()

    if application:
        application.status = "Rejected"
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/mark-message-read/<int:message_id>", methods=["POST"])
def mark_message_read(message_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    message = db.query(ContactMessage).filter(
        ContactMessage.id == message_id
    ).first()

    if message:
        message.is_read = 1
        db.commit()

    db.close()

    return redirect("/admin")

@app.route("/admin/view-message/<int:message_id>")
def view_message(message_id):

    if not session.get("admin_logged_in"):
        return redirect("/admin/login")

    from database import SessionLocal

    db = SessionLocal()

    message = db.query(ContactMessage).filter(
        ContactMessage.id == message_id
    ).first()

    if not message:
        db.close()
        return "Message not found", 404

    message.is_read = 1
    db.commit()

    return render_template(
        "view_message.html",
        message=message
    )

@app.route("/admin/edit-project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):

    if not session.get("admin_logged_in"):
         return redirect("/admin/login")
    
    from database import SessionLocal

    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if request.method == "POST":

        project.name = request.form.get("name")
        project.category = request.form.get("category")
        project.description = request.form.get("description")
        project.image = request.form.get("image")

        db.commit()
        db.close()

        return redirect("/admin")

    db.close()

    return render_template("edit_project.html", project=project)


@app.route("/contact", methods=["POST"])
def contact():
    from database import SessionLocal

    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    db = SessionLocal()

    try:
        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        db.add(contact_message)
        db.commit()

    except Exception:
        db.rollback()
        app.logger.exception("Failed to save contact message")
        return "Imeshindikana kuhifadhi ujumbe. Tafadhali jaribu tena.", 500

    finally:
        db.close()

    # SEND EMAIL NOTIFICATION
    try:
        msg = Message(
            subject=f"CIY-26 Contact: {subject}",
            sender=app.config["MAIL_USERNAME"],
            recipients=[app.config["MAIL_USERNAME"]],
            body=f"""
New message received from CIY-26 website.

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
        )

        mail.send(msg)

    except Exception:
        app.logger.exception(
            "Email notification failed; contact message is already saved"
        )

    return render_template("message_sent.html")


@app.route("/join", methods=["POST"])
def join_application():

    from database import SessionLocal

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    skill = request.form.get("skill")
    message = request.form.get("message")

    print("JOIN DATA:")
    print("Name:", name)
    print("Email:", email)
    print("Phone:", phone)
    print("Skill:", skill)
    print("Message:", message)

    db = SessionLocal()

    application = JoinApplication(
        name=name,
        email=email,
        password=generate_password_hash(password),
        phone=phone,
        skill=skill,
        message=message
    )

    db.add(application)
    db.commit()

    print("JOIN APPLICATION SAVED:", application.id)

    db.close()

    return render_template("join_success.html")

@app.route("/member/login", methods=["GET", "POST"])
def member_login():

    if request.method == "POST":

        from database import SessionLocal
        from werkzeug.security import check_password_hash

        email = request.form.get("email")
        password = request.form.get("password")

        db = SessionLocal()

        application = db.query(JoinApplication).filter(
            JoinApplication.email == email
        ).first()

        if not application:
            db.close()
            return render_template(
                "member_login.html",
                error="Email or password is incorrect."
            )

        if not check_password_hash(application.password, password):
            db.close()
            return render_template(
                "member_login.html",
                error="Email or password is incorrect."
            )

        if application.status != "Accepted":
            db.close()
            return render_template(
                "member_login.html",
                error="Your application has not been accepted yet."
            )

        session["member_logged_in"] = True
        session["member_id"] = application.id
        session["member_name"] = application.name

        db.close()

        return redirect("/member/dashboard")

    return render_template("member_login.html")

@app.route("/member/dashboard")
def member_dashboard():

    if not session.get("member_logged_in"):
        return redirect("/member/login")

    return render_template(
        "member_dashboard.html",
        member_name=session.get("member_name")
    )

@app.route("/member/profile")
def member_profile():

    if not session.get("member_logged_in"):
        return redirect("/member/login")

    from database import SessionLocal

    db = SessionLocal()

    member = db.query(JoinApplication).filter(
        JoinApplication.id == session.get("member_id")
    ).first()

    db.close()

    if not member:
        session.clear()
        return redirect("/member/login")

    return render_template(
        "member_profile.html",
        member=member
    )

@app.route("/member/logout")
def member_logout():

    session.pop("member_logged_in", None)
    session.pop("member_id", None)
    session.pop("member_name", None)

    return redirect("/member/login")

@app.route("/member/application")
def member_application():

    if not session.get("member_logged_in"):
        return redirect("/member/login")

    from database import SessionLocal

    db = SessionLocal()

    application = db.query(JoinApplication).filter(
        JoinApplication.id == session.get("member_id")
    ).first()

    db.close()

    if not application:
        session.clear()
        return redirect("/member/login")

    return render_template(
        "member_application.html",
        application=application
    )

@app.route("/member/announcements")
def member_announcements():

    if not session.get("member_logged_in"):
        return redirect("/member/login")

    from database import SessionLocal

    db = SessionLocal()

    announcements = db.query(Announcement).all()

    db.close()

    return render_template(
        "member_announcements.html",
        announcements=announcements
    )

@app.route("/member/events")
def member_events():

    if not session.get("member_logged_in"):
        return redirect("/member/login")

    from database import SessionLocal

    db = SessionLocal()

    events = db.query(Event).order_by(
        Event.event_date.asc()
    ).all()

    db.close()

    return render_template(
        "member_events.html",
        events=events
    )

@app.route("/member/news")
def member_news():

    if not session.get("member_logged_in"):
        return redirect("/member/login")

    from database import SessionLocal

    db = SessionLocal()

    news = db.query(News).order_by(
        News.created_at.desc()
    ).all()

    db.close()

    return render_template(
        "member_news.html",
        news=news
    )
@app.route("/member/projects")
def member_projects():

    if not session.get("member_logged_in"):
        return redirect("/member/login")

    from database import SessionLocal

    db = SessionLocal()

    projects = db.query(Project).all()

    db.close()

    return render_template(
        "member_projects.html",
        projects=projects
    )

if __name__ == "__main__":
    app.run(debug=False)