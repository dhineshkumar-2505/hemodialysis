import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import time

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load custom CSS
local_css("style.css")

# App title and header
st.markdown("""
<div class="header">
    <h1>🧡 Hemodialysis Machine Troubleshooting Assistant</h1>
    <p class="subheader">AI-powered diagnostic support for biomedical engineers</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation and info
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913108.png", width=100)
    st.markdown("""
    <div class="sidebar-section">
        <h3>About This Tool</h3>
        <p>This AI assistant helps biomedical technicians quickly diagnose and resolve issues with hemodialysis machines.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3>How to Use</h3>
        <ol>
            <li>Select the machine state</li>
            <li>Choose the specific alarm/issue</li>
            <li>Follow the guided steps</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3>Emergency Contact</h3>
        <p>For critical issues, contact:<br>
        <strong>Biomedical Support:</strong> +1 (555) 123-4567</p>
    </div>
    """, unsafe_allow_html=True)

# Function to load Excel data
@st.cache_data
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    data_dict = {}
    
    for sheet in sheet_names:
        if sheet == "States":  # Skip the States sheet
            continue
        df = pd.read_excel(xls, sheet_name=sheet, header=0)
        # Clean up column names
        df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
        # Drop empty rows
        df = df.dropna(how='all')
        data_dict[sheet] = df
    
    return data_dict, sheet_names

# Function to get all alarms from a sheet
def get_alarms_for_sheet(df):
    alarms = df['Alarms / Reasons'].dropna().unique().tolist()
    issues = df[df['Alarms / Reasons'] == 'Issues'].index
    if len(issues) > 0:
        issue_start = issues[0] + 1
        additional_issues = df.iloc[issue_start:]['Alarms / Reasons'].dropna().unique().tolist()
        alarms.extend(additional_issues)
    return [a for a in alarms if a != 'Issues' and str(a) != 'nan']

# Main app function
def main():
    # Default Excel file path
    file_path = "MachineDataAnalytics.xlsx"
    
    try:
        data_dict, sheet_names = load_data(file_path)
        
        # Remove 'States' from sheet names if present
        sheet_names = [s for s in sheet_names if s != "States"]
        
        # State selection
        st.markdown("### 1️⃣ Select Machine State")
        selected_sheet = st.selectbox(
            "Choose the current machine state:",
            sheet_names,
            index=0,
            key="sheet_select"
        )
        
        # Get alarms for selected sheet
        df = data_dict[selected_sheet]
        alarms = get_alarms_for_sheet(df)
        
        if not alarms:
            st.warning("No alarm data found for this state.")
            return
            
        # Alarm selection
        st.markdown("### 2️⃣ Select Alarm/Issue")
        selected_alarm = st.selectbox(
            "Choose the alarm or issue you're troubleshooting:",
            alarms,
            index=0,
            key="alarm_select"
        )
        
        # Find the row with the selected alarm
        alarm_row = df[df['Alarms / Reasons'] == selected_alarm]
        
        if alarm_row.empty:
            # Check if it's in the issues section
            issues_section = df[df['Alarms / Reasons'] == 'Issues']
            if not issues_section.empty:
                issue_start = issues_section.index[0] + 1
                issue_rows = df.iloc[issue_start:]
                alarm_row = issue_rows[issue_rows['Alarms / Reasons'] == selected_alarm]
        
        if alarm_row.empty:
            st.error("No troubleshooting information found for this alarm.")
            return
            
        # Display troubleshooting steps
        st.markdown("### 3️⃣ Troubleshooting Steps")
        
        # Create a glowing box for the alarm name
        st.markdown(f"""
        <div class="glowing-box">
            <div class="glow"></div>
            <div class="content">
                <h3>{selected_alarm}</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Get all reasons (steps)
        reasons = []
        for i in range(1, 11):
            reason_col = f"Reason {i}"
            if reason_col in alarm_row.columns:
                reason = alarm_row[reason_col].values[0]
                if pd.notna(reason):
                    reasons.append(reason)
        
        if not reasons:
            st.info("No specific troubleshooting steps documented for this alarm.")
        else:
            for i, reason in enumerate(reasons, 1):
                # Animate the appearance of each step
                with st.empty():
                    time.sleep(0.3)  # Small delay for animation effect
                    st.markdown(f"""
                    <div class="step-box animated-step">
                        <div class="step-number">Step {i}</div>
                        <div class="step-content">{reason}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Add some spacing
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Additional notes section
            st.markdown("### 📝 Additional Notes")
            st.markdown("""
            <div class="notes-box animated-notes">
                <ul>
                    <li>Always follow hospital safety protocols</li>
                    <li>Wear appropriate PPE when handling machines</li>
                    <li>Document all maintenance actions</li>
                    <li>Report unresolved issues to biomedical engineering department</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a completion check
            st.markdown("---")
            resolved = st.radio("Did this resolve your issue?", ("Still troubleshooting", "Issue resolved"), index=0)
            if resolved == "Issue resolved":
                st.balloons()
                st.success("Great job! Issue resolved successfully.")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please ensure you're using the correct Excel file format.")

if __name__ == "__main__":
    main()