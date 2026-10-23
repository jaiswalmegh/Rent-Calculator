
# 🏠 NESTWISE | Shared Rent Calculator

A modern, dark-themed desktop application built with Python and CustomTkinter to simplify shared rent and household expense management.

## ✨ Features

- 👥 Add and remove household members
- 🏠 Track monthly rent and shared expenses
- ⚡ Manage electricity, water, internet, groceries, and other bills
- ⚖️ Split expenses equally among roommates
- 📊 Allocate costs using custom percentage shares
- 💰 Generate itemized payment breakdowns
- 📄 Export payment summaries to CSV
- 🛡️ Validate member names, expense amounts, and percentages
- 🌙 Modern dark-themed GUI
- 🔒 Local calculations without an external API or database

## 🛠️ Tech Stack

- Python
- CustomTkinter
- Tkinter
- CSV module
- Python Standard Library

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/jaiswalmegh/Rent-Calculator
cd YOUR_REPOSITORY_NAME
```

Replace the placeholders with your actual repository URL and folder name.

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

## 📁 Project Structure

```text
NESTWISE-Rent-Calculator/
├── main.py
├── requirements.txt
└── README.md
```

## 🚀 How to Use

1. Add the names of all household members.
2. Enter monthly rent, utilities, and other shared expenses.
3. Select Equal Split or Custom Percentages.
4. If using custom percentages, ensure the shares total 100%.
5. Click Calculate Household Share.
6. Review each member's itemized payment breakdown.
7. Export the results to a CSV file if needed.

## 🧮 Calculation Logic

**Equal Split**

Each member pays an equal portion of every expense.

**Custom Percentage Split**

Each member pays according to their configured percentage.

For example, if the household expenses total ₹20,000 and a member's share is 40%, their total contribution is ₹8,000.

## 🔐 Privacy

The application runs locally. It does not require account registration, a database, or an external API. CSV reports are saved only when the user chooses to export them.

## 🔮 Future Improvements

- Expense history and monthly comparisons
- Individual payment tracking
- Settlement recommendations
- Persistent storage using SQLite
- PDF report generation
- Windows executable packaging

## 👨‍💻 Author

Megh Jaiswal

Built with Python to make shared household budgeting simpler and more transparent.
