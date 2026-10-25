# 🔎 GitHub Repository Analyzer

<p align="center">
  <strong>Discover. Explore. Analyze.</strong>
  <br>
  A Python desktop application for discovering GitHub repositories by programming language.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-1F6AA5?style=for-the-badge" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/API-GitHub_REST-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub REST API">
  <img src="https://img.shields.io/badge/Engine-Multithreading-orange?style=for-the-badge" alt="Multithreading">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License">
</p>

---



## 📌 Overview

**GitHub Repository Analyzer** is a Python-based desktop application that uses the GitHub REST API to discover and explore repositories based on programming language.

Built with CustomTkinter, the application provides a dark-themed graphical interface where users can select a programming language, choose a sorting method, retrieve repository results, and open repositories directly in their default web browser.

Instead of manually searching through GitHub, users can explore repository rankings through a single desktop interface.

## ✨ Features

- 🔎 **Language-Based Search** — Find repositories written in Python, JavaScript, Rust, and other programming languages.
- ⭐ **Sort by Stars** — Discover repositories with the highest star counts.
- 🍴 **Sort by Forks** — Explore repositories with the most forks.
- 🔄 **Recently Updated** — Find repositories ordered by recent activity.
- 📊 **Repository Details** — View repository names, descriptions, star counts, and fork counts.
- 🌐 **Direct Repository Access** — Open any result in your default web browser.
- 🎨 **Dark-Themed Interface** — A modern desktop UI with custom panels, borders, and scrollable result cards.
- 🧵 **Background Requests** — Fetch repository data in a background thread to help keep the interface responsive.
- ⚠️ **Error Handling** — Display messages for request timeouts, connection failures, HTTP errors, and GitHub API rate limits.
- ℹ️ **Built-In Help Window** — Access basic usage instructions from within the application.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| CustomTkinter | Desktop graphical interface |
| Requests | HTTP requests to the GitHub REST API |
| Threading | Background repository fetching |
| Webbrowser | Open repositories in the default browser |
| GitHub REST API | Retrieve repository search results |

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or newer recommended
- pip package manager
- Internet connection

### 1. Clone the Repository

```bash
git clone https://github.com/Rudra1725/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace `YOUR-REPOSITORY` with your actual GitHub repository name.

### 2. Install Dependencies

```bash
pip install customtkinter requests
```

The remaining modules used by the application are included in Python's standard library.

### 3. Run the Application

Save the source code as `main.py` and execute:

```bash
python main.py
```

## 📖 How to Use

1. Launch the application.
2. Enter a programming language in the **Language** field, such as `python`, `javascript`, or `rust`.
3. Select a sorting option: `stars`, `forks`, or `updated`.
4. Choose the desired repository count.
5. Click **Fetch Repositories**.
6. Browse the repository cards and review their descriptions, stars, and forks.
7. Click **Open Repo** to visit a repository in your default browser.

## ⚙️ How It Works

```text
       User Input
           |
           v
   Select Language
   Sort & Result Count
           |
           v
   Build GitHub API Query
           |
           v
    Send HTTP Request
           |
           v
    GitHub REST API
           |
           v
    Parse JSON Response
           |
           v
    Display Repository Cards
           |
           v
      Open Repository
      in Web Browser
```

## 🌐 API Integration

The application uses the GitHub repository search endpoint:

```text
https://api.github.com/search/repositories
```

The request includes the selected programming language, sorting method, descending order, and requested result count.

Example query:

```text
q=language:python&sort=stars&order=desc&per_page=15
```

The application processes the JSON response and extracts repository information, including:

- Full repository name
- Description
- Star count
- Fork count
- Repository URL

### API Rate Limits

Unauthenticated GitHub REST API requests are subject to rate limits. If the limit is reached, the application displays an error message explaining that requests have been restricted.

## 🧠 Concepts Demonstrated

- REST API integration
- HTTP requests and JSON parsing
- Desktop GUI development
- Background threading
- Event-driven programming
- Exception handling
- Dynamic UI rendering
- Opening external URLs with Python

## ⚠️ Limitations

- An active internet connection is required to retrieve repository results.
- GitHub API rate limits may restrict repeated searches.
- Results depend on GitHub's repository search response and selected filters.
- The application currently displays basic repository metadata rather than detailed analytics.
- The application does not currently use GitHub authentication or personal access tokens.

## 🔮 Future Improvements

- 🔐 Optional GitHub authentication for higher API rate limits.
- 🔍 Additional search filters for topics, minimum stars, and repository descriptions.
- 📈 Repository activity charts and statistics.
- 💾 Save search results as CSV or JSON.
- ⭐ Bookmark favorite repositories.
- 📋 Copy repository URLs directly from result cards.
- 🧰 Add input validation and improved loading indicators.

## 👨‍💻 Author

**Rudra1725**

GitHub: [github.com/Rudra1725](https://github.com/Rudra1725)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

⭐ If you find this project useful, consider starring the repository!
