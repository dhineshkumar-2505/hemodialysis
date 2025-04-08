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
            <li>Use interactive troubleshooting mode for complex problems</li>
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

# Common troubleshooting procedures dictionary
common_procedures = {
    "power_cycle": {
        "title": "Power Cycling Procedure",
        "steps": [
            "Ensure the patient is stable and inform medical staff before proceeding",
            "Put the machine in bypass mode if applicable",
            "Power off the machine using the main power switch",
            "Wait 30 seconds for capacitors to discharge",
            "Turn the machine back on and observe the boot sequence",
            "Check if the alarm persists after restart"
        ]
    },
    "fluid_system": {
        "title": "Fluid System Check",
        "steps": [
            "Check all fluid lines for kinks or restrictions",
            "Inspect dialysate concentrate connections",
            "Verify water supply connections are secure",
            "Check for air in the fluid pathways",
            "Inspect drains for proper flow",
            "Verify all valves are in correct positions"
        ]
    },
    "pressure_test": {
        "title": "Pressure System Testing",
        "steps": [
            "Enter service mode (if applicable)",
            "Navigate to pressure test menu",
            "Follow on-screen instructions to test each pressure sensor",
            "Record any pressure deviations",
            "Check transducer connections",
            "Replace failed pressure components if needed"
        ]
    },
    "safety_systems": {
        "title": "Safety Systems Check",
        "steps": [
            "Verify blood leak detector is functioning",
            "Test air detector functionality",
            "Check temperature sensors",
            "Verify conductivity sensors operation",
            "Test bypass valve operation",
            "Ensure alarms trigger appropriately"
        ]
    }
}

# Interactive troubleshooting guide
def show_interactive_troubleshooting(alarm_name):
    st.markdown(f"""
    <div class="interactive-header">
        <h3>🔍 Interactive Troubleshooting for: {alarm_name}</h3>
        <p>Follow this step-by-step guide to resolve the issue</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Determine which procedures to show based on alarm name (simplified logic)
    related_procedures = []
    
    if any(word in alarm_name.lower() for word in ["pressure", "flow", "leak"]):
        related_procedures.append("pressure_test")
        related_procedures.append("fluid_system")
    
    if any(word in alarm_name.lower() for word in ["power", "electrical", "display", "system"]):
        related_procedures.append("power_cycle")
    
    if any(word in alarm_name.lower() for word in ["alarm", "safety", "detector", "temp"]):
        related_procedures.append("safety_systems")
    
    # If no specific procedures matched, show all common ones
    if not related_procedures:
        related_procedures = ["power_cycle", "fluid_system", "pressure_test", "safety_systems"]
    
    # Progress tracking
    current_step = st.session_state.get("troubleshoot_step", 0)
    max_steps = sum([len(common_procedures[p]["steps"]) for p in related_procedures])
    
    # Progress bar
    progress_bar = st.progress(current_step / max_steps if max_steps > 0 else 0)
    
    # Show procedure steps with checkboxes
    overall_step_counter = 0
    for procedure_key in related_procedures:
        procedure = common_procedures[procedure_key]
        
        st.markdown(f"""
        <div class="procedure-header">
            <h4>{procedure["title"]}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for i, step in enumerate(procedure["steps"]):
            step_key = f"{procedure_key}_step_{i}"
            step_complete = st.checkbox(
                f"{step}",
                key=step_key,
                value=overall_step_counter < current_step
            )
            
            # If this checkbox was just checked, increment the step counter
            if step_complete and overall_step_counter >= current_step:
                st.session_state.troubleshoot_step = overall_step_counter + 1
                progress_bar.progress((overall_step_counter + 1) / max_steps)
                
                # Show a success message for completing a procedure
                if overall_step_counter + 1 == sum([len(common_procedures[p]["steps"]) for p in related_procedures[:related_procedures.index(procedure_key)+1]]):
                    st.success(f"✅ {procedure['title']} completed!")
            
            overall_step_counter += 1
    
    # Final resolution options
    if current_step >= max_steps:
        st.markdown("### 🎯 Issue Resolution")
        resolution = st.radio(
            "Did these steps resolve the issue?",
            ["Yes, issue resolved", "No, issue persists"],
            key="resolution"
        )
        
        if resolution == "Yes, issue resolved":
            st.balloons()
            st.success("Great job! Please document this repair in the maintenance log.")
        else:
            st.warning("If the issue persists, consider:")
            st.markdown("""
            1. Escalating to senior biomedical engineer
            2. Referring to manufacturer service manual
            3. Contacting technical support: +1 (555) 456-7890
            """)
    
    # Reset button
    if st.button("Reset Troubleshooting Progress"):
        st.session_state.troubleshoot_step = 0
        st.experimental_rerun()

# Main app function
def main():
    # Initialize session state for troubleshooting
    if 'troubleshoot_step' not in st.session_state:
        st.session_state.troubleshoot_step = 0
        
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
        
        # NEW FEATURE: Interactive troubleshooting
        st.markdown("---")
        show_detailed = st.checkbox("Show detailed interactive troubleshooting guide", value=False)
        
        if show_detailed:
            show_interactive_troubleshooting(selected_alarm)
        else:
            # Add a completion check (original code)
            st.markdown("---")
            resolved = st.radio("Did this resolve your issue?", ("Still troubleshooting", "Issue resolved"), index=0)
            if resolved == "Issue resolved":
                st.balloons()
                st.success("Great job! Issue resolved successfully.")
        
        # NEW FEATURE: Technical diagrams and resources
        st.markdown("---")
        with st.expander("Technical Resources"):
            st.markdown("""
            ### Machine Documentation
            
            Check these resources for more detailed information:
            
            1. **Service Manual**: Access machine-specific documentation
            2. **Circuit Diagrams**: Electrical schematics for component testing
            3. **Parts Catalog**: Replacement part numbers and ordering
            4. **Training Materials**: Video tutorials on common repairs
            
            Contact your supervisor for access to restricted documentation.
            """)
            
            st.markdown("### Common Test Points")
            # Example table of test points
            test_points = pd.DataFrame({
                "Test Point": ["TP1", "TP2", "TP3", "TP4", "TP5"],
                "Location": ["Main PCB J3", "Power Supply", "Flow Sensor", "Pump Motor", "UI Board"],
                "Normal Range": ["3.3V ± 0.1V", "12V ± 0.5V", "0.5-4.5V", "0-24V DC", "5V ± 0.25V"],
                "Notes": [
                    "Reference voltage", 
                    "Main power rail",
                    "Varies with flow rate",
                    "Varies with speed",
                    "Digital logic supply"
                ]
            })
            st.dataframe(test_points)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please ensure you're using the correct Excel file format.")

if __name__ == "__main__":
    main()