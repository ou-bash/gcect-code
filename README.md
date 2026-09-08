### GCECT - Academic Laboratory Assignments

This repository contains all my laboratory work, assignments, and academic codes for the **Government College of Engineering and Ceramic Technology (GCECT)**. 

### Repository Structure

text

├── 1st-semester-gcect/
│   ├── ADS/                  # Advanced Data Structures
│   │   └── ADS-Lab/
│   │       ├── assignment-1.py
│   │       └── ...
│   └── Syllabus/             # Academic curriculum copies
└── README.md

Use code with caution.

### Setup & Execution

### Prerequisites

Make sure you have Python 3 and pip installed on your Ubuntu system. 

bash

sudo apt update
sudo apt install python3 python3-pip python3-venv -y

Use code with caution.

### Installation

To prevent breaking system packages, it is recommended to run the scripts inside a Python virtual environment: 

1. **Create a virtual environment:** 

bash

python3 -m venv .venv

Use code with caution.
2. **Activate the environment:** 

bash

source .venv/bin/activate

Use code with caution.
3. **Install dependencies:** 

bash

pip install matplotlib numpy

Use code with caution.

### Running the Scripts

Navigate to the specific lab directory and execute the Python file: 

bash

cd 1st-semester-gcect/ADS/ADS-Lab
python3 assignment-1.py

Use code with caution.

### Git Workflow Guide (Quick Reference)

To add new assignments from a feature branch and merge them on GitHub: 

bash

# 1. Create a new branch for the assignment
git checkout -b ads-ass-1

# 2. Stage and commit changes
git add .
git commit -m "add: assignment-1 input and output"

# 3. Push the branch to GitHub
git push -u origin ads-ass-1

# 4. Open the Pull Request in your browser to merge
gh pr create --web

Use code with caution.
