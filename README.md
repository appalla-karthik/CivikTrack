# 📊 CivicTrack Analytics Dashboard

A responsive and visually clean analytics dashboard page for the **CivicTrack** civic issue tracking system. This page provides useful insights into user-reported issues via visualizations including line charts, bar graphs, and pie charts.

---

## 🚀 Features

- 📈 **Line Chart** — Issues reported over the past 6 months
- 📊 **Bar Chart** — Breakdown of issues by category
- 🥧 **Pie Chart** — Resolved vs Pending issues
- 📦 **Summary Cards** — Total, Resolved, Pending, and Anonymous issues
- 🎨 Fully responsive & Bootstrap 5 styled
- 🌙 Ready for Dark Mode toggle (CSS variable based)

---

## 📂 File Structure


---

## 📸 Screenshot

![Analytics Screenshot](./screenshot.png)

*(Replace with an actual screenshot of your analytics page)*

---

## 🔧 Technologies Used

- HTML5 + CSS3
- Bootstrap 5
- Chart.js (via CDN)
- JavaScript (Vanilla)

---

## 🛠️ Setup Instructions

1. Clone or download this repository.
2. Open `analytics.html` directly in the browser.
3. Or integrate into your **Django**/**React**/**MERN** project.

---

## ⚙️ Optional Django Integration

In your `views.py`:

```python
from django.shortcuts import render

def analytics_view(request):
    return render(request, 'analytics.html')
