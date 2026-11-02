# 📰 TechNews Scraper & Aggregator

A clean, modular Python project that scrapes the latest tech headlines from [Hacker News](https://news.ycombinator.com/), displays them in a terminal table, and saves them to a JSON file.

[🇹🇷 Türkçe README için tıklayın](./README_tr.md)

---

## 🚀 Features
- **Modular Architecture:** Scraper, storage, and display logic are completely decoupled.
- **Robust Error Handling:** Built with retries and graceful degradation (never crashes on a bad network or row).
- **Rich Output:** Clean terminal table display using `rich`.
- **JSON Persistence:** Automatically saves results locally with timestamps.

---

## 💡 Note on AI & Learning
This is a simple project built with the assistance of AI, primarily designed as a first step into software development and GitHub. In today's AI-driven world, writing code is easy, but the true value lies in reading, understanding, reviewing, and debugging it. If this project helps you grasp the underlying logic rather than just running the code, it has fulfilled its purpose. :) Thanks!

---


## 📄 License

This project is released under the MIT License. Feel free to use it as a
learning reference or a starting point for your own scraping projects.

---

## ⚙️ Quick Start

```bash
# Clone the repository
git clone [https://github.com/](https://github.com/)<your-username>/technews-scraper.git
cd technews-scraper

# Create virtual environment & install dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run the app
python -m src