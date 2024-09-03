import matplotlib.pyplot as plt
import numpy as np

# Example data
names = ['Alice', 'Bob', 'Charlie', 'David', 'Emily']
age = [28, 24, 22, 31, 29]
salary = [60000, 55000, 45000, 70000, 62000]
career = ['Engineer', 'Analyst', 'Designer', 'Manager', 'Developer']

# 1. Bar Chart
plt.figure(figsize=(8, 5))
plt.bar(names, age)
plt.xlabel('Names')
plt.ylabel('Age')
plt.title('Age of Individuals')
plt.show()

# 2. Scatter Plot
plt.figure(figsize=(8, 5))
plt.scatter(age, salary)
plt.xlabel('Age')
plt.ylabel('Salary')
plt.title('Age vs. Salary')
plt.show()

# 3. Pie Chart
plt.figure(figsize=(6, 6))
plt.pie([salary[i] for i in range(len(names))], labels=names, autopct='%1.1f%%')
plt.title('Salary Distribution')
plt.show()

# 4. Line Chart
plt.figure(figsize=(8, 5))
plt.plot(names, salary, marker='o')
plt.xlabel('Names')
plt.ylabel('Salary')
plt.title('Salary of Individuals')
plt.xticks(rotation=45)
plt.show()

# 5. Box Plot
plt.figure(figsize=(8, 5))
plt.boxplot(salary)
plt.ylabel('Salary')
plt.title('Salary Distribution')
plt.show()

# 6. Histogram
plt.figure(figsize=(8, 5))
plt.hist(age, bins=5, edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Age Distribution')
plt.show()

# 7. Stacked Bar Chart
plt.figure(figsize=(8, 5))
plt.bar(names, salary, label='Salary')
plt.bar(names, age, label='Age', bottom=salary)
plt.xlabel('Names')
plt.ylabel('Values')
plt.title('Stacked Bar Chart')
plt.legend()
plt.show()
