import streamlit as st
import pandas as pd
import time

# App title and header
st.set_page_config(page_title="Medical Equipment Troubleshooter", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Try to load custom CSS if available
try:
    local_css("style.css")
except:
    pass

# Initialize state if not already done
if 'machine_selected' not in st.session_state:
    st.session_state.machine_selected = None
    
if 'troubleshoot_step' not in st.session_state:
    st.session_state.troubleshoot_step = 0

# Function to reset session state
def reset_state():
    st.session_state.machine_selected = None
    st.session_state.troubleshoot_step = 0

# ===== MACHINE SELECTION PAGE =====
def show_machine_selection():
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Medical Equipment Troubleshooting Assistant</h1>
        <p class="subheader">AI-powered diagnostic support for biomedical engineers</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='machine-selection'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="machine-card" id="pms-card">
            <img src="https://img.freepik.com/free-vector/battery-power-realistic-composition-with-isolated-image-accumulator-battery-with-charging-indicators-vector-illustration_1284-66320.jpg" alt="PMS Machine">
            <h3>Power Management System (PMS)</h3>
            <p>Troubleshoot issues with power supply, temperature, current, and system controls.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select PMS Machine"):
            st.session_state.machine_selected = "PMS"
            st.rerun()

    
    with col2:
        st.markdown("""
        <div class="machine-card" id="hemo-card">
            <img src="https://img.freepik.com/free-vector/dialysis-concept-illustration_114360-7293.jpg" alt="Hemodialysis Machine">
            <h3>Hemodialysis Machine</h3>
            <p>Troubleshoot alarms and issues with hemodialysis equipment.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Hemodialysis Machine"):
            st.session_state.machine_selected = "Hemodialysis"
            st.rerun()

    
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Medical Equipment Troubleshooter | For trained biomedical technicians only</p>
    </div>
    """, unsafe_allow_html=True)

# ===== PMS MACHINE TROUBLESHOOTING =====
def load_pms_data():
    # In a real app, this would load from a database or file
    # For this example, we'll create a structured dictionary
    pms_categories = {
        "Power Supply Errors": [
            "Low Battery Voltage",
            "AC Power Failure",
            "Overvoltage / Undervoltage"
        ],
        "Temperature-Related Errors": [
            "Over Temperature Warning",
            "Temperature Sensor Failure"
        ],
        "Current & Load-Related Errors": [
            "Overload Detection",
            "Short Circuit at Output",
            "Current Imbalance"
        ],
        "System Control & Communication Errors": [
            "Microcontroller Failure",
            "Communication Loss (CAN/RS485)"
        ],
        "Network/Remote Monitoring Errors": [
            "Modbus/SCADA Link Down",
            "Sensor Data Missing"
        ],
        "Maintenance & Predictive Alerts": [
            "Battery Health Warning",
            "Maintenance Due Reminder"
        ]
    }
    
    # Create a mapping of error codes to descriptions
    error_codes = {
        "E01": "Low Battery",
        "E02": "AC Power Failure",
        "E03": "Over Temperature",
        "E04": "Short Circuit Output",
        "E05": "Comm Error (CAN/RS485)",
        "E06": "MCU Crash"
    }
    
    # Create a detailed error information dictionary
    error_details = {
        "Low Battery Voltage": {
            "indication": "Red LED indicator, audible intermittent beeps, display message: 'Low Battery Voltage'",
            "causes": [
                "Aging or degraded battery",
                "Incomplete charging cycles",
                "Loose or corroded battery terminals"
            ],
            "impact": "Risk of system shutdown during AC power failure",
            "steps": [
                "Test voltage with multimeter",
                "Replace battery if below threshold",
                "Ensure tight and clean terminal connections"
            ]
        },
        "AC Power Failure": {
            "indication": "Blinking red LED, continuous alarm tone, display message: 'AC Mains Failure'",
            "causes": [
                "Power grid failure",
                "Damaged or disconnected AC input",
                "Blown AC input fuse"
            ],
            "impact": "Triggers battery backup; system shutdown if battery fails",
            "steps": [
                "Verify AC input source",
                "Inspect fuse and AC cord integrity",
                "Restore mains power supply"
            ]
        },
        "Overvoltage / Undervoltage": {
            "indication": "Beep + message: 'Voltage Out of Range'",
            "causes": [
                "Surge or sag in input power",
                "Faulty voltage regulator"
            ],
            "impact": "Internal component damage or malfunction",
            "steps": [
                "Monitor input voltage",
                "Stabilize source voltage using AVR or UPS"
            ]
        },
        "Over Temperature Warning": {
            "indication": "Continuous high-pitched alarm, red LED, message: 'System Overheat'",
            "causes": [
                "Blocked air vents",
                "Faulty cooling fan",
                "High ambient temperature"
            ],
            "impact": "Thermal shutdown or component damage",
            "steps": [
                "Clear obstructions",
                "Replace malfunctioning fans",
                "Improve cooling/ventilation"
            ]
        },
        "Temperature Sensor Failure": {
            "indication": "Amber LED, screen: 'Sensor Fault'",
            "causes": [
                "Broken or disconnected sensor",
                "Open/short circuit in sensor line"
            ],
            "impact": "Incorrect temperature regulation",
            "steps": [
                "Inspect sensor wiring",
                "Replace damaged sensors"
            ]
        },
        "Overload Detection": {
            "indication": "Red LED, beeping, display: 'Load Exceeded Limit'",
            "causes": [
                "Excessive connected load",
                "Faulty devices drawing high current"
            ],
            "impact": "Auto shutdown to prevent damage",
            "steps": [
                "Reduce load to within rated capacity",
                "Test individual connected devices"
            ]
        },
        "Short Circuit at Output": {
            "indication": "Loud alarm, system shutdown, screen: 'Output Short Detected'",
            "causes": [
                "Direct short in connected equipment",
                "Crossed wiring"
            ],
            "impact": "Damage to switching components (MOSFETs, IGBTs)",
            "steps": [
                "Isolate and test output branches",
                "Repair damaged circuits"
            ]
        },
        "Current Imbalance": {
            "indication": "Warning message, irregular load readings",
            "causes": [
                "Uneven load across phases",
                "Faulty sensor"
            ],
            "impact": "Reduced efficiency, potential overheating",
            "steps": [
                "Balance loads",
                "Check CT sensors"
            ]
        },
        "Microcontroller Failure": {
            "indication": "Frozen or blank screen, error code (e.g., E01)",
            "causes": [
                "Firmware crash",
                "Clock failure"
            ],
            "impact": "Full system halt",
            "steps": [
                "Reset system",
                "Reprogram controller or replace MCU"
            ]
        },
        "Communication Loss (CAN/RS485)": {
            "indication": "'Comm Error' message, yellow LED",
            "causes": [
                "Faulty communication cable",
                "Incorrect baud rate"
            ],
            "impact": "Module syncing fails",
            "steps": [
                "Verify cable connections",
                "Match communication settings"
            ]
        },
        "Modbus/SCADA Link Down": {
            "indication": "Icon with red cross, 'Network Lost'",
            "causes": [
                "Disconnected network cable",
                "Transceiver failure"
            ],
            "impact": "Remote monitoring inoperative",
            "steps": [
                "Replace or reconfigure communication module",
                "Restart SCADA/PLC systems"
            ]
        },
        "Sensor Data Missing": {
            "indication": "'No Signal from Sensor' alert",
            "causes": [
                "Broken sensor cable",
                "Sensor powered off"
            ],
            "impact": "Incorrect readings and control behavior",
            "steps": [
                "Replace or reconnect sensors"
            ]
        },
        "Battery Health Warning": {
            "indication": "'Battery Health Degraded' or 'Replace Battery Soon'",
            "causes": [
                "High internal resistance",
                "Battery age exceeds threshold"
            ],
            "impact": "Reduced backup time",
            "steps": [
                "Replace battery"
            ]
        },
        "Maintenance Due Reminder": {
            "indication": "Wrench icon, message: 'Service Due'",
            "causes": [
                "Predefined service interval reached"
            ],
            "impact": "Potential for future failures",
            "steps": [
                "Perform full system check",
                "Log service activity and reset maintenance timer"
            ]
        }
    }
    
    return pms_categories, error_codes, error_details

# Common troubleshooting procedures dictionary
common_procedures = {
    "power_cycle": {
        "title": "Power Cycling Procedure",
        "steps": [
            "Ensure the machine is safe to restart",
            "Power off the machine using the main power switch",
            "Wait 30 seconds for capacitors to discharge",
            "Turn the machine back on and observe the boot sequence",
            "Check if the alarm persists after restart"
        ]
    },
    "system_check": {
        "title": "System Diagnostic Check",
        "steps": [
            "Enter diagnostic mode (if applicable)",
            "Run system self-test",
            "Check for error codes or messages",
            "Verify sensor readings against normal ranges",
            "Document all abnormal values"
        ]
    },
    "connections_check": {
        "title": "Connection Verification",
        "steps": [
            "Inspect all cable connections",
            "Check for loose or damaged connectors",
            "Verify proper seating of all modular components",
            "Test continuity of suspect cables with multimeter",
            "Clean connectors if needed"
        ]
    },
    "safety_systems": {
        "title": "Safety Systems Check",
        "steps": [
            "Verify safety systems are functioning",
            "Test alarm functionality",
            "Check sensor calibration",
            "Verify bypass mechanisms work correctly",
            "Ensure all indicators and displays function properly"
        ]
    }
}

def show_pms_troubleshooting():
    st.markdown("""
    <div class="header">
        <h1>🔋 Power Management System (PMS) Troubleshooting</h1>
        <p class="subheader">Diagnose and resolve issues with power supply, temperature, and other systems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load PMS data
    pms_categories, error_codes, error_details = load_pms_data()
    
    # Sidebar for navigation
    with st.sidebar:
        st.image("https://img.freepik.com/free-vector/battery-power-realistic-composition-with-isolated-image-accumulator-battery-with-charging-indicators-vector-illustration_1284-66320.jpg", width=100)
        st.markdown("""
        <div class="sidebar-section">
            <h3>Quick Navigation</h3>
            <ul>
                <li>Select an error category</li>
                <li>Choose the specific error</li>
                <li>Follow the troubleshooting steps</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-section">
            <h3>Emergency Contact</h3>
            <p>For critical issues, contact:<br>
            <strong>Technical Support:</strong> +1 (555) 123-4567</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Button to go back to selection page
        if st.button("Change Machine"):
            reset_state()
            st.rerun()

    
    # Error category selection
    st.markdown("### 1️⃣ Select Error Category")
    selected_category = st.selectbox(
        "Choose the error category:",
        list(pms_categories.keys()),
        index=0,
        key="category_select"
    )
    
    # Error selection
    st.markdown("### 2️⃣ Select Specific Error")
    selected_error = st.selectbox(
        "Choose the specific error:",
        pms_categories[selected_category],
        index=0,
        key="error_select"
    )
    
    # Display error details
    if selected_error in error_details:
        st.markdown("### 3️⃣ Error Details")
        
        # Create a glowing box for the error name
        st.markdown(f"""
        <div class="glowing-box">
            <div class="glow"></div>
            <div class="content">
                <h3>{selected_error}</h3>
                <p><strong>Indication:</strong> {error_details[selected_error]['indication']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display causes in collapsible section
        with st.expander("Possible Causes"):
            for cause in error_details[selected_error]['causes']:
                st.markdown(f"- {cause}")
        
        # Display impact
        st.markdown(f"**Impact:** {error_details[selected_error]['impact']}")
        
        # Display steps
        st.markdown("### 4️⃣ Troubleshooting Steps")
        for i, step in enumerate(error_details[selected_error]['steps'], 1):
            # Animate the appearance of each step
            with st.empty():
                time.sleep(0.1)  # Small delay for animation effect
                st.markdown(f"""
                <div class="step-box animated-step">
                    <div class="step-number">Step {i}</div>
                    <div class="step-content">{step}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Interactive troubleshooting
        st.markdown("---")
        show_detailed = st.checkbox("Show interactive troubleshooting guide", value=False)
        
        if show_detailed:
            # Determine which procedures to show based on selected error
            related_procedures = []
            
            if selected_category == "Power Supply Errors":
                related_procedures.append("power_cycle")
                related_procedures.append("connections_check")
            
            elif selected_category == "Temperature-Related Errors":
                related_procedures.append("system_check")
                related_procedures.append("connections_check")
            
            elif selected_category == "Current & Load-Related Errors":
                related_procedures.append("power_cycle")
                related_procedures.append("system_check")
            
            elif selected_category == "System Control & Communication Errors":
                related_procedures.append("power_cycle")
                related_procedures.append("connections_check")
            
            elif selected_category == "Network/Remote Monitoring Errors":
                related_procedures.append("connections_check")
                related_procedures.append("system_check")
            
            else:
                related_procedures.append("system_check")
                related_procedures.append("safety_systems")
            
            # Add safety check for all procedures
            if "safety_systems" not in related_procedures:
                related_procedures.append("safety_systems")
            
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
                    1. Escalating to senior engineer
                    2. Referring to manufacturer service manual
                    3. Contacting technical support: +1 (555) 456-7890
                    """)
            
            # Reset button
            if st.button("Reset Troubleshooting Progress"):
                st.session_state.troubleshoot_step = 0
                st.rerun()

        
        # Add technical resources
        st.markdown("---")
        with st.expander("Technical Resources"):
            st.markdown("""
            ### Machine Documentation
            
            Check these resources for more detailed information:
            
            1. **Service Manual**: Access machine-specific documentation
            2. **Circuit Diagrams**: Electrical schematics for testing
            3. **Parts Catalog**: Replacement part numbers and ordering
            
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
    else:
        st.error("No data available for the selected error.")

# ===== HEMODIALYSIS MACHINE TROUBLESHOOTING =====
# Function to load Excel data
@st.cache_data
def load_hemodialysis_data(file_path=None):
    # If no file is provided, create example data
    if file_path is None:
        # Example data dictionary
        data_dict = {
            "Pre-Treatment": pd.DataFrame({
                "Alarms / Reasons": ["Water Pressure Low", "Concentrate Error", "Air Detector Alarm", "Blood Leak Detector", "Issues"],
                "Reason 1": ["Check water supply", "Check concentrate connection", "Reset air detector", "Verify detector calibration", "Additional issues below"],
                "Reason 2": ["Verify inlet pressure", "Verify concentrate ratio", "Check tubing for air", "Test detector function", ""],
                "Reason 3": ["Check pressure regulator", "Inspect mixing system", "Inspect venous chamber", "Replace detector if needed", ""],
                "Reason 4": ["Replace filter if needed", "Replace concentrate if needed", "Check pump function", "", ""],
            }),
            "During Treatment": pd.DataFrame({
                "Alarms / Reasons": ["Venous Pressure High", "Arterial Pressure Low", "Temperature Error", "Conductivity Error", "Issues"],
                "Reason 1": ["Check for kinks in line", "Check access needle position", "Verify temperature sensor", "Check concentrate ratio", "Additional issues below"],
                "Reason 2": ["Inspect venous clamp", "Inspect arterial line", "Reset temperature limits", "Calibrate conductivity meter", ""],
                "Reason 3": ["Verify clot filter", "Check blood pump function", "Check heater function", "Replace conductivity cell", ""],
                "Reason 4": ["Reposition catheter", "", "", "", ""],
            }),
            "Post-Treatment": pd.DataFrame({
                "Alarms / Reasons": ["Disinfection Error", "Rinse Failure", "System Test Failed", "Battery Warning", "Issues"],
                "Reason 1": ["Check disinfectant supply", "Verify water supply", "Run diagnostics", "Test battery voltage", "Additional issues below"],
                "Reason 2": ["Verify concentration", "Check drain function", "Check individual components", "Replace battery if needed", ""],
                "Reason 3": ["Check timing parameters", "Inspect fluid paths", "Reset system memory", "", ""],
                "Reason 4": ["Replace disinfectant", "Clear clogged lines", "", "", ""],
            })
        }
        
        sheet_names = list(data_dict.keys())
        return data_dict, sheet_names
    else:
        # Load from Excel file
        try:
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
        except Exception as e:
            # Return example data if file loading fails
            st.warning(f"Error loading Excel file: {str(e)}. Using example data instead.")
            return load_hemodialysis_data(None)

# Function to get all alarms from a sheet
def get_alarms_for_sheet(df):
    alarms = df['Alarms / Reasons'].dropna().unique().tolist()
    issues = df[df['Alarms / Reasons'] == 'Issues'].index
    if len(issues) > 0:
        issue_start = issues[0] + 1
        additional_issues = df.iloc[issue_start:]['Alarms / Reasons'].dropna().unique().tolist()
        alarms.extend(additional_issues)
    return [a for a in alarms if a != 'Issues' and str(a) != 'nan']

def show_hemodialysis_troubleshooting():
    st.markdown("""
    <div class="header">
        <h1>🧡 Hemodialysis Machine Troubleshooting Assistant</h1>
        <p class="subheader">AI-powered diagnostic support for biomedical engineers</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for navigation and info
    with st.sidebar:
        st.image("https://img.freepik.com/free-vector/dialysis-concept-illustration_114360-7293.jpg", width=100)
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
        
        # Button to go back to selection page
        if st.button("Change Machine"):
            reset_state()
            st.rerun()

    
    # Hemodialysis troubleshooting logic
    try:
        # Load data (dummy file path since we're using example data)
        data_dict, sheet_names = load_hemodialysis_data()
        
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
        
        # Interactive troubleshooting
        st.markdown("---")
        show_detailed = st.checkbox("Show detailed interactive troubleshooting guide", value=False)
        
        if show_detailed:
            st.markdown(f"""
            <div class="interactive-header">
                <h3>🔍 Interactive Troubleshooting for: {selected_alarm}</h3>
                <p>Follow this step-by-step guide to resolve the issue</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Determine which procedures to show based on alarm name (simplified logic)
            related_procedures = []
            
            if any(word in selected_alarm.lower() for word in ["pressure", "flow", "leak"]):
                related_procedures.append("connections_check")
                related_procedures.append("system_check")
            
            if any(word in selected_alarm.lower() for word in ["power", "electrical", "display", "system"]):
                related_procedures.append("power_cycle")
            
            if any(word in selected_alarm.lower() for word in ["alarm", "safety", "detector", "temp"]):
                related_procedures.append("safety_systems")
            
            # If no specific procedures identified, add a default set
            if not related_procedures:
                related_procedures = ["connections_check", "system_check", "safety_systems"]
            
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
                    1. Escalating to senior technician
                    2. Referring to manufacturer service manual
                    3. Contacting technical support: +1 (555) 789-0123
                    """)
            
            # Reset button
            if st.button("Reset Troubleshooting Progress"):
                st.session_state.troubleshoot_step = 0
                st.rerun()

        
        # Add technical resources
        st.markdown("---")
        with st.expander("Technical Resources"):
            st.markdown("""
            ### Machine Documentation
            
            Check these resources for more detailed information:
            
            1. **Service Manual**: Access machine-specific documentation
            2. **Circuit Diagrams**: Electrical schematics for testing
            3. **Parts Catalog**: Replacement part numbers and ordering
            
            Contact your supervisor for access to restricted documentation.
            """)
            
            st.markdown("### Common Test Points")
            # Example table of test points for hemodialysis
            test_points = pd.DataFrame({
                "Test Point": ["TP1", "TP2", "TP3", "TP4", "TP5"],
                "Location": ["Main PCB J7", "Flow Sensor", "Heat Exchanger", "UF Pump", "Control Board"],
                "Normal Range": ["5V DC ± 0.2V", "0.5-4.5V", "36-39°C", "±24V DC", "3.3V ± 0.1V"],
                "Notes": [
                    "Logic supply", 
                    "Varies with flow",
                    "Treatment temperature",
                    "Varies with operation",
                    "Digital signal reference"
                ]
            })
            st.dataframe(test_points)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try refreshing the page or contact IT support.")

# ===== MAIN APP LOGIC =====
def main():
    # Apply custom styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        margin-bottom: 30px;
        background: linear-gradient(to right, #4e54c8, #8f94fb);
        border-radius: 10px;
        color: white;
    }
    
    .subheader {
        font-size: 1.2em;
        opacity: 0.9;
    }
    
    .machine-selection {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    
    .machine-card {
        background: #fff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
        margin-bottom: 20px;
    }
    
    .machine-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    }
    
    .machine-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    
    .machine-card h3 {
        color: #333;
        margin-bottom: 10px;
    }
    
    .machine-card p {
        color: #666;
        font-size: 0.9em;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        color: #888;
        font-size: 0.8em;
    }
    
    .glowing-box {
        position: relative;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.1);
        box-shadow: 0 0 15px rgba(78, 84, 200, 0.5);
        overflow: hidden;
    }
    
    .glow {
        position: absolute;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        background: linear-gradient(45deg, rgba(78, 84, 200, 0.3), rgba(143, 148, 251, 0.3));
        z-index: -1;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            opacity: 0.5;
        }
        50% {
            opacity: 0.8;
        }
        100% {
            opacity: 0.5;
        }
    }
    
    .content {
        position: relative;
        z-index: 1;
    }
    
    .step-box {
        display: flex;
        background: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .step-number {
        background: #4e54c8;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        margin-right: 15px;
        font-weight: 600;
        min-width: 80px;
        text-align: center;
    }
    
    .step-content {
        flex: 1;
        padding: 8px 0;
    }
    
    .animated-step {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .procedure-header {
        background: #eef2ff;
        padding: 10px 15px;
        border-radius: 6px;
        margin: 15px 0 10px 0;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    
    .notes-box {
        background: #fff9db;
        border-left: 4px solid #ffd43b;
        padding: 15px;
        border-radius: 0 8px 8px 0;
    }
    
    .animated-notes {
        animation: slideIn 0.7s ease-in-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .interactive-header {
        background: linear-gradient(to right, #3a7bd5, #00d2ff);
        padding: 15px;
        border-radius: 8px;
        color: white;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check which machine is selected
    if st.session_state.machine_selected is None:
        show_machine_selection()
    elif st.session_state.machine_selected == "PMS":
        show_pms_troubleshooting()
    elif st.session_state.machine_selected == "Hemodialysis":
        show_hemodialysis_troubleshooting()

if __name__ == "__main__":
    main()
