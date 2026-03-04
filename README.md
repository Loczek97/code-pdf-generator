# Code PDF Generator

A premium application to convert source code files into professional, syntax-highlighted PDF documents. Features automatic language detection and AI-powered code descriptions.

## Features

- 📂 **Multi-file Import**: Drag & Drop or Paste multiple code snippets.
- 🎨 **Syntax Highlighting**: Automatic language detection and coloring (using Pygments).
- 🤖 **AI Descriptions**: Optional AI summary of what the code does (Simulated for demo).
- 🌓 **Dark/Light Mode**: Premium UI with theme switching.
- 📄 **PDF Generation**: Generates clean, printable PDFs.

## Setup & Installation

### Prerequisites
- Python 3.8+
- `pip`
- GTK/Pango libraries (required by WeasyPrint for PDF generation).
  - Ubuntu/Debian: `sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`
  - MacOS: `brew install pango`

### Installation

**Note for Linux Users**: Modern Linux distributions (Debian 12+, Ubuntu 23.04+) enforce PEP 668, which requires virtual environments for Python packages.

1.  Clone the repository.
2.  Install the virtual environment package (if missing):
    ```bash
    sudo apt install python3-venv
    ```
3.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  Start the backend server (ensure venv is active):
    ```bash
    uvicorn backend.main:app --reload
    ```
    (Or run `python3 backend/main.py`)

2.  Open the application in your browser:
    The API runs at `http://localhost:8000`.
    
    Since the frontend is currently served statically or can be opened directly:
    - You can simply open `frontend/index.html` in your browser (though API calls might need CORS enabled or serving from the same origin).
    - **Recommended**: Serve the frontend. You can use Python's built-in server for the frontend folder:
      ```bash
      cd frontend
      python3 -m http.server 3000
      ```
      Then visit `http://localhost:3000`.

## Project Structure

- `backend/`: FastAPI application, PDF generation logic.
- `frontend/`: HTML/CSS/JS for the user interface.

## Notes
- The AI description feature is currently mocked for demonstration. To enable real AI, update `backend/services/ai_service.py` with an actual API call (e.g., OpenAI).
