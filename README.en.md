# Project: PDF Compression Web Service

### General Description
The goal of this project is to create a simple and fast web service for reducing PDF file sizes. The service helps people send large documents through platforms that have file size limits, such as **Gmail**.

### How it works
* **Backend:** FastAPI (Python).

* **Data Processing:** Ghostscript — a tool used to compress PDF files by changing their internal parts.

* **Frontend:** A simple web interface using pure HTML, CSS, and JavaScript. It also uses **Jinja2** to make the HTML pages dynamic.

* **Infrastructure:** **Docker** is used to make sure the app works exactly the same way on any computer.

### Tech Stack (Planned)
* **Language:** Python 3.11+.
* **Framework:** FastAPI.
* **System tools:** Ghostscript.
* **Setup:** Docker.
* **OS:** Fedora Linux (for building) and Docker images (for running).

### Planned Features
* **Drag-and-Drop** file upload.
* **Automatic cleanup:** The server will delete old files to keep user data private and save disk space.
