# ============================================================
# Student Performance Analysis
# Author: Pradeep Kumar
# Description: Analyzing student exam scores to identify
#              performance patterns and key influencing factors.
# Tools: Python, Pandas, Matplotlib, Seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. Create Sample Dataset ─────────────────────────────────
np.random.seed(7)
n = 400

data = {
    'Student_ID': range(1, n + 1),
    'Gender': np.random.choice(['Male', 'Female'], n, p=[0.48, 0.52]),
    'Study_Hours_Per_Day': np.round(np.random.uniform(0.5, 9, n), 1),
    'Attendance_Pct': np.random.randint(50, 100, n),
    'Parent_Education': np.random.choice(
        ['High School', 'Graduate', 'Post Graduate'], n, p=[0.35, 0.45, 0.20]
    ),
    'Internet_Access': np.random.choice(['Yes', 'No'], n, p=[0.75, 0.25]),
    'Extra_Coaching': np.random.choice(['Yes', 'No'], n, p=[0.4, 0.6]),
}

df = pd.DataFrame(data)

# Generate marks correlated with study hours & attendance
df['Math_Score'] = (
    df['Study_Hours_Per_Day'] * 5 +
    df['Attendance_Pct'] * 0.3 +
    np.random.normal(0, 8, n)
).clip(20, 100).round(1)

df['Science_Score'] = (
    df['Study_Hours_Per_Day'] * 4.5 +
    df['Attendance_Pct'] * 0.28 +
    np.random.normal(0, 9, n)
).clip(20, 100).round(1)

df['English_Score'] = (
    df['Study_Hours_Per_Day'] * 3.8 +
    df['Attendance_Pct'] * 0.32 +
    np.random.normal(0, 10, n)
).clip(20, 100).round(1)

df['Average_Score'] = df[['Math_Score', 'Science_Score', 'English_Score']].mean(axis=1).round(1)

# Grade
def assign_grade(score):
    if score >= 85: return 'A'
    elif score >= 70: return 'B'
    elif score >= 55: return 'C'
    elif score >= 40: return 'D'
    else: return 'F'

df['Grade'] = df['Average_Score'].apply(assign_grade)

# Introduce missing values
df.loc[np.random.choice(df.index, 10), 'Study_Hours_Per_Day'] = np.nan

# ── 2. Data Overview ─────────────────────────────────────────
print("=" * 55)
print("       STUDENT PERFORMANCE ANALYSIS REPORT")
print("=" * 55)

print("\n📋 Dataset Shape:", df.shape)
print("\n📋 First 5 Rows:")
print(df.head())

print("\n📋 Missing Values:")
print(df.isnull().sum())

# ── 3. Data Cleaning ─────────────────────────────────────────
df['Study_Hours_Per_Day'].fillna(df['Study_Hours_Per_Day'].median(), inplace=True)
print("\n🔧 Missing values filled. Remaining:", df.isnull().sum().sum())

# ── 4. Key Statistics ────────────────────────────────────────
print("\n📊 Score Summary:")
print(df[['Math_Score', 'Science_Score', 'English_Score', 'Average_Score']].describe().round(2))

print("\n📊 Grade Distribution:")
print(df['Grade'].value_counts())

pass_rate = (df['Average_Score'] >= 40).mean() * 100
print(f"\n✅ Overall Pass Rate: {pass_rate:.1f}%")
print(f"✅ Class Average Score: {df['Average_Score'].mean():.1f}")

# ── 5. Visualizations ────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Student Performance Analysis Dashboard', fontsize=16, fontweight='bold')

# Plot 1: Grade Distribution
grade_order = ['A', 'B', 'C', 'D', 'F']
grade_counts = df['Grade'].value_counts().reindex(grade_order)
colors = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336']
axes[0, 0].bar(grade_counts.index, grade_counts.values, color=colors, edgecolor='white', linewidth=1.5)
axes[0, 0].set_title('Grade Distribution', fontweight='bold')
axes[0, 0].set_xlabel('Grade')
axes[0, 0].set_ylabel('Number of Students')
for i, v in enumerate(grade_counts.values):
    axes[0, 0].text(i, v + 2, str(v), ha='center', fontweight='bold')

# Plot 2: Study Hours vs Average Score
axes[0, 1].scatter(df['Study_Hours_Per_Day'], df['Average_Score'],
                   alpha=0.5, color='#2196F3', s=30)
z = np.polyfit(df['Study_Hours_Per_Day'], df['Average_Score'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['Study_Hours_Per_Day'].min(), df['Study_Hours_Per_Day'].max(), 100)
axes[0, 1].plot(x_line, p(x_line), color='red', linewidth=2, label='Trend')
axes[0, 1].set_title('Study Hours vs Average Score', fontweight='bold')
axes[0, 1].set_xlabel('Study Hours Per Day')
axes[0, 1].set_ylabel('Average Score')
axes[0, 1].legend()
axes[0, 1].grid(alpha=0.3)

# Plot 3: Subject-wise Average Score by Gender
subject_gender = df.groupby('Gender')[['Math_Score', 'Science_Score', 'English_Score']].mean()
subject_gender.T.plot(kind='bar', ax=axes[1, 0], color=['#2196F3', '#E91E63'],
                      edgecolor='white', linewidth=1)
axes[1, 0].set_title('Subject Scores by Gender', fontweight='bold')
axes[1, 0].set_xlabel('Subject')
axes[1, 0].set_ylabel('Average Score')
axes[1, 0].set_xticklabels(['Math', 'Science', 'English'], rotation=0)
axes[1, 0].legend(title='Gender')
axes[1, 0].grid(axis='y', alpha=0.3)

# Plot 4: Attendance vs Average Score
axes[1, 1].scatter(df['Attendance_Pct'], df['Average_Score'],
                   alpha=0.5, color='#9C27B0', s=30)
axes[1, 1].set_title('Attendance % vs Average Score', fontweight='bold')
axes[1, 1].set_xlabel('Attendance (%)')
axes[1, 1].set_ylabel('Average Score')
axes[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('student_performance_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Chart saved as 'student_performance_analysis.png'")

# ── 6. Key Insights ──────────────────────────────────────────
corr_study = df['Study_Hours_Per_Day'].corr(df['Average_Score'])
corr_attend = df['Attendance_Pct'].corr(df['Average_Score'])
top_grade = df[df['Grade'] == 'A']['Study_Hours_Per_Day'].mean()

print("\n" + "=" * 55)
print("                  KEY INSIGHTS")
print("=" * 55)
print(f"  ✅ Study Hours vs Score Correlation : {corr_study:.2f}")
print(f"  ✅ Attendance vs Score Correlation  : {corr_attend:.2f}")
print(f"  ✅ Avg Study Hours (Grade A students): {top_grade:.1f} hrs/day")
print(f"  ✅ Overall Pass Rate                : {pass_rate:.1f}%")
print(f"  ✅ Class Average Score              : {df['Average_Score'].mean():.1f}/100")
print("=" * 55)
