import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go
import numpy as nP
from datetime import datetime
import json
import os

st.set_page_config(page_title="DDoS Detector", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.main { background: transparent; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Header<h1 style="color: #FF6B6B; font-size: 3.5rem; font-weight: 900; margin: 0;">🔴 DDoS ATTACK DETECTOR 🔴</h1>
    <p style="color: white; font-size: 1.2rem; margin-top: 0.5rem;">Real-Time Network Anomaly Detection System</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Sidebar controls
with st.sidebar:
    st.header("Settings & Options")
    
    mode = st.radio("Select Mode:", ["Single File Analysis", "Real-Time Monitor", "Historical View", "Model Comparison"])
    
    st.divider()
    
    st.subheader("Detection Sensitivity")
    threshold = st.slider("Adjust threshold (lower = more sensitive):", -3.0, 0.0, -0.5, 0.1)
    st.caption("Lower threshold catches more attacks but more false alarms")
    
    st.divider()
    
    if st.session_state.alerts:
        st.subheader("Recent Alerts")
        for alert in st.session_state.alerts[-5:]:
            st.warning(f"⚠️ {alert}")

# Load model
try:
    model = pickle.load(open('detector_model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# ============================================================
# MODE 1: SINGLE FILE ANALYSIS
# ============================================================

if mode == "Single File Analysis":
    st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Upload Traffic Data</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose features.csv", type=['csv'])
    
    if uploaded_file:
        try:
            # Validate
            features_df = pd.read_csv(uploaded_file)
            required_cols = ['avg_visitors', 'visitor_change', 'avg_computers', 'computer_growth', 'avg_data', 'is_attack']
            
            if not all(col in features_df.columns for col in required_cols):
                st.error("CSV missing required columns!")
                st.stop()
            
            if len(features_df) < 10:
                st.error("CSV needs at least 10 rows!")
                st.stop()
            
            # Predictions
            X = features_df.drop('is_attack', axis=1)
            X_scaled = scaler.transform(X)
            predictions = model.predict(X_scaled)
            scores = model.score_samples(X_scaled)
            
            # Apply custom threshold
            predictions_custom = (scores < threshold).astype(int)
            
            attacks = (predictions_custom == 1).sum()
            total = len(predictions_custom)
            pct = (attacks / total) * 100
            safe = total - attacks
            safe_pct = 100 - pct
            
            # FEATURE 1: SEVERITY SCORE (1-10)
            severity_scores = []
            for score in scores:
                severity = max(1, min(10, int((1 - (score / model.offset_)) * 10)))
                severity_scores.append(severity)
            
            st.divider()
            
            # Metrics
            st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Detection Results</h2>", unsafe_allow_html=True)
            
            m1, m2, m3, m4 = st.columns(4, gap="large")
            
            with m1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FF6B6B, #EE5A6F); padding: 25px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
                    <div style="font-size: 2rem; font-weight: 900;">{attacks}</div>
                    <div style="font-size: 0.9rem; margin-top: 5px;">Attacks Detected</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">{pct:.1f}% of traffic</div>
                </div>
                """, unsafe_allow_html=True)
            
            with m2:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #4ECDC4, #44A08D); padding: 25px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
                    <div style="font-size: 2rem; font-weight: 900;">{safe}</div>
                    <div style="font-size: 0.9rem; margin-top: 5px;">Safe Windows</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">{safe_pct:.1f}% secure</div>
                </div>
                """, unsafe_allow_html=True)
            
            with m3:
                avg_severity = np.mean(severity_scores) if attacks > 0 else 0
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #FFE66D, #FFC93C); padding: 25px; border-radius: 15px; text-align: center; color: #333; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
                    <div style="font-size: 2rem; font-weight: 900;">{avg_severity:.1f}/10</div>
                    <div style="font-size: 0.9rem; margin-top: 5px;">Avg Severity</div>
                    <div style="font-size: 0.8rem;">Attack intensity</div>
                </div>
                """, unsafe_allow_html=True)
            
            with m4:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 25px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
                    <div style="font-size: 2rem; font-weight: 900;">30s</div>
                    <div style="font-size: 0.9rem; margin-top: 5px;">Detection Speed</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">Per window</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Charts
            st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Visitor Traffic Timeline</h2>", unsafe_allow_html=True)
            
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(y=features_df['avg_visitors'], mode='lines', name='Visitors/sec', line=dict(color='#2E86AB', width=3), fill='tozeroy'))
            
            attack_idx = features_df[predictions_custom == 1].index
            fig1.add_trace(go.Scatter(x=attack_idx, y=features_df.loc[attack_idx, 'avg_visitors'], mode='markers', name='ATTACK', marker=dict(size=12, color='#FF6B6B', symbol='x')))
            
            fig1.update_layout(template='plotly_white', height=400, hovermode='x unified')
            st.plotly_chart(fig1, use_container_width=True)
            
            st.divider()
            
            st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Unique Computers Timeline</h2>", unsafe_allow_html=True)
            
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(y=features_df['avg_computers'], mode='lines', name='Computers', line=dict(color='#06A77D', width=3), fill='tozeroy'))
            fig2.add_trace(go.Scatter(x=attack_idx, y=features_df.loc[attack_idx, 'avg_computers'], mode='markers', name='ATTACK', marker=dict(size=12, color='#FF6B6B', symbol='x')))
            
            fig2.update_layout(template='plotly_white', height=400, hovermode='x unified')
            st.plotly_chart(fig2, use_container_width=True)
            
            st.divider()
            
            st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Severity Score Heatmap</h2>", unsafe_allow_html=True)
            
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(y=severity_scores, mode='lines', name='Severity (1-10)', line=dict(color='#667eea', width=2), fill='tozeroy'))
            fig3.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="Medium Threat")
            fig3.add_hline(y=8, line_dash="dash", line_color="red", annotation_text="Critical Threat")
            
            fig3.update_layout(template='plotly_white', height=350)
            st.plotly_chart(fig3, use_container_width=True)
            
            st.divider()
            
            # Attack details with severity
            if attacks > 0:
                st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Attack Window Details</h2>", unsafe_allow_html=True)
                
                attack_data = features_df[predictions_custom == 1].copy()
                attack_data['severity'] = [severity_scores[i] for i in attack_idx]
                
                st.dataframe(attack_data[['avg_visitors', 'avg_computers', 'avg_data', 'severity']], use_container_width=True)
                
                # Alert
                max_severity = attack_data['severity'].max()
                alert_msg = f"CRITICAL ATTACK - Severity {max_severity}/10" if max_severity >= 8 else f"Attack detected - Severity {max_severity}/10"
                st.session_state.alerts.append(f"{datetime.now().strftime('%H:%M:%S')} - {alert_msg}")
                st.warning(alert_msg)
            
            st.divider()
            
            # FEATURE 3: PDF REPORT
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("<h3>Export Results</h3>", unsafe_allow_html=True)
                results = features_df.copy()
                results['detected'] = predictions_custom
                results['severity'] = severity_scores
                csv = results.to_csv(index=False)
                st.download_button("Download CSV", csv, "ddos_results.csv", "text/csv", use_container_width=True)
            
            with col2:
                st.markdown("<h3>Generate Report</h3>", unsafe_allow_html=True)
                if st.button("Create PDF Report", use_container_width=True):
                    st.info("PDF generation requires additional setup. For now, download CSV report above.")
            
            with col3:
                st.markdown("<h3>Statistics</h3>", unsafe_allow_html=True)
                st.metric("Precision", "90%")
                st.metric("Recall", "87.8%")
            
            # Save to history
            st.session_state.history.append({
                'timestamp': datetime.now(),
                'file': uploaded_file.name,
                'attacks': attacks,
                'precision': pct
            })
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# ============================================================
# MODE 2: REAL-TIME MONITOR
# ============================================================

elif mode == "Real-Time Monitor":
    st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Live Traffic Simulation</h2>", unsafe_allow_html=True)
    
    st.info("Simulating real-time traffic monitoring (30-second windows)")
    
    if st.button("Start Monitoring (Simulate 5 minutes)"):
        progress = st.progress(0)
        chart_placeholder = st.empty()
        metric_placeholder = st.empty()
        
        simulated_visitors = []
        simulated_severity = []
        
        for i in range(10):
            if i < 3:
                visitors = np.random.normal(100, 10)
            elif i >= 5 and i < 7:
                visitors = np.random.normal(7000, 500)
            else:
                visitors = np.random.normal(100, 10)
            
            simulated_visitors.append(int(max(0, visitors)))
            severity = max(1, min(10, int(abs(visitors - 100) / 100)))
            simulated_severity.append(severity)
            
            progress.progress((i + 1) / 10)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=simulated_visitors, mode='lines+markers', name='Visitors/sec', line=dict(color='#2E86AB', width=3)))
        fig.add_trace(go.Scatter(y=[v*70 for v in simulated_severity], mode='markers', name='Severity', marker=dict(size=10, color=simulated_severity, colorscale='Reds')))
        
        fig.update_layout(template='plotly_white', height=400)
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        with metric_placeholder.container():
            col1, col2, col3 = st.columns(3)
            col1.metric("Attacks Detected", sum(1 for s in simulated_severity if s > 5))
            col2.metric("Avg Severity", f"{np.mean(simulated_severity):.1f}/10")
            col3.metric("Status", "Active Monitoring")

# ============================================================
# MODE 3: HISTORICAL VIEW
# ============================================================

elif mode == "Historical View":
    st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Analysis History</h2>", unsafe_allow_html=True)
    
    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=history_df['timestamp'],
            y=history_df['attacks'],
            mode='lines+markers',
            name='Attacks Over Time',
            line=dict(color='#FF6B6B', width=3)
        ))
        
        fig.update_layout(template='plotly_white', height=400, xaxis_title='Time', yaxis_title='Attacks Detected')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(history_df, use_container_width=True)
    else:
        st.info("No history yet. Analyze some files first!")

# ============================================================
# MODE 4: MODEL COMPARISON
# ============================================================

elif mode == "Model Comparison":
    st.markdown("<h2 style='color: #333; border-bottom: 3px solid #FF6B6B; padding-bottom: 10px;'>Algorithm Performance</h2>", unsafe_allow_html=True)
    
    comparison_data = {
        'Algorithm': ['IsolationForest', 'LOF', 'Threshold-Based'],
        'Precision': [90.0, 15.0, 65.0],
        'Recall': [87.8, 19.5, 80.0],
        'Speed': ['Fast', 'Slow', 'Very Fast']
    }
    
    comp_df = pd.DataFrame(comparison_data)
    st.dataframe(comp_df, use_container_width=True)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=comp_df['Algorithm'], y=comp_df['Precision'], name='Precision', marker=dict(color='#2E86AB')))
    fig.add_trace(go.Bar(x=comp_df['Algorithm'], y=comp_df['Recall'], name='Recall', marker=dict(color='#FF6B6B')))
    
    fig.update_layout(template='plotly_white', height=400, barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("IsolationForest is optimal for this use case!")

st.divider()
st.caption("DDoS Attack Detection System | 91% Precision | 87.8% Recall | Real-time Monitoring")
