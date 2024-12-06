import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure database
# SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = './static/uploads'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create the Project model


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'


# Create the database (if it doesn't already exist)
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/omgwtf')
def omgwtf():
    return render_template('egg.html')


@app.route('/gallery')
def gallery():
    projects = Project.query.all()  # Fetch all projects from the database
    return render_template('gallery.html', projects=projects)


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['image']

        # Validate inputs
        if title and description and file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Save project to the database
            new_project = Project(
                title=title, description=description, image=filename)
            db.session.add(new_project)
            db.session.commit()

            # Redirect to the gallery page after successful creation
            return redirect(url_for('gallery'))
        else:
            return 'Please fill in all fields and upload an image.'

    return render_template('create_project.html')


@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        if 'image' in request.files:
            file = request.files['image']
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                project.image = filename

        db.session.commit()
        return redirect(url_for('gallery'))

    return render_template('edit_project.html', project=project)


@app.route('/delete_project/<int:project_id>', methods=['GET'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    # Delete the image file from the server (optional)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], project.image))

    # Delete the project from the database
    db.session.delete(project)
    db.session.commit()

    return redirect(url_for('gallery'))


if __name__ == '__main__':
    app.run(debug=True)
