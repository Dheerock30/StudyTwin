# StudyTwin
A data-driven, rule-based learning analytics system designed to act as a digital twin for student study patterns. Built for the RECURSION 2.0 Hackathon, StudyTwin replaces generic study planners by analyzing individual learning behaviors, tracking quiz performance, and automatically identifying weak topics to optimize revision time.

🚀 Features
Personalized Learning Profile: Aggregates study hours, focus ratings, and test scores to establish a dynamic digital footprint of student progress.

Automated Weak-Area Detection: Analyzes quiz performance via Python and SQL queries to pinpoint specific topics needing urgent revision.

Smart Recommendations: Generates targeted, actionable study insights based on performance gaps rather than rigid, one-size-fits-all schedules.

Interactive Dashboard: Built with Streamlit for a clean, responsive UI requiring zero frontend overhead.

🛠️ Tech Stack
Backend & Logic: Python

Database: SQLite / SQL

Interface: Streamlit

⚙️ Quick Start
Clone the repository:

Bash
git clone https://github.com/your-username/study-twin.git
cd study-twin
Install dependencies:

Bash
pip install streamlit pandas
Initialize the database and run the app:

Bash
streamlit run app.py
