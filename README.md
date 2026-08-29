\# DDoS Attack Detection System



I built a machine learning system that detects DDoS attacks in real-time. This is what it does.



\## The Problem



Websites get hit with massive bot traffic. Thousands of fake requests per second. Server crashes. Users can't access anything. Company loses money and reputation.



Old solution: Set a threshold like "alert if traffic > 5000 requests/sec". Problem? Black Friday happens. Legitimate traffic spikes. False alarm. Useless.



My solution: Train a model on normal traffic patterns. Then flag when things deviate. That's it.



\## What I Built



Anomaly detection using IsolationForest. Analyzes 30-second windows of network traffic. Extracts 5 smart features. If they all spike together = attack.



\*\*Performance:\*\* 90% precision, 87.8% recall. Translation: when I flag it as attack, 90% chance it's real. I catch 88% of actual attacks.



\## 8 Features I Added



1\. \*\*Severity Scoring\*\* - Rate attacks 1-10 instead of just yes/no

2\. \*\*Adjustable Threshold\*\* - Slider to tune sensitivity

3\. \*\*Real-time Monitor\*\* - Live traffic simulation 

4\. \*\*Historical Tracking\*\* - See past analyses

5\. \*\*Model Comparison\*\* - Why IsolationForest wins

6\. \*\*Alert System\*\* - Get notified when attacks happen

7\. \*\*CSV Export\*\* - Download results

8\. \*\*Report Generation\*\* - Create analysis reports



\## Results



| Metric | Score |

|--------|-------|

| Precision | 90.0% |

| Recall | 87.8% |

| False Alarms | 8 per 1000 windows |

| Detection Speed | 30 seconds |



\## How to Use



```bash

git clone https://github.com/Kans1505/ddos-detector.git

cd ddos-detector

py -m pip install -r requirements.txt

py -m streamlit run app.py

```



Upload your traffic CSV. System analyzes it. Shows you attacks, severity scores, and visualizations.



\## How It Actually Works



I trained the model on 1 hour of normal website traffic (100 visitors/sec, 50 unique IPs). Then injected 5 minutes of fake DDoS attack (7000 visitors/sec from 15,000 different bot IPs). Model learned to distinguish between them.



\*\*The 5 features I engineered:\*\*

\- \*\*avg\_visitors\*\* - Average traffic per window

\- \*\*visitor\_change\*\* - How volatile (max - min)

\- \*\*avg\_computers\*\* - Number of unique IP sources

\- \*\*computer\_growth\*\* - How many NEW IPs suddenly connected

\- \*\*avg\_data\*\* - Volume of data being transferred



When ALL of these spike at the same time = not legitimate users, that's an attack.



\## Why Anomaly Detection?



DDoS attacks are rare (\~1% of traffic). Classification algorithms need balanced data (50/50 normal/attack). Anomaly detection handles imbalanced data and catches novel attack patterns we haven't trained on.



\## What It CANNOT Do



\- Doesn't catch slow/gradual DDoS (my model looks at 30-sec snapshots)

\- Can't detect encrypted attacks (only sees traffic patterns)

\- Works for HTTP traffic only (not DNS/UDP attacks)

\- Trained on traditional volumetric DDoS (not sophisticated attacks)



\## Tech Stack



\- Python 3.14

\- scikit-learn (IsolationForest)

\- Streamlit (UI)

\- Plotly (charts)

\- Pandas/NumPy (data processing)



\## What I Learned



\- Feature engineering is 80% of machine learning

\- Precision-recall tradeoff is real (catch everything = more false alarms)

\- Anomaly detection beats classification for rare events

\- Time-series features matter (velocity, acceleration, growth)



\## Next Steps



\- Deploy to Streamlit Cloud (live URL)

\- Add API endpoint for automation

\- Real-time database logging

\- Email alert integration

\- Build admin dashboard



\## About Me



3rd year BTech Computer Science student @ IILM University, AI/ML specialization. I build actual working projects, not just theory.



\*\*Links:\*\*

\- GitHub: \[Kans1505](https://github.com/Kans1505)

\- LinkedIn: \[kanishka-nandini](https://linkedin.com/in/kanishka-nandini)



\## Questions?



Open an issue on GitHub or message me on LinkedIn. I enjoy discussing ML and security stuff.



\---



This project shows I can: engineer features from raw data, train models, understand precision-recall tradeoffs, build UIs, and actually ship working code.

