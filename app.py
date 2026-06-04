from supabase_client import supabase
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
from datetime import datetime, date
from werkzeug.utils import secure_filename

load_dotenv()


app = Flask(__name__)



app.secret_key = os.getenv("SECRET_KEY")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")



# ==================================================
# SETTINGS
# ==================================================

def load_settings():

    try:

        result = (
            supabase
            .table("settings")
            .select("*")
            .execute()
        )

        settings = {}

        for row in result.data:

            settings[row["key"]] = row["value"]

        return settings

    except Exception as e:

        print(
            "SETTINGS LOAD ERROR:",
            e
        )

        return {}


def save_settings(settings):

    try:

        for key, value in settings.items():

            supabase.table(
                "settings"
            ).upsert({

                "key": key,
                "value": value

            }, on_conflict="key").execute()

    except Exception as e:

        print(
            "SAVE SETTINGS ERROR:",
            e
        )




# ==================================================
# SKILLS
# ==================================================

def load_skills():

    try:

        result = (
            supabase
            .table("skills")
            .select("*")
            .order("id")
            .execute()
        )

        return result.data

    except Exception as e:

        print(
            "SKILLS LOAD ERROR:",
            e
        )

        return []




# ==================================================
# SOFT SKILLS
# ==================================================

def load_soft_skills():

    try:

        result = (
            supabase
            .table("soft_skills")
            .select("*")
            .order("id")
            .execute()
        )

        return result.data

    except Exception as e:

        print("SOFT SKILLS LOAD ERROR:", e)

        return []




# ==================================================
# EXTRA CURRICULAR
# ==================================================

def load_extra_curricular():

    try:

        result = (
            supabase
            .table("extra_curricular")
            .select("*")
            .order("id")
            .execute()
        )

        return result.data

    except Exception as e:

        print(
            "EXTRA CURRICULAR LOAD ERROR:",
            e
        )

        return []




# ==================================================
# EDUCATION
# ==================================================

def load_education():

    try:

        result = (
            supabase
            .table("education")
            .select("*")
            .order("id")
            .execute()
        )

        return result.data

    except Exception as e:

        print(
            "EDUCATION LOAD ERROR:",
            e
        )

        return []




# ==================================================
# CERTIFICATES
# ==================================================

def load_certificates():

    try:

        result = (
            supabase
            .table("certificates")
            .select("*")
            .order("id")
            .execute()
        )

        certificates = result.data

        for cert in certificates:

            if cert.get("image_name"):

                cert["image_url"] = (
                    supabase.storage
                    .from_("certificate-files")
                    .get_public_url(
                        cert["image_name"]
                    )
                )

            else:

                cert["image_url"] = ""

        return certificates

    except Exception as e:

        print(
            "CERTIFICATES LOAD ERROR:",
            e
        )

        return []


# ==================================================
# INTERNSHIPS
# ==================================================

def load_internships():

    try:

        result = (
            supabase
            .table("internships")
            .select("*")
            .order("id")
            .execute()
        )

        return result.data

    except Exception as e:

        print(
            "INTERNSHIP LOAD ERROR:",
            e
        )

        return []

# ==================================================
# ACHIEVEMENTS
# ==================================================
def load_achievements():

    try:

        result = (
            supabase
            .table("achievements")
            .select("*")
            .order("id")
            .execute()
        )

        return result.data

    except Exception as e:

        print(
            "ACHIEVEMENTS LOAD ERROR:",
            e
        )

        return []

# ==================================================
# VISITOR COUNTER
# ==================================================

def get_visitor_count():

    try:

        result = (
            supabase
            .table("visitors")
            .select("total_visitors")
            .eq("id", 1)
            .single()
            .execute()
        )

        return result.data["total_visitors"]

    except Exception as e:

        print(
            "VISITOR COUNT ERROR:",
            e
        )

        return 0


def increment_visitor_count():

    try:

        today = date.today().isoformat()

        result = (
            supabase
            .table("visitors")
            .select("*")
            .eq("id", 1)
            .single()
            .execute()
        )

        data = result.data

        total = data["total_visitors"]
        today_count = data["today_visitors"]
        last_date = data["last_visit_date"]

        if str(last_date) != today:

            today_count = 0

        total += 1
        today_count += 1

        supabase.table(
            "visitors"
        ).update({

            "total_visitors": total,
            "today_visitors": today_count,
            "last_visit_date": today

        }).eq(
            "id",
            1
        ).execute()

        return total

    except Exception as e:

        print(
            "INCREMENT VISITOR ERROR:",
            e
        )

        return 0


def get_visitor_stats():

    try:

        result = (
            supabase
            .table("visitors")
            .select("*")
            .eq("id", 1)
            .single()
            .execute()
        )

        data = result.data

        return {

            "today":
            data["today_visitors"],

            "week":
            data["total_visitors"],

            "month":
            data["total_visitors"]

        }

    except Exception as e:

        print(
            "VISITOR STATS ERROR:",
            e
        )

        return {

            "today": 0,
            "week": 0,
            "month": 0

        }

# ==================================================
# PROJECTS
# ==================================================

def load_projects():

    try:

        result = (
            supabase
            .table("projects")
            .select("*")
            .order("id")
            .execute()
        )

        projects = result.data

        for project in projects:

            if project.get("tech_stack"):

                project["tech_stack"] = [
                    tech.strip()
                    for tech in project["tech_stack"].split(",")
                ]

            else:
                project["tech_stack"] = []

            gallery_result = (
                supabase
                .table("project_images")
                .select("*")
                .eq("project_id", project["id"])
                .execute()
            )

            gallery = []

            for image in gallery_result.data:

                image_url = (
                    supabase.storage
                    .from_("project-gallery")
                    .get_public_url(image["image_name"])
                )

                gallery.append(image_url)

            project["gallery"] = gallery

        return projects

    except Exception as e:

        print("PROJECT LOAD ERROR:", e)

        return []
    
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

    return render_template(
        "achievements.html",
        achievements=load_achievements()
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

    if file and file.filename:

        settings = load_settings()

        old_resume = settings.get("resume")

        if old_resume:

            try:

                supabase.storage \
                    .from_("resume-files") \
                    .remove([old_resume])

            except Exception as e:

                print(
                    "DELETE OLD RESUME ERROR:",
                    e
                )

        filename = (
            f"{int(datetime.now().timestamp())}_"
            f"{secure_filename(file.filename)}"
        )

        file_bytes = file.read()

        supabase.storage \
            .from_("resume-files") \
            .upload(
                filename,
                file_bytes,
                {
                    "content-type":
                    file.content_type
                }
            )

        settings["resume"] = filename

        save_settings(settings)

    return redirect("/admin")



@app.route("/download-resume")
def download_resume():

    settings = load_settings()

    filename = settings.get("resume")

    if not filename:

        return redirect("/admin")

    resume_url = (
        supabase.storage
        .from_("resume-files")
        .get_public_url(filename)
    )

    return redirect(resume_url)


@app.route("/delete-resume")
def delete_resume():

    if not session.get("admin"):
        return redirect("/login")

    settings = load_settings()

    filename = settings.get("resume")

    if filename:

        try:

            supabase.storage \
                .from_("resume-files") \
                .remove([filename])

        except Exception as e:

            print(
                "DELETE RESUME ERROR:",
                e
            )

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

    try:

        supabase.table("skills").insert({

            "name": request.form.get("name"),

            "level": int(
                request.form.get("level")
            )

        }).execute()

    except Exception as e:

        print(
            "ADD SKILL ERROR:",
            e
        )

    return redirect("/skills")

# ==================================================
# DELETE SKILL
# ==================================================

@app.route("/delete-skill/<name>")
def delete_skill(name):

    if not session.get("admin"):
        return redirect("/login")

    try:

        supabase.table("skills") \
            .delete() \
            .eq("name", name) \
            .execute()

    except Exception as e:

        print("DELETE SKILL ERROR:", e)

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

    try:

        supabase.table(
            "soft_skills"
        ).insert({

            "skill":
            request.form.get("name")

        }).execute()

    except Exception as e:

        print(
            "ADD SOFT SKILL ERROR:",
            e
        )

    return redirect("/soft-skills")

@app.route(
    "/delete-soft-skill/<int:index>"
)


def delete_soft_skill(index):

    if not session.get("admin"):

        return redirect("/login")

    skills = load_soft_skills()

    if 0 <= index < len(skills):

        try:

            supabase.table(
                "soft_skills"
            ).delete().eq(
                "id",
                skills[index]["id"]
            ).execute()

        except Exception as e:

            print(
                "DELETE SOFT SKILL ERROR:",
                e
            )

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

        try:

            supabase.table(
                "soft_skills"
            ).update({

                "skill":
                request.form.get("name")

            }).eq(

                "id",
                soft_skills[index]["id"]

            ).execute()

        except Exception as e:

            print(
                "EDIT SOFT SKILL ERROR:",
                e
            )

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

    try:

        supabase.table(
            "extra_curricular"
        ).insert({

            "name":
            request.form.get("name")

        }).execute()

    except Exception as e:

        print(
            "ADD EXTRA CURRICULAR ERROR:",
            e
        )

    return redirect("/extra-curricular")


@app.route(
    "/delete-extra-curricular/<int:index>"
)
def delete_extra_curricular(index):

    if not session.get("admin"):

        return redirect("/login")

    activities = load_extra_curricular()

    if 0 <= index < len(activities):

        try:

            supabase.table(
                "extra_curricular"
            ).delete().eq(
                "id",
                activities[index]["id"]
            ).execute()

        except Exception as e:

            print(
                "DELETE EXTRA CURRICULAR ERROR:",
                e
            )

    return redirect("/extra-curricular")


@app.route(
    "/edit-extra-curricular/<int:index>",
    methods=["GET", "POST"]
)
def edit_extra_curricular(index):

    if not session.get("admin"):

        return redirect("/login")

    activities = load_extra_curricular()

    if index < 0 or index >= len(activities):

        return redirect("/extra-curricular")

    if request.method == "POST":

        try:

            supabase.table(
                "extra_curricular"
            ).update({

                "name":
                request.form.get("name")

            }).eq(

                "id",
                activities[index]["id"]

            ).execute()

        except Exception as e:

            print(
                "EDIT EXTRA CURRICULAR ERROR:",
                e
            )

        return redirect("/extra-curricular")

    return render_template(
        "edit_extra_curricular.html",
        activity=activities[index],
        index=index
    )


# ==================================================
# ADD EDUCATION
# ==================================================
@app.route("/add-education", methods=["POST"])
def add_education():

    if not session.get("admin"):

        return redirect("/login")

    try:

        supabase.table(
            "education"
        ).insert({

            "degree":
            request.form.get("qualification"),

            "institution":
            request.form.get("institution"),

            "year":
            request.form.get("duration"),

            "cgpa":
            request.form.get("result")

        }).execute()

    except Exception as e:

        print(
            "ADD EDUCATION ERROR:",
            e
        )

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

        try:

            supabase.table(
                "education"
            ).delete().eq(
                "id",
                education[index]["id"]
            ).execute()

        except Exception as e:

            print(
                "DELETE EDUCATION ERROR:",
                e
            )

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

        try:

            supabase.table(
                "education"
            ).update({

                "degree": request.form.get("qualification"),
                "institution": request.form.get("institution"),
                "year": request.form.get("duration"),
                "cgpa": request.form.get("result")

            }).eq(
                "id",
                education[index]["id"]
            ).execute()

        except Exception as e:

            print("EDIT EDUCATION ERROR:", e)

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

    try:

        supabase.table(
            "internships"
        ).insert({

            "company":
            request.form.get("company"),

            "description":
            request.form.get("description")

        }).execute()

    except Exception as e:

        print(
            "ADD INTERNSHIP ERROR:",
            e
        )

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

        try:

            supabase.table(
                "internships"
            ).delete().eq(
                "id",
                internships[index]["id"]
            ).execute()

        except Exception as e:

            print(
                "DELETE INTERNSHIP ERROR:",
                e
            )

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

        try:

            supabase.table(
                "internships"
            ).update({

                "company":
                request.form.get("company"),

                "description":
                request.form.get("description")

            }).eq(

                "id",
                internships[index]["id"]

            ).execute()

        except Exception as e:

            print(
                "EDIT INTERNSHIP ERROR:",
                e
            )

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

    try:

        supabase.table(
            "achievements"
        ).insert({

            "title":
            request.form.get("title"),

            "description":
            request.form.get("description")

        }).execute()

    except Exception as e:

        print(
            "ADD ACHIEVEMENT ERROR:",
            e
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

    file = request.files.get("file")

    image_name = ""

    if file and file.filename:

        image_name = (
            f"{int(datetime.now().timestamp())}_"
            f"{secure_filename(file.filename)}"
        )

        file_bytes = file.read()

        supabase.storage \
            .from_("certificate-files") \
            .upload(
                image_name,
                file_bytes,
                {
                    "content-type":
                    file.content_type
                }
            )

    supabase.table(
        "certificates"
    ).insert({

        "title":
        request.form.get("title"),

        "description":
        request.form.get("description"),

        "image_name":
        image_name

    }).execute()

    return redirect("/certificates")

# ==================================================
# EDIT CERTIFICATE
# ==================================================
@app.route(
    "/edit-certificate/<int:certificate_id>",
    methods=["GET", "POST"]
)
def edit_certificate(certificate_id):

    if not session.get("admin"):
        return redirect("/login")

    certificates = load_certificates()

    certificate = next(
        (
            c for c in certificates
            if c["id"] == certificate_id
        ),
        None
    )

    if not certificate:
        return redirect("/certificates")

    if request.method == "POST":

        try:

            update_data = {

                "title":
                request.form.get("title"),

                "description":
                request.form.get("description")

            }

            file = request.files.get("file")

            if file and file.filename:

                if certificate.get("image_name"):

                    supabase.storage \
                        .from_("certificate-files") \
                        .remove([
                            certificate["image_name"]
                        ])

                image_name = (
                    f"{int(datetime.now().timestamp())}_"
                    f"{secure_filename(file.filename)}"
                )

                file_bytes = file.read()

                supabase.storage \
                    .from_("certificate-files") \
                    .upload(
                        image_name,
                        file_bytes,
                        {
                            "content-type":
                            file.content_type
                        }
                    )

                update_data["image_name"] = image_name

            supabase.table(
                "certificates"
            ).update(
                update_data
            ).eq(
                "id",
                certificate_id
            ).execute()

        except Exception as e:

            print(
                "EDIT CERTIFICATE ERROR:",
                e
            )

        return redirect("/certificates")

    return render_template(
        "edit_certificate.html",
        certificate=certificate
    )


# ==================================================
# DELETE CERTIFICATE IMAGE
# ==================================================

@app.route(
    "/delete-certificate-image/<int:certificate_id>"
)
def delete_certificate_image(certificate_id):

    if not session.get("admin"):
        return redirect("/login")

    try:

        result = (
            supabase
            .table("certificates")
            .select("*")
            .eq("id", certificate_id)
            .single()
            .execute()
        )

        certificate = result.data

        if certificate and certificate.get("image_name"):

            filename = certificate["image_name"]

            supabase.storage \
                .from_("certificate-files") \
                .remove([filename])

            supabase.table(
                "certificates"
            ).update({

                "image_name": ""

            }).eq(
                "id",
                certificate_id
            ).execute()

    except Exception as e:

        print(
            "DELETE CERTIFICATE IMAGE ERROR:",
            e
        )

    return redirect(
        f"/edit-certificate/{certificate_id}"
    )


# ==================================================
# DELETE CERTIFICATE
# ==================================================
@app.route("/delete-certificate/<int:certificate_id>")
def delete_certificate(certificate_id):

    if not session.get("admin"):
        return redirect("/login")

    try:

        print("Deleting certificate:", certificate_id)

        result = (
            supabase
            .table("certificates")
            .select("*")
            .eq("id", certificate_id)
            .execute()
        )

        print("Result:", result.data)

        if result.data:

            certificate = result.data[0]

            if certificate.get("image_name"):

                print(
                    "Deleting image:",
                    certificate["image_name"]
                )

                supabase.storage \
                    .from_("certificate-files") \
                    .remove([
                        certificate["image_name"]
                    ])

        supabase.table(
            "certificates"
        ).delete().eq(
            "id",
            certificate_id
        ).execute()

        print("Certificate deleted")

    except Exception as e:

        print(
            "DELETE CERTIFICATE ERROR:",
            str(e)
        )

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

    try:

        supabase.table(
            "projects"
        ).insert({

            "title":
            title,

            "slug":
            slug,

            "short_description":
            request.form.get(
                "short_description"
            ),

            "full_description":
            request.form.get(
                "full_description"
            ),

            "category":
            request.form.get(
                "category"
            ),

            "year":
            request.form.get(
                "year"
            ),

            "tech_stack":
            request.form.get(
                "tech_stack"
            )

        }).execute()

    except Exception as e:

        print(
            "CREATE PROJECT ERROR:",
            e
        )

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

        try:

            supabase.table(
                "projects"
            ).update({

                "title":
                request.form.get("title"),

                "short_description":
                request.form.get(
                    "short_description"
                ),

                "full_description":
                request.form.get(
                    "full_description"
                ),

                "category":
                request.form.get(
                    "category"
                ),

                "year":
                request.form.get(
                    "year"
                ),

                "tech_stack":
                request.form.get(
                    "tech_stack"
                )

            }).eq(

                "id",
                project["id"]

            ).execute()

        except Exception as e:

            print(
                "EDIT PROJECT ERROR:",
                e
            )

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

    projects = load_projects()

    project = next(
        (
            p for p in projects
            if p["slug"] == slug
        ),
        None
    )

    if not project:
        return redirect("/projects")

    files = request.files.getlist("images")

    for file in files:

        if file and file.filename:

            filename = (
                f"{project['id']}_"
                f"{int(datetime.now().timestamp())}_"
                f"{secure_filename(file.filename)}"
            )

            file_bytes = file.read()

            supabase.storage \
                .from_("project-gallery") \
                .upload(
                    filename,
                    file_bytes,
                    {"content-type": file.content_type}
                )

            supabase.table(
                "project_images"
            ).insert({

                "project_id": project["id"],
                "image_name": filename

            }).execute()

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

    try:

        supabase.storage \
            .from_("project-gallery") \
            .remove([filename])

        supabase.table(
            "project_images"
        ).delete().eq(
            "image_name",
            filename
        ).execute()

    except Exception as e:

        print(
            "DELETE IMAGE ERROR:",
            e
        )

    return redirect(
        f"/edit-project/{slug}"
    )

# ==================================================
# PROJECT GALLERY IMAGE
# ==================================================


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

    skill = skills[index]

    if request.method == "POST":

        try:

            supabase.table("skills").update({

                "name": request.form.get("name"),

                "level": int(
                    request.form.get("level")
                )

            }).eq(
                "id",
                skill["id"]
            ).execute()

        except Exception as e:

            print(
                "EDIT SKILL ERROR:",
                e
            )

        return redirect("/skills")

    return render_template(
        "edit_skill.html",
        skill=skill,
        index=index
    )

# ==================================================
# DELETE PROJECT
# ==================================================
@app.route("/delete-achievement/<int:index>")
def delete_achievement(index):

    if not session.get("admin"):
        return redirect("/login")

    achievements = load_achievements()

    if 0 <= index < len(achievements):

        try:

            supabase.table(
                "achievements"
            ).delete().eq(

                "id",
                achievements[index]["id"]

            ).execute()

        except Exception as e:

            print(
                "DELETE ACHIEVEMENT ERROR:",
                e
            )

    return redirect("/achievements")

@app.route(
    "/edit-achievement/<int:index>",
    methods=["GET", "POST"]
)
def edit_achievement(index):

    if not session.get("admin"):
        return redirect("/login")

    achievements = load_achievements()

    if index < 0 or index >= len(achievements):
        return redirect("/achievements")

    if request.method == "POST":

        try:

            supabase.table(
                "achievements"
            ).update({

                "title":
                request.form.get("title"),

                "description":
                request.form.get("description")

            }).eq(

                "id",
                achievements[index]["id"]

            ).execute()

        except Exception as e:

            print(
                "EDIT ACHIEVEMENT ERROR:",
                e
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

    try:

        supabase.table(
            "projects"
        ).delete().eq(
            "slug",
            slug
        ).execute()

    except Exception as e:

        print(
            "DELETE PROJECT ERROR:",
            e
        )

    return redirect("/projects")

# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )

