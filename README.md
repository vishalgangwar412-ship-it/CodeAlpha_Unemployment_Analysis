# CodeAlpha - Unemployment Analysis with Python

## Task 2

This project follows the CodeAlpha Data Science Internship Task 2 requirements: data cleaning, exploration, unemployment-trend visualization, COVID-19-period analysis, pattern identification, and insights.

### Dataset

File: `Unemployment_Rate_upto_11_2020.csv`

The commonly used dataset contains Indian region/state unemployment observations for 2020, including:
- Date
- Estimated Unemployment Rate
- Estimated Employed
- Estimated Labour Participation Rate
- Region/zone information

The project automatically downloads the CSV the first time it is run, so the GitHub repository can remain lightweight.

### Technologies

- Python
- Pandas
- Matplotlib

### Run

```bash
pip install -r requirements.txt
python unemployment_analysis.py
```

### Generated files

```text
outputs/
├── analysis_summary.csv
├── regional_summary.csv
├── national_unemployment_trend.png
├── top_10_regions.png
├── covid_comparison.png
├── monthly_2020_pattern.png
└── unemployment_vs_labour_participation.png
```

### COVID analysis

For this project, observations before March 2020 are labelled `Pre-COVID`, while observations from April 2020 onward are labelled `COVID Period`. March 2020 is treated as a transition month.

This is a descriptive comparison, not a causal estimate of the pandemic's effect.

### Project structure

```text
CodeAlpha_Unemployment_Analysis/
├── unemployment_analysis.py
├── requirements.txt
├── README.md
├── .gitignore
└── outputs/
```

### Author

Vishal Gangwar

CodeAlpha Data Science Internship - Task 2
