# Sales Intelligence Platform

A Streamlit dashboard for sales data analysis and machine learning predictions.

## Features

- Interactive sales data visualization
- Machine learning predictions using Random Forest
- Responsive dashboard layout
- Professional styling and design

## Setup

### Prerequisites
- Python 3.8+
- pip or conda

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/AI-Engineer-Project.git
cd AI-Engineer-Project
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the App

```bash
streamlit run app/dashboard.py
```

The app will open at `http://localhost:8501`

## Deployment

This app is deployed on Streamlit Cloud. Visit the live version: [Your App URL]

## Project Structure

```
├── app/
│   └── dashboard.py          # Main Streamlit app
├── data/
│   └── sales_data.csv        # Sample sales data
├── notebooks/
│   └── 01_python_basics.ipynb # Analysis notebooks
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Technologies Used

- **Streamlit** - Web framework
- **Pandas** - Data manipulation
- **Scikit-learn** - Machine learning
- **Matplotlib & Seaborn** - Data visualization

## License

MIT License - feel free to use for personal and commercial projects.
