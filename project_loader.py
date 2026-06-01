import os
import json

PROJECTS_FOLDER = "projects"

def load_projects():

    projects = []

    if not os.path.exists(PROJECTS_FOLDER):

        return projects

    for folder in os.listdir(PROJECTS_FOLDER):

        project_path = os.path.join(
            PROJECTS_FOLDER,
            folder
        )

        if os.path.isdir(project_path):

            json_path = os.path.join(
                project_path,
                "project.json"
            )

            if os.path.isfile(json_path):

                try:

                    with open(json_path, "r") as file:

                        project = json.load(file)

                        projects.append(project)

                except Exception as e:

                    print(e)

    return projects