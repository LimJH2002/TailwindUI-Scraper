# 🎨 Tailwind UI Component Scraper

A Python-based web scraper designed to automatically extract and organize components from Tailwind UI. This tool preserves the original site structure and saves React components in a hierarchical folder system.

## ✨ Features

- 🔑 Automatic login to Tailwind UI
- 🏗️ Maintains original site structure (Marketing, Application UI, Ecommerce)
- 📥 Extracts React component code
- 📁 Creates organized folder hierarchy
- 💾 Saves component code in JSX files
- 📝 Generates a structured index of all components

## 📂 Folder Structure

The scraper creates a hierarchical folder structure:

```
components/
├── Marketing/
│   ├── Page Sections/
│   │   ├── Hero Sections/
│   │   │   ├── SimpleHero.jsx
│   │   │   └── ...
│   │   └── ...
│   └── ...
├── Application UI/
└── Ecommerce/
```

## 📋 Prerequisites

- 🐍 Python 3.8 or higher
- 🌐 Chrome browser
- 🚗 ChromeDriver
- 🔐 Tailwind UI account

## 🚀 Installation

1. Clone the repository:

```bash
git clone <your-repository-url>
cd tailwind-ui-scraper
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   Create a `.env` file in the project root:

```env
TAILWIND_UI_EMAIL=your-email@example.com
TAILWIND_UI_PASSWORD=your-password
```

## 🛠️ Usage

1. Run the main script:

```bash
python components.py
```

The script will:

1. 🔑 Log in to Tailwind UI
2. 📄 Generate a structured index in `tailwind_components_structure.txt`
3. 🔍 Visit each component page
4. 📥 Extract React component code
5. 💾 Save components in their respective folders

## 🔧 Script Structure

- 🗺️ `get_component_structure()`: Creates initial site structure map
- 📝 `save_structure_to_file()`: Saves structure to text file
- 🌐 `visit_component_urls()`: Visits each component URL
- 📤 `get_component_code()`: Extracts component code
- 🔐 `login()`: Handles Tailwind UI authentication

## ⚠️ Error Handling

The script includes error handling for:

- 🌐 Network timeouts
- 🔍 Missing elements
- 🔒 Authentication issues
- 📁 File system operations

## 📝 Notes

- ✅ The script respects Tailwind UI's structure
- 🔄 Components are saved with sanitized filenames
- 📄 Each component gets its own JSX file
- 📊 Progress is logged to console

## ⚖️ Disclaimer

This tool is for educational purposes. Ensure you have proper authorization and comply with Tailwind UI's terms of service when using this scraper.
