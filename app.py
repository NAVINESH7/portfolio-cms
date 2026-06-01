from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file,
    send_from_directory
)

import os
import json
import shutil
from datetime import datetime
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

PROJECTS_FOLDER = "projects"

UPLOAD_FOLDER = "static/uploads"
CERTIFICATE_FOLDER = "static/certificates"
VISITORS_FILE = "visitors.json"

os.makedirs(
    CERTIFICATE_FOLDER,
    exist_ok=True
)

os.makedirs(PROJECTS_FOLDER, exist_ok=True)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==================================================
# SETTINGS
# ==================================================

def load_settings():

    if os.path.exists("settings.json"):

        try:

            with open("settings.json", "r") as file:

                return json.load(file)

        except:

            pass

    return {
        "hero_title": "NAVINESH P K",
        "hero_subtitle": "Portfolio Website",
        "about_text": "About Me",
        "email": "",
        "phone": "",
        "github": "",
        "linkedin": "",
        "resume": ""
    }


def save_settings(settings):

    with open("settings.json", "w") as file:

        json.dump(settings, file, indent=4)

# ==================================================
# SAVE PROJECT
# ==================================================

def save_project(project):

    slug = project["slug"]

    project_folder = os.path.join(
        PROJECTS_FOLDER,
        slug
    )

    os.makedirs(
        project_folder,
        exist_ok=True
    )

    json_file = os.path.join(
        project_folder,
        "project.json"
    )

    with open(
        json_file,
        "w"
    ) as file:

        json.dump(
            project,
            file,
            indent=4
        )

# ==================================================
# SKILLS
# ==================================================

def load_skills():

    if os.path.exists("skills.json"):

        try:

            with open("skills.json", "r") as file:

                return json.load(file)

        except:

            pass

    return []


def save_skills(skills):

    with open("skills.json", "w") as file:

        json.dump(skills, file, indent=4)

# ==================================================
# SOFT SKILLS
# ==================================================

def load_soft_skills():

    if os.path.exists("soft_skills.json"):

        try:

            with open("soft_skills.json", "r") as file:

                return json.load(file)

        except:

            pass

    return []


def save_soft_skills(soft_skills):

    with open("soft_skills.json", "w") as file:

        json.dump(
            soft_skills,
            file,
            indent=4
        )

# ==================================================
# EXTRA CURRICULAR
# ==================================================

def load_extra_curricular():

    if os.path.exists("extra_curricular.json"):

        try:

            with open("extra_curricular.json", "r") as file:

                return json.load(file)

        except:

            pass

    return []


def save_extra_curricular(extra_curricular):

    with open("extra_curricular.json", "w") as file:

        json.dump(
            extra_curricular,
            file,
            indent=4
        )

# ==================================================
# EDUCATION
# ==================================================

def load_education():

    if os.path.exists("education.json"):

        try:

            with open("education.json", "r") as file:

                return json.load(file)

        except:

            pass

    return []


def save_education(education):

    with open("education.json", "w") as file:

        json.dump(
            education,
            file,
            indent=4
        )

# ==================================================
# CERTIFICATES
# ==================================================

def load_certificates():

    if os.path.exists("certificates.json"):

        try:

            with open("certificates.json", "r") as file:

                return json.load(file)

        except:

            pass

    return []


def save_certificates(certificates):

    path = os.path.abspath("certificates.json")

    
    with open(path, "w") as file:

        json.dump(
            certificates,
            file,
            indent=4
        )

# ==================================================
# INTERNSHIPS
# ==================================================

def load_internships():

    if os.path.exists("internships.json"):

        try:

            with open("internships.json", "r") as file:

                return json.load(file)

        except:

            pass

    return []


def save_internships(internships):

    with open("internships.json", "w") as file:

        json.dump(
            internships,
            file,
            indent=4
        )


# ==================================================
# ACHIEVEMENTS
# ==================================================

def load_achievements():

    if os.path.exists("achievements.json"):

        try:

            with open("achievements.json", "r") as file:

                data = json.load(file)

                

                return data

        except Exception as e:
            return []

def save_achievements(achievements):

    with open("achievements.json", "w") as file:

        json.dump(
            achievements,
            file,
            indent=4
        )

# ==================================================
# VISITOR COUNTER
# ==================================================

def get_visitor_count():

    if os.path.exists(VISITORS_FILE):

        try:

            with open(VISITORS_FILE, "r") as file:

                data = json.load(file)

                return data.get("count", 0)

        except:

            pass

    return 0


def increment_visitor_count():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    data = {

        "count": 0,
        "daily": {}

    }

    if os.path.exists(VISITORS_FILE):

        try:

            with open(VISITORS_FILE, "r") as file:

                data = json.load(file)

        except:

            pass

    data["count"] += 1

    if "daily" not in data:

        data["daily"] = {}

    data["daily"][today] = (

        data["daily"].get(today, 0) + 1

    )

   
    with open(VISITORS_FILE, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


def get_visitor_stats():

    if not os.path.exists(VISITORS_FILE):

        return {
            "today": 0,
            "week": 0,
            "month": 0
        }

    try:

        with open(VISITORS_FILE, "r") as file:

            data = json.load(file)

    except:

        return {
            "today": 0,
            "week": 0,
            "month": 0
        }

    daily = data.get("daily", {})

    today_count = 0
    week_count = 0
    month_count = 0

    current_date = datetime.now()

    for date_str, count in daily.items():

        try:

            visit_date = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            days = (
                current_date - visit_date
            ).days

            if days == 0:

                today_count += count

            if days <= 7:

                week_count += count

            if days <= 30:

                month_count += count

        except:

            pass

    return {

        "today": today_count,
        "week": week_count,
        "month": month_count

    }


# ==================================================
# PROJECTS
# ==================================================

def load_projects():

    projects = []

    if not os.path.exists(PROJECTS_FOLDER):

        return projects

    for folder in os.listdir(PROJECTS_FOLDER):

        project_folder = os.path.join(
            PROJECTS_FOLDER,
            folder
        )

        if os.path.isdir(project_folder):

            json_file = os.path.join(
                project_folder,
                "project.json"
            )

            if os.path.exists(json_file):

                try:

                    with open(json_file, "r") as file:

                        project = json.load(file)

                        # SAFE DEFAULTS

                        gallery_folder = os.path.join(
                            project_folder,
                            "gallery"
                        )

                        gallery = []

                        if os.path.exists(gallery_folder):

                            for image in os.listdir(
                                gallery_folder
                            ):

                                gallery.append(
                                    f"/projects/{project['slug']}/gallery/{image}"
                                )

                        project["gallery"] = gallery

                        if "gallery" not in project:
                            project["gallery"] = []

                        if "tech_stack" not in project:
                            project["tech_stack"] = []

                        projects.append(project)

                except Exception as e:

                    print(
                        "PROJECT ERROR:",
                        e
                    )

    return projects

# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():

    if not session.get("visited"):

        increment_visitor_count()
        session["visited"] = True

    return render_template(
        "index.html",
        settings=load_settings(),
        skills=load_skills(),
        soft_skills=load_soft_skills(),
        extra_curricular=load_extra_curricular(),
        projects=load_projects(),
        education=load_education(),
        internships=load_internships(),
        achievements=load_achievements(),
        certificates=load_certificates()
    )


# ==================================================
# LOGIN
# ==================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")

        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin"] = True

            return redirect("/admin")

    return render_template("login.html")


# ==================================================
# LOGOUT
# ==================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==================================================
# ADMIN
# ==================================================

@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect("/login")

    visitor_count = get_visitor_count()
    visitor_stats = get_visitor_stats()
    
    return render_template(
    "admin.html",
    settings=load_settings(),
    skills=load_skills(),
    projects=load_projects(),
    education=load_education(),
    internships=load_internships(),
    certificates=load_certificates(),
    visitor_count=visitor_count,
    visitor_stats=visitor_stats
)

@app.route("/resume")
def resume_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "resume.html",
        settings=load_settings()
    )


@app.route("/website")
def website_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "website.html",
        settings=load_settings()
    )


@app.route("/skills")
def skills_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "skills.html",
        skills=load_skills()
    )

@app.route("/soft-skills")
def soft_skills_page():

    if not session.get("admin"):

        return redirect("/login")

    return render_template(
        "soft_skills.html",
        soft_skills=load_soft_skills()
    )

@app.route("/extra-curricular")
def extra_curricular_page():

    if not session.get("admin"):

        return redirect("/login")

    return render_template(
        "extra_curricular.html",
        extra_curricular=load_extra_curricular()
    )

@app.route("/education")
def education_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "education.html",
        education=load_education()
    )


@app.route("/internships")
def internships_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "internships.html",
        internships=load_internships()
    )


@app.route("/projects")
def projects_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "projects.html",
        projects=load_projects()
    )

@app.route("/certificates")
def certificates_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "certificates.html",
        certificates=load_certificates()
    )

@app.route("/achievements")
def achievements_page():

    if not session.get("admin"):
        return redirect("/login")

    achievements = []

    if os.path.exists("achievements.json"):

        with open("achievements.json", "r") as file:

            try:
                achievements = json.load(file)

            except:
                achievements = []

    return render_template(
        "achievements.html",
        achievements=achievements
    )



@app.route("/create-project-page")
def create_project_page():

    if not session.get("admin"):
        return redirect("/login")

    return render_template(
        "create_project.html"
    )


# ==================================================
# UPDATE SETTINGS
# ==================================================

@app.route("/update-settings", methods=["POST"])
def update_settings():

    if not session.get("admin"):

        return redirect("/login")

    settings = {

        "hero_title":
        request.form.get("hero_title"),

        "hero_subtitle":
        request.form.get("hero_subtitle"),

        "about_text":
        request.form.get("about_text"),

        "email":
        request.form.get("email"),

        "phone":
        request.form.get("phone"),

        "github":
        request.form.get("github"),

        "linkedin":
        request.form.get("linkedin"),

        "resume":
        load_settings().get("resume", "")
    }

    save_settings(settings)

    return redirect("/admin")

# ==================================================
# UPLOAD RESUME
# ==================================================

@app.route("/upload-resume", methods=["POST"])
def upload_resume():

    if not session.get("admin"):

        return redirect("/login")

    file = request.files.get("resume")

    if file and file.filename != "":

        settings = load_settings()

        old_resume = settings.get("resume")

        if old_resume:

            old_path = os.path.join(
                "static",
                old_resume
            )

            if os.path.exists(old_path):

                os.remove(old_path)

        filename = secure_filename(
            file.filename
        )

        save_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        file.save(save_path)

        settings["resume"] = (
            f"uploads/{filename}"
        )

        save_settings(settings)

    return redirect("/admin")

@app.route("/download-resume")
def download_resume():

    settings = load_settings()

    if not settings.get("resume"):

        return redirect("/admin")

    path = os.path.join(
        "static",
        settings["resume"]
    )

    return send_file(
        path,
        as_attachment=True
    )


@app.route("/delete-resume")
def delete_resume():

    if not session.get("admin"):

        return redirect("/login")

    settings = load_settings()

    if settings.get("resume"):

        path = os.path.join(
            "static",
            settings["resume"]
        )

        if os.path.exists(path):

            os.remove(path)

    settings["resume"] = ""

    save_settings(settings)

    return redirect("/admin")

# ==================================================
# ADD SKILL
# ==================================================

@app.route("/add-skill", methods=["POST"])
def add_skill():

    if not session.get("admin"):

        return redirect("/login")

    skills = load_skills()

    skills.append({

        "name":
        request.form.get("name"),

        "level":
        request.form.get("level")
    })

    save_skills(skills)
    return redirect("/skills")


# ==================================================
# DELETE SKILL
# ==================================================

@app.route("/delete-skill/<name>")
def delete_skill(name):

    if not session.get("admin"):

        return redirect("/login")

    skills = load_skills()

    skills = [
        skill for skill in skills
        if skill["name"] != name
    ]

    save_skills(skills)

    return redirect("/skills")

# ==================================================
# SOFT SKILLS
# ==================================================

@app.route(
    "/add-soft-skill",
    methods=["POST"]
)
def add_soft_skill():

    if not session.get("admin"):

        return redirect("/login")

    soft_skills = load_soft_skills()

    soft_skills.append({

        "name":
        request.form.get("name")

    })

    save_soft_skills(soft_skills)

    return redirect("/soft-skills")

@app.route(
    "/delete-soft-skill/<int:index>"
)
def delete_soft_skill(index):

    if not session.get("admin"):

        return redirect("/login")

    soft_skills = load_soft_skills()

    if 0 <= index < len(soft_skills):

        soft_skills.pop(index)

        save_soft_skills(soft_skills)

    return redirect("/soft-skills")

@app.route(
    "/edit-soft-skill/<int:index>",
    methods=["GET", "POST"]
)
def edit_soft_skill(index):

    if not session.get("admin"):

        return redirect("/login")

    soft_skills = load_soft_skills()

    if index < 0 or index >= len(soft_skills):

        return redirect("/soft-skills")

    if request.method == "POST":

        soft_skills[index]["name"] = request.form.get(
            "name"
        )

        save_soft_skills(soft_skills)

        return redirect("/soft-skills")

    return render_template(
        "edit_soft_skill.html",
        skill=soft_skills[index],
        index=index
    )

@app.route(
    "/add-extra-curricular",
    methods=["POST"]
)
def add_extra_curricular():

    if not session.get("admin"):

        return redirect("/login")

    extra_curricular = load_extra_curricular()

    extra_curricular.append({

        "name":
        request.form.get("name")

    })

    save_extra_curricular(extra_curricular)

    return redirect("/extra-curricular")


@app.route(
    "/delete-extra-curricular/<int:index>"
)
def delete_extra_curricular(index):

    if not session.get("admin"):

        return redirect("/login")

    extra_curricular = load_extra_curricular()

    if 0 <= index < len(extra_curricular):

        extra_curricular.pop(index)

        save_extra_curricular(extra_curricular)

    return redirect("/extra-curricular")


@app.route(
    "/edit-extra-curricular/<int:index>",
    methods=["GET", "POST"]
)
def edit_extra_curricular(index):

    if not session.get("admin"):

        return redirect("/login")

    extra_curricular = load_extra_curricular()

    if index < 0 or index >= len(extra_curricular):

        return redirect("/extra-curricular")

    if request.method == "POST":

        extra_curricular[index]["name"] = request.form.get(
            "name"
        )

        save_extra_curricular(extra_curricular)

        return redirect("/extra-curricular")

    return render_template(
        "edit_extra_curricular.html",
        activity=extra_curricular[index],
        index=index
    )

# ==================================================
# ADD EDUCATION
# ==================================================

@app.route("/add-education", methods=["POST"])
def add_education():

    if not session.get("admin"):

        return redirect("/login")

    education = load_education()

    education.append({

    "qualification":
    request.form.get("qualification"),

    "institution":
    request.form.get("institution"),

    "duration":
    request.form.get("duration"),

    "result":
    request.form.get("result")

})

    save_education(education)

    return redirect("/education")


# ==================================================
# DELETE EDUCATION
# ==================================================

@app.route("/delete-education/<int:index>")
def delete_education(index):

    if not session.get("admin"):

        return redirect("/login")

    education = load_education()

    if 0 <= index < len(education):

        education.pop(index)

        save_education(education)

    return redirect("/education")


# ==================================================
# EDIT EDUCATION
# ==================================================

@app.route(
    "/edit-education/<int:index>",
    methods=["GET", "POST"]
)
def edit_education(index):

    if not session.get("admin"):

        return redirect("/login")

    education = load_education()

    if index < 0 or index >= len(education):

        return redirect("/education")

    if request.method == "POST":

       education[index]["qualification"] = request.form.get(
            "qualification"
        )
       education[index]["institution"] = request.form.get(
            "institution"
        )
       education[index]["duration"] = request.form.get(
            "duration"
        )
       education[index]["result"] = request.form.get(
            "result"
        )
       save_education(education)
       return redirect("/education")

    return render_template(
        "edit_education.html",
        education=education[index],
        index=index
    )
# ==================================================
# ADD INTERNSHIP
# ==================================================

@app.route(
    "/add-internship",
    methods=["POST"]
)
def add_internship():

    if not session.get("admin"):

        return redirect("/login")

    internships = load_internships()

    internships.append({

        "company":
        request.form.get("company"),

        "description":
        request.form.get("description")

    })

    save_internships(internships)

    return redirect("/internships")


# ==================================================
# DELETE INTERNSHIP
# ==================================================

@app.route("/delete-internship/<int:index>")
def delete_internship(index):

    if not session.get("admin"):

        return redirect("/login")

    internships = load_internships()

    if 0 <= index < len(internships):

        internships.pop(index)

        save_internships(internships)

    return redirect("/internships")


# ==================================================
# EDIT INTERNSHIP
# ==================================================

@app.route(
    "/edit-internship/<int:index>",
    methods=["GET", "POST"]
)
def edit_internship(index):

    if not session.get("admin"):

        return redirect("/login")

    internships = load_internships()

    if index < 0 or index >= len(internships):

        return redirect("/internships")

    if request.method == "POST":

        internships[index]["company"] = request.form.get(
            "company"
        )

        internships[index]["description"] = request.form.get(
            "description"
        )

        save_internships(internships)

        return redirect("/internships")

    return render_template(
        "edit_internship.html",
        internship=internships[index],
        index=index
    )
# ==================================================
# ADD ACHIEVEMENT
# ==================================================

@app.route("/add-achievement", methods=["POST"])
def add_achievement():

    if not session.get("admin"):
        return redirect("/login")

    if os.path.exists("achievements.json"):

        with open("achievements.json", "r") as file:

            try:
                achievements = json.load(file)

            except:
                achievements = []

    else:

        achievements = []

    achievements.append({

        "title": request.form["title"],

        "description": request.form["description"]

    })

    with open("achievements.json", "w") as file:

        json.dump(
            achievements,
            file,
            indent=4
        )

   
    return redirect("/achievements")

# ==================================================
# ADD CERTIFICATE
# ==================================================

@app.route(
    "/add-certificate",
    methods=["POST"]
)
def add_certificate():

    if not session.get("admin"):
        return redirect("/login")

    certificates = load_certificates()

    file = request.files.get("file")

    filename = ""

    if file and file.filename != "":

        filename = (
            str(int(datetime.now().timestamp()))
            + "_"
            + secure_filename(file.filename)
        )

        file.save(
            os.path.join(
                CERTIFICATE_FOLDER,
                filename
            )
        )

    certificates.append({

        "title":
        request.form.get("title"),

        "description":
        request.form.get("description"),

        "file":
        f"certificates/{filename}"

    })

    save_certificates(certificates)

    return redirect("/certificates")

# ==================================================
# EDIT CERTIFICATE
# ==================================================

@app.route(
    "/edit-certificate/<int:index>",
    methods=["GET", "POST"]
)
def edit_certificate(index):

    if not session.get("admin"):
        return redirect("/login")

    certificates = load_certificates()

    if index < 0 or index >= len(certificates):
        return redirect("/certificates")

    if request.method == "POST":

        certificates[index]["title"] = request.form.get(
            "title"
        )

        certificates[index]["description"] = request.form.get(
            "description"
        )

        file = request.files.get("file")

        if file and file.filename != "":

            old_file = certificates[index].get(
                "file",
                ""
            )

            if old_file:

                old_path = os.path.join(
                    "static",
                    old_file
                )

                if os.path.exists(old_path):

                    os.remove(old_path)

            filename = (
                str(int(datetime.now().timestamp()))
                + "_"
                + secure_filename(file.filename)
            )

            file.save(
                os.path.join(
                    CERTIFICATE_FOLDER,
                    filename
                )
            )

            certificates[index]["file"] = (
                f"certificates/{filename}"
            )

        save_certificates(certificates)

        return redirect("/certificates")

    return render_template(
        "edit_certificate.html",
        certificate=certificates[index]
    )

# ==================================================
# DELETE CERTIFICATE
# ==================================================

@app.route("/delete-certificate/<int:index>")
def delete_certificate(index):

    if not session.get("admin"):
        return redirect("/login")

    certificates = load_certificates()

    if 0 <= index < len(certificates):

        certificate = certificates[index]

        # Get file path
        file_path = certificate.get("file", "")

        # Delete uploaded file from static/certificates
        if file_path:

            full_path = os.path.join(
                "static",
                file_path
            )

            
            try:

                if os.path.exists(full_path):

                    os.remove(full_path)

            except Exception as e:

                print("FILE DELETE ERROR:", e)

        # Remove certificate from JSON
        certificates.pop(index)

        save_certificates(certificates)

    return redirect("/certificates")

# ==================================================
# CREATE PROJECT
# ==================================================

@app.route("/create-project", methods=["POST"])
def create_project():

    if not session.get("admin"):

        return redirect("/login")

    title = request.form.get("title")

    slug = secure_filename(
    title.lower()
)

    project_folder = os.path.join(
        PROJECTS_FOLDER,
        slug
    )

    os.makedirs(project_folder, exist_ok=True)

    
    project = {

        "title":
        title,

        "slug":
        slug,

        "short_description":
        request.form.get("short_description"),

        "full_description":
        request.form.get("full_description"),

        "category":
        request.form.get("category"),

        "year":
        request.form.get("year"),

        "tech_stack":
        [
            tech.strip()
            for tech in request.form.get(
                "tech_stack"
            ).split(",")
        ],

        "gallery":
        []

    }

    save_project(project)

    return redirect("/projects")


# ==================================================
# PROJECT PAGE
# ==================================================

@app.route("/project/<slug>")
def project_page(slug):

    projects = load_projects()

    project = next(

        (
            p for p in projects
            if p["slug"] == slug
        ),

        None
    )

    if not project:

        return "Project Not Found"

    return render_template(
        "project.html",
        project=project
    )


# ==================================================
# EDIT PROJECT
# ==================================================

@app.route(
    "/edit-project/<slug>",
    methods=["GET", "POST"]
)
def edit_project(slug):

    if not session.get("admin"):

        return redirect("/login")

    projects = load_projects()

    project = next(

        (
            p for p in projects
            if p["slug"] == slug
        ),

        None
    )

    if not project:

        return "Project Not Found"

    if request.method == "POST":

        project["title"] = request.form.get("title")

        project["short_description"] = request.form.get(
            "short_description"
        )

        project["full_description"] = request.form.get(
            "full_description"
        )

        project["category"] = request.form.get(
            "category"
        )

        project["year"] = request.form.get(
            "year"
        )

        project["tech_stack"] = [

            tech.strip()

            for tech in request.form.get(
                "tech_stack"
            ).split(",")
        ]

        save_project(project)

        return redirect("/projects")

    return render_template(
        "edit_project.html",
        project=project
    )


# ==================================================
# UPLOAD PROJECT IMAGES
# ==================================================

@app.route(
    "/upload-project-images/<slug>",
    methods=["POST"]
)
def upload_project_images(slug):

    if not session.get("admin"):
        return redirect("/login")

    project_folder = os.path.join(
        PROJECTS_FOLDER,
        slug
    )

    gallery_folder = os.path.join(
        project_folder,
        "gallery"
    )

    os.makedirs(
        gallery_folder,
        exist_ok=True
    )

    files = request.files.getlist(
        "images"
    )

    for file in files:

        if file.filename != "":

            filename = secure_filename(
                file.filename
            )

            save_path = os.path.join(
                gallery_folder,
                filename
            )

            file.save(save_path)

    return redirect(
        f"/edit-project/{slug}"
    )

# ==================================================
# DELETE PROJECT IMAGE
# ==================================================

@app.route(
    "/delete-project-image/<slug>/<filename>"
)
def delete_project_image(
    slug,
    filename
):

    if not session.get("admin"):
        return redirect("/login")

    image_path = os.path.join(
        PROJECTS_FOLDER,
        slug,
        "gallery",
        filename
    )

    if os.path.exists(image_path):

        os.remove(image_path)

    return redirect(
        f"/edit-project/{slug}"
    )


# ==================================================
# PROJECT GALLERY IMAGE
# ==================================================

@app.route(
    "/projects/<slug>/gallery/<filename>"
)
def project_gallery_image(
    slug,
    filename
):

    return send_from_directory(
        os.path.join(
            PROJECTS_FOLDER,
            slug,
            "gallery"
        ),
        filename
    )

# ==================================================
# EDIT SKILL
# ==================================================

@app.route(
    "/edit-skill/<int:index>",
    methods=["GET", "POST"]
)
def edit_skill(index):

    if not session.get("admin"):

        return redirect("/login")

    skills = load_skills()

    if index < 0 or index >= len(skills):

        return redirect("/skills")

    if request.method == "POST":

        skills[index]["name"] = request.form.get(
            "name"
        )

        skills[index]["level"] = int(
            request.form.get("level")
        )

        save_skills(skills)

        return redirect("/skills")

    return render_template(
        "edit_skill.html",
        skill=skills[index],
        index=index
    )

# ==================================================
# DELETE PROJECT
# ==================================================
@app.route("/delete-achievement/<int:index>")
def delete_achievement(index):

    if not session.get("admin"):
        return redirect("/login")

    with open("achievements.json", "r") as file:
        achievements = json.load(file)

    if 0 <= index < len(achievements):
        achievements.pop(index)

    with open("achievements.json", "w") as file:
        json.dump(
            achievements,
            file,
            indent=4
        )

    return redirect("/achievements")

@app.route(
    "/edit-achievement/<int:index>",
    methods=["GET", "POST"]
)
def edit_achievement(index):

    if not session.get("admin"):
        return redirect("/login")

    with open("achievements.json", "r") as file:
        achievements = json.load(file)

    if request.method == "POST":

        achievements[index]["title"] = request.form.get(
            "title"
        )

        achievements[index]["description"] = request.form.get(
            "description"
        )

        with open("achievements.json", "w") as file:

            json.dump(
                achievements,
                file,
                indent=4
            )

        return redirect("/achievements")

    return render_template(
        "edit_achievement.html",
        achievement=achievements[index]
    )

# ==================================================
# DELETE PROJECT
# ==================================================

@app.route("/delete-project/<slug>")
def delete_project(slug):

    if not session.get("admin"):
        return redirect("/login")

    project_folder = os.path.join(
        PROJECTS_FOLDER,
        slug
    )

    if os.path.exists(project_folder):

        shutil.rmtree(project_folder)

    return redirect("/projects")


@app.route("/visitor-count")
def visitor_count():

    return {
        "count": get_visitor_count()
    }



# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

