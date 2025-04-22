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
    
    col1, col2, col3 = st.columns(3)
    
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
    
    with col3:
        st.markdown("""
        <div class="machine-card" id="up7000-card">
            <img src="https://img.freepik.com/free-vector/health-monitoring-abstract-concept-vector-illustration-remote-monitoring-device-smart-healthcare-diagnostic-system-wearable-technology-data-collection-personal-medical-service-abstract-metaphor_335657-2304.jpg" alt="UP-7000 Patient Monitor">
            <h3>UP-7000 Patient Monitoring System</h3>
            <p>Troubleshoot issues with ECG, NIBP, SpO₂, CO₂, display, and printer.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select UP-7000 Patient Monitor"):
            st.session_state.machine_selected = "UP7000"
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

# ===== UP-7000 PATIENT MONITORING SYSTEM DATA =====
def load_up7000_data():
    # Categories of errors for the UP-7000
    up7000_categories = {
        "Display Issues": [
            "No Display on Screen"
        ],
        "ECG Issues": [
            "Lead Off Message",
            "Thick Baseline / Interference",
            "Pacemaker Signal Miscount"
        ],
        "NIBP (Blood Pressure) Issues": [
            "No Reading",
            "Overpressure or Inflation Error",
            "Motion Artifact or Signal Weak"
        ],
        "SpO₂ (Oxygen Saturation) Issues": [
            "No Reading or Low Readings",
            "Probe Off Alarm",
            "Sensor Temperature High"
        ],
        "CO₂ Monitoring Issues": [
            "Sensor Over Temperature",
            "Sensor Faulty or EEPROM Error",
            "Check Sampling Line or Airway Adapter",
            "Zero Required Warning"
        ],
        "Temperature Monitoring Errors": [
            "Temperature Probe Issues"
        ],
        "System Alarms": [
            "High Priority Alarms",
            "Medium Priority Alarms",
            "Low Priority Alarms"
        ],
        "Arrhythmia Detection Issues": [
            "Arrhythmia Detection Problems"
        ],
        "Waveform Problems": [
            "Freezing or No Movement"
        ],
        "Printer Issues": [
            "Paper Not Feeding",
            "Printing Blank"
        ]
    }
    
    # Create a detailed error information dictionary
    error_details = {
        "No Display on Screen": {
            "indication": "Screen remains black or blank when powered on",
            "causes": [
                "Monitor not receiving power",
                "Faulty AC cable or fuse blown",
                "Internal fault in the display"
            ],
            "impact": "Unable to view patient data or use the monitor",
            "steps": [
                "Check that the AC plug is properly connected to a grounded outlet",
                "Try turning on the monitor using its power button",
                "If AC power fails, try using the built-in battery (ensure it's charged)",
                "Check the fuse on the back panel. Replace if necessary",
                "If none of these work, contact service for internal board or LCD replacement"
            ]
        },
        "Lead Off Message": {
            "indication": "ECG trace missing with 'Lead Off' message",
            "causes": [
                "ECG electrodes are not connected or are loose"
            ],
            "impact": "Unable to monitor heart activity",
            "steps": [
                "Ensure skin is clean and dry (avoid using alcohol as it leaves a film)",
                "Reposition the ECG electrodes on correct anatomical locations",
                "Use high-quality silver/silver chloride electrodes",
                "Make sure cables are properly snapped into the electrodes"
            ]
        },
        "Thick Baseline / Interference": {
            "indication": "ECG waveform with significant noise or distortion",
            "causes": [
                "Patient movement",
                "Dry skin",
                "Electrical interference"
            ],
            "impact": "Difficulty accurately reading ECG",
            "steps": [
                "Re-prepare the skin and reapply electrodes",
                "Keep ECG cables away from power cables or ESU",
                "Verify that the monitor is properly grounded"
            ]
        },
        "Pacemaker Signal Miscount": {
            "indication": "Incorrect heart rate displayed for patients with pacemakers",
            "causes": [
                "Some pacemaker pulses may be miscounted as heartbeats"
            ],
            "impact": "Inaccurate heart rate monitoring",
            "steps": [
                "Use 5-lead ECG and observe the waveform closely",
                "Never rely solely on heart rate alarms; always visually confirm ECG",
                "Adjust pacemaker rejection settings if available"
            ]
        },
        "No Reading": {
            "indication": "NIBP displays no values or error message",
            "causes": [
                "Loose cuff",
                "Tubing kinked",
                "Leak in the system"
            ],
            "impact": "Unable to measure blood pressure",
            "steps": [
                "Re-wrap the cuff snugly on the upper arm",
                "Ensure the cuff is the correct size for the patient (too small or large affects accuracy)",
                "Check for leaks by manually inflating and listening for hissing"
            ]
        },
        "Overpressure or Inflation Error": {
            "indication": "NIBP displays error message or over-pressure alarm",
            "causes": [
                "Incorrect patient type selected",
                "Faulty pressure valve"
            ],
            "impact": "Risk of patient discomfort or injury",
            "steps": [
                "Switch mode to correct patient type (Adult, Pediatric, Neonate)",
                "Avoid continuous NIBP mode unless under supervision",
                "Perform pressure accuracy verification or leak test"
            ]
        },
        "Motion Artifact or Signal Weak": {
            "indication": "NIBP displays 'Motion Artifact' or 'Signal Weak' message",
            "causes": [
                "Patient movement during measurement"
            ],
            "impact": "Inaccurate or failed BP readings",
            "steps": [
                "Ask patient to stay still and avoid talking",
                "Do not place cuff on limb with IV lines or wounds",
                "Monitor the color and temperature of the limb to ensure circulation isn't blocked"
            ]
        },
        "No Reading or Low Readings": {
            "indication": "SpO₂ values missing or suspiciously low",
            "causes": [
                "Loose probe",
                "Low perfusion",
                "Ambient light interference"
            ],
            "impact": "Inaccurate oxygen monitoring",
            "steps": [
                "Ensure probe fits snugly on the finger and the nail is clean and not painted",
                "Avoid placing on edematous or injured fingers",
                "Cover the sensor with opaque tape or cloth to block bright light",
                "Switch fingers if readings are unstable"
            ]
        },
        "Probe Off Alarm": {
            "indication": "SpO₂ displays 'Probe Off' message",
            "causes": [
                "Sensor disconnected",
                "Sensor damaged"
            ],
            "impact": "No SpO₂ monitoring",
            "steps": [
                "Disconnect and reconnect the SpO₂ cable",
                "Replace the sensor if damaged or old"
            ]
        },
        "Sensor Temperature High": {
            "indication": "SpO₂ alarm for high sensor temperature",
            "causes": [
                "Sensor overheating",
                "Sensor left in same position too long"
            ],
            "impact": "Risk of skin burns",
            "steps": [
                "Remove the sensor and replace with a new one",
                "Do not leave the same site monitored for more than 2 hours continuously"
            ]
        },
        "Sensor Over Temperature": {
            "indication": "CO₂ module displays temperature warning",
            "causes": [
                "Overheating CO₂ sensor",
                "External heat source"
            ],
            "impact": "Inaccurate CO₂ readings",
            "steps": [
                "Turn off the unit, allow cooling, and restart",
                "Move away from external heat sources (sunlight, heaters)",
                "Replace the CO₂ sensor if repeated"
            ]
        },
        "Sensor Faulty or EEPROM Error": {
            "indication": "CO₂ displays 'Sensor Faulty' or 'EEPROM Error'",
            "causes": [
                "Sensor memory error",
                "Hardware failure"
            ],
            "impact": "Unable to monitor CO₂",
            "steps": [
                "Restart the monitor",
                "If error persists, replace the CO₂ module"
            ]
        },
        "Check Sampling Line or Airway Adapter": {
            "indication": "CO₂ displays 'Check Sampling Line' or 'Check Airway Adapter'",
            "causes": [
                "Blocked tubing",
                "Dirty or damaged adapter"
            ],
            "impact": "Inaccurate CO₂ readings",
            "steps": [
                "Ensure tubing is not blocked or kinked",
                "Replace the airway adapter if dirty or damaged",
                "Never reuse single-use CO₂ adapters"
            ]
        },
        "Zero Required Warning": {
            "indication": "CO₂ displays 'Zero Required' message",
            "causes": [
                "Calibration drift",
                "New sensor installed"
            ],
            "impact": "Inaccurate CO₂ readings",
            "steps": [
                "Disconnect the sampling line",
                "Select 'Zero' in the monitor menu",
                "Wait until the system completes the process"
            ]
        },
        "Temperature Probe Issues": {
            "indication": "Erratic or missing temperature readings",
            "causes": [
                "Loose probe connection",
                "Damaged probe",
                "Incorrect placement"
            ],
            "impact": "Inaccurate temperature monitoring",
            "steps": [
                "Ensure temperature probes are firmly attached and connected to correct ports",
                "Avoid attaching to exposed skin; probe should be covered or taped down",
                "If temperature values are erratic, clean or replace the probe"
            ]
        },
        "High Priority Alarms": {
            "indication": "Red flashing lights and urgent alarm tone",
            "causes": [
                "Cardiac arrest",
                "Pulse stop",
                "Apnea",
                "Dangerous vital sign values"
            ],
            "impact": "Indicates life-threatening condition",
            "steps": [
                "Attend to patient immediately",
                "Verify the patient's condition",
                "Resolve underlying clinical issue",
                "Only silence alarm when actively addressing the problem"
            ]
        },
        "Medium Priority Alarms": {
            "indication": "Orange flashing lights and medium urgency tone",
            "causes": [
                "Probe off",
                "Lead off",
                "Sensor error"
            ],
            "impact": "Technical issue affecting monitoring",
            "steps": [
                "Check connections and equipment",
                "Replace or reposition sensors as needed",
                "Address technical issues promptly"
            ]
        },
        "Low Priority Alarms": {
            "indication": "Orange solid light (not flashing) and low urgency tone",
            "causes": [
                "Arrhythmia detection",
                "Parameter approaching limit"
            ],
            "impact": "Potential developing issue",
            "steps": [
                "Monitor the situation",
                "Check patient condition",
                "Prepare for intervention if condition worsens"
            ]
        },
        "Arrhythmia Detection Problems": {
            "indication": "False arrhythmia alarms or missed arrhythmias",
            "causes": [
                "Poor signal quality",
                "Learning function not activated",
                "ECG leads positioned incorrectly"
            ],
            "impact": "Missed cardiac events or false alarms",
            "steps": [
                "Start 'Learn' function when new patient is connected",
                "Make sure ECG waveform is stable before enabling ARR detection",
                "If wrong arrhythmia is triggered, perform ARR relearning"
            ]
        },
        "Freezing or No Movement": {
            "indication": "Waveforms not moving on screen",
            "causes": [
                "System in Freeze mode",
                "Printer in active mode"
            ],
            "impact": "Not seeing real-time patient data",
            "steps": [
                "Press 'Freeze' again to return to live monitoring",
                "Check if printer is actively printing; printing may pause waveforms"
            ]
        },
        "Paper Not Feeding": {
            "indication": "Printer not producing paper output",
            "causes": [
                "Improper paper loading",
                "Door not closed",
                "Paper jam"
            ],
            "impact": "Unable to print patient data",
            "steps": [
                "Reload paper following the guide (cut end into triangle, insert under roller)",
                "Ensure printer door is closed tightly",
                "Clear any paper jams"
            ]
        },
        "Printing Blank": {
            "indication": "Paper feeds but no printing appears",
            "causes": [
                "Paper inserted backwards",
                "Wrong paper type",
                "Printhead failure"
            ],
            "impact": "No record of patient data",
            "steps": [
                "Check paper orientation",
                "Use only manufacturer-recommended paper",
                "If persists, service required for printhead"
            ]
        }
    }
    
    return up7000_categories, error_details

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
            # Progress bar
            progress_bar = st.progress(current_step / max_steps if max_steps > 0 else 0)
            
            # Display procedures
            for proc_name in related_procedures:
                proc = common_procedures[proc_name]
                st.markdown(f"### {proc['title']}")
                
                for i, step in enumerate(proc['steps']):
                    step_index = sum([len(common_procedures[p]["steps"]) for p in related_procedures[:related_procedures.index(proc_name)]]) + i
                    
                    # Create a checkbox for each step
                    if st.checkbox(f"{step}", value=step_index < current_step, key=f"step_{proc_name}_{i}"):
                        if step_index >= current_step:
                            st.session_state.troubleshoot_step = step_index + 1
                            progress_bar.progress(st.session_state.troubleshoot_step / max_steps if max_steps > 0 else 0)
            
            # Reset progress button
            if st.button("Reset Progress"):
                st.session_state.troubleshoot_step = 0
                st.rerun()
        
        # Resolution confirmation
        st.markdown("---")
        st.markdown("### 5️⃣ Resolution Confirmation")
        
        resolution_status = st.radio(
            "Has the issue been resolved?",
            ["Select an option", "Yes, issue resolved", "No, issue persists"],
            index=0
        )
        
        if resolution_status == "Yes, issue resolved":
            st.success("Great! The issue has been resolved. Remember to document this incident in your maintenance log.")
            if st.button("Start New Troubleshooting Session"):
                reset_state()
                st.rerun()
        elif resolution_status == "No, issue persists":
            st.error("The issue persists. Consider the following options:")
            st.markdown("""
            1. Escalate to Technical Support
            2. Check for additional error codes
            3. Refer to manufacturer's service manual
            4. Replace the affected component
            """)

# ===== HEMODIALYSIS MACHINE TROUBLESHOOTING =====
def load_hemodialysis_data():
    # Categories of errors for hemodialysis machines
    hemo_categories = {
        "Water System Errors": [
            "Water Pressure Low",
            "Water Temperature Error",
            "Conductivity Error"
        ],
        "Blood Circuit Errors": [
            "Air Detector Alarm",
            "Venous Pressure Alarm",
            "Arterial Pressure Alarm",
            "Blood Leak Detector Alarm"
        ],
        "Dialysate Circuit Issues": [
            "Dialysate Flow Error",
            "Dialysate Temperature Alarm",
            "Ultrafiltration Error"
        ],
        "Pump and Motor Errors": [
            "Blood Pump Error",
            "Dialysate Pump Error",
            "UF Pump Error"
        ],
        "Sensor and Detector Issues": [
            "Level Detector Error",
            "Bubbles Detected",
            "Conductivity Sensor Error"
        ],
        "System Control Errors": [
            "Power Failure",
            "Battery Error",
            "Software Error"
        ]
    }
    
    # Detailed error information
    error_details = {
        "Water Pressure Low": {
            "indication": "Audible alarm, 'Water Pressure Low' message on screen",
            "causes": [
                "Water supply disruption",
                "Clogged pre-filters",
                "Faulty pressure regulator"
            ],
            "impact": "Inability to produce dialysate properly",
            "steps": [
                "Check water supply to the machine",
                "Verify pre-filters are clean and not clogged",
                "Check pressure gauge readings against acceptable range",
                "Ensure pressure regulator is functioning correctly"
            ]
        },
        "Water Temperature Error": {
            "indication": "Alarm and error message indicating water temperature out of range",
            "causes": [
                "Heater malfunction",
                "Incoming water temperature too low",
                "Temperature sensor failure"
            ],
            "impact": "Incorrect dialysate temperature may cause patient discomfort or harm",
            "steps": [
                "Check temperature sensor readings",
                "Verify heater operation",
                "Ensure incoming water temperature meets specifications",
                "Calibrate temperature sensors if possible"
            ]
        },
        "Conductivity Error": {
            "indication": "Alarm indicating conductivity out of range",
            "causes": [
                "Incorrect concentrate ratio",
                "Malfunctioning conductivity sensor",
                "Air in the hydraulic system"
            ],
            "impact": "Improper dialysate concentration may cause electrolyte imbalance",
            "steps": [
                "Check concentrate containers for proper solutions",
                "Verify concentrate pump operation",
                "Calibrate conductivity cells",
                "Perform rinse cycle to remove air"
            ]
        },
        "Air Detector Alarm": {
            "indication": "Air detector alarm, machine stops blood pump",
            "causes": [
                "Air bubbles in blood line",
                "Improper tubing placement in detector",
                "Faulty air detector"
            ],
            "impact": "Risk of air embolism if ignored",
            "steps": [
                "Check for air bubbles in venous line",
                "Ensure tubing is properly positioned in air detector",
                "Verify connections are secure",
                "Reset alarm only after confirming air is removed"
            ]
        },
        "Venous Pressure Alarm": {
            "indication": "Alarm indicating abnormal venous pressure (high or low)",
            "causes": [
                "Patient's venous access issues",
                "Kinked blood tubing",
                "Clotting in the venous chamber",
                "Incorrect pressure transducer connection"
            ],
            "impact": "Improper blood return to patient",
            "steps": [
                "Check venous access and cannula position",
                "Inspect blood tubing for kinks or obstruction",
                "Verify venous chamber level",
                "Ensure pressure transducer protector is dry and properly connected"
            ]
        },
        "Arterial Pressure Alarm": {
            "indication": "Alarm indicating abnormal arterial pressure (usually low)",
            "causes": [
                "Access needle position issues",
                "Occlusion in arterial line",
                "Blood pump speed too high",
                "Pressure transducer issue"
            ],
            "impact": "Inadequate blood flow to the dialyzer",
            "steps": [
                "Check arterial access and needle position",
                "Inspect arterial line for kinks",
                "Adjust blood pump speed if necessary",
                "Verify arterial transducer connection"
            ]
        },
        "Blood Leak Detector Alarm": {
            "indication": "Blood leak alarm, machine may stop",
            "causes": [
                "Actual blood leak in dialyzer",
                "Air bubbles in dialysate line",
                "Detector malfunction",
                "Contamination in optical system"
            ],
            "impact": "Blood loss into dialysate",
            "steps": [
                "Check dialysate line for visible blood",
                "Inspect dialyzer for potential rupture",
                "Verify detector function with test",
                "Clean optical detector if necessary"
            ]
        },
        "Dialysate Flow Error": {
            "indication": "Dialysate flow rate error message",
            "causes": [
                "Restricted flow path",
                "Pump malfunction",
                "Flow meter inaccuracy"
            ],
            "impact": "Suboptimal dialysis efficiency",
            "steps": [
                "Check for restrictions in dialysate pathway",
                "Verify pump operation",
                "Calibrate flow meter",
                "Ensure proper drain function"
            ]
        },
        "Dialysate Temperature Alarm": {
            "indication": "Temperature out of range alarm for dialysate",
            "causes": [
                "Heater malfunction",
                "Temperature sensor failure",
                "Control board issue"
            ],
            "impact": "Patient discomfort, potential hemolysis if too high",
            "steps": [
                "Allow system to stabilize",
                "Verify temperature sensor readings",
                "Check heater function",
                "Calibrate temperature sensors"
            ]
        },
        "Ultrafiltration Error": {
            "indication": "UF rate or volume error message",
            "causes": [
                "UF pump malfunction",
                "Flow balancing system issue",
                "Pressure transducer problem",
                "Valve leakage"
            ],
            "impact": "Incorrect fluid removal from patient",
            "steps": [
                "Verify UF settings",
                "Check UF pump operation",
                "Test balancing chamber function",
                "Calibrate pressure transducers"
            ]
        },
        "Blood Pump Error": {
            "indication": "Blood pump not running or error message",
            "causes": [
                "Pump rotor obstruction",
                "Motor failure",
                "Control board issue",
                "Pump segment improperly loaded"
            ],
            "impact": "Unable to circulate blood",
            "steps": [
                "Check pump segment loading",
                "Inspect rotor for free movement",
                "Test pump motor function",
                "Verify control signals to pump"
            ]
        },
        "Dialysate Pump Error": {
            "indication": "Dialysate flow issues or pump error message",
            "causes": [
                "Pump mechanism failure",
                "Control issue",
                "Obstruction in flow path"
            ],
            "impact": "Inadequate dialysate flow",
            "steps": [
                "Check for restrictions in dialysate pathway",
                "Verify pump operation",
                "Test motor and control circuits",
                "Inspect for leaks or air in system"
            ]
        },
        "UF Pump Error": {
            "indication": "UF pump error or UF goal not achievable",
            "causes": [
                "UF pump malfunction",
                "Control system issue",
                "Calibration error"
            ],
            "impact": "Inability to achieve ultrafiltration goals",
            "steps": [
                "Verify UF pump operation",
                "Check control signals to pump",
                "Run pump calibration test",
                "Inspect for mechanical issues"
            ]
        },
        "Level Detector Error": {
            "indication": "Level detector alarm or error",
            "causes": [
                "Incorrect level in chambers",
                "Detector malfunction",
                "Contamination on optical sensors"
            ],
            "impact": "Improper fluid management",
            "steps": [
                "Check fluid levels in chambers",
                "Clean optical detectors if applicable",
                "Verify detector operation with test",
                "Adjust levels manually if necessary"
            ]
        },
        "Bubbles Detected": {
            "indication": "Bubble detector alarm",
            "causes": [
                "Actual air in blood circuit",
                "Sensor misalignment",
                "Ultrasonic coupling issue"
            ],
            "impact": "Risk of air embolism",
            "steps": [
                "Check for visible air bubbles",
                "Verify sensor position and coupling",
                "Check for proper priming of circuit",
                "Ensure venous chamber level is appropriate"
            ]
        },
        "Conductivity Sensor Error": {
            "indication": "Conductivity sensor failure message",
            "causes": [
                "Sensor malfunction",
                "Calibration drift",
                "Contaminants on sensor"
            ],
            "impact": "Unable to verify dialysate composition",
            "steps": [
                "Clean sensors according to manufacturer guidance",
                "Calibrate sensors if possible",
                "Check reference values with external meter",
                "Verify sensor connections"
            ]
        },
        "Power Failure": {
            "indication": "Machine shuts down or switches to battery",
            "causes": [
                "Power supply interruption",
                "Internal power supply failure",
                "Circuit breaker trip"
            ],
            "impact": "Interruption of treatment",
            "steps": [
                "Check power source and connections",
                "Verify circuit breakers",
                "Switch to battery operation if available",
                "Follow emergency procedures for returning blood"
            ]
        },
        "Battery Error": {
            "indication": "Battery warning or failure message",
            "causes": [
                "Battery charge depleted",
                "Battery failing to hold charge",
                "Charging circuit issue"
            ],
            "impact": "No backup power during outages",
            "steps": [
                "Check battery charge status",
                "Ensure proper charging",
                "Test battery under load",
                "Replace battery if necessary"
            ]
        },
        "Software Error": {
            "indication": "Software crash, freeze, or error code",
            "causes": [
                "Software bug",
                "Memory corruption",
                "Processing overload"
            ],
            "impact": "Machine malfunction or shutdown",
            "steps": [
                "Record error code",
                "Perform controlled shutdown",
                "Restart system",
                "Contact technical support if persistent"
            ]
        }
    }
    
    return hemo_categories, error_details

def show_hemodialysis_troubleshooting():
    st.markdown("""
    <div class="header">
        <h1>🩸 Hemodialysis Machine Troubleshooting</h1>
        <p class="subheader">Diagnose and resolve issues with hemodialysis equipment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load hemodialysis data
    hemo_categories, error_details = load_hemodialysis_data()
    
    # Sidebar for navigation
    with st.sidebar:
        st.image("https://img.freepik.com/free-vector/dialysis-concept-illustration_114360-7293.jpg", width=100)
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
            <strong>Technical Support:</strong> +1 (555) 987-6543</p>
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
        list(hemo_categories.keys()),
        index=0,
        key="category_select"
    )
    
    # Error selection
    st.markdown("### 2️⃣ Select Specific Error")
    selected_error = st.selectbox(
        "Choose the specific error:",
        hemo_categories[selected_category],
        index=0,
        key="error_select"
    )
    
    # Display error details
    if selected_error in error_details:
        st.markdown("### 3️⃣ Error Details")
        
        # Create a glowing box for the error name
        st.markdown(f"""
        <div class="glowing-box red-glow">
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
        
        # Display impact - with warning styling for hemodialysis issues
        st.markdown(f"""
        <div class="warning-box">
            <strong>⚠️ Clinical Impact:</strong> {error_details[selected_error]['impact']}
        </div>
        """, unsafe_allow_html=True)
        
        # Display steps
        st.markdown("### 4️⃣ Troubleshooting Steps")
        
        # First show critical reminder for safety
        st.markdown("""
        <div class="critical-reminder">
            <strong>⚠️ CRITICAL REMINDER:</strong> Always prioritize patient safety. If in doubt, return blood to patient using emergency procedures and contact clinical staff.
        </div>
        """, unsafe_allow_html=True)
        
        for i, step in enumerate(error_details[selected_error]['steps'], 1):
            # Animate the appearance of each step
            with st.empty():
                time.sleep(0.1)  # Small delay for animation effect
                st.markdown(f"""
                <div class="step-box animated-step red-theme">
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
            
            if selected_category == "Water System Errors":
                related_procedures.append("system_check")
                related_procedures.append("connections_check")
            
            elif selected_category == "Blood Circuit Errors":
                related_procedures.append("safety_systems")
                related_procedures.append("connections_check")
            
            elif selected_category == "Dialysate Circuit Issues":
                related_procedures.append("system_check")
                related_procedures.append("connections_check")
            
            elif selected_category == "Pump and Motor Errors":
                related_procedures.append("power_cycle")
                related_procedures.append("system_check")
            
            elif selected_category == "Sensor and Detector Issues":
                related_procedures.append("connections_check")
                related_procedures.append("system_check")
            
            else:
                related_procedures.append("power_cycle")
                related_procedures.append("system_check")
            
            # Add safety check for all procedures
            if "safety_systems" not in related_procedures:
                related_procedures.append("safety_systems")
            
            # Progress tracking
            current_step = st.session_state.get("troubleshoot_step", 0)
            max_steps = sum([len(common_procedures[p]["steps"]) for p in related_procedures])
            
            # Progress bar
            progress_bar = st.progress(current_step / max_steps if max_steps > 0 else 0)
            
            # Display procedures
            for proc_name in related_procedures:
                proc = common_procedures[proc_name]
                st.markdown(f"### {proc['title']}")
                
                for i, step in enumerate(proc['steps']):
                    step_index = sum([len(common_procedures[p]["steps"]) for p in related_procedures[:related_procedures.index(proc_name)]]) + i
                    
                    # Create a checkbox for each step
                    if st.checkbox(f"{step}", value=step_index < current_step, key=f"step_{proc_name}_{i}"):
                        if step_index >= current_step:
                            st.session_state.troubleshoot_step = step_index + 1
                            progress_bar.progress(st.session_state.troubleshoot_step / max_steps if max_steps > 0 else 0)
            
            # Reset progress button
            if st.button("Reset Progress"):
                st.session_state.troubleshoot_step = 0
                st.rerun()
        
        # Resolution confirmation
        st.markdown("---")
        st.markdown("### 5️⃣ Resolution Confirmation")
        
        resolution_status = st.radio(
            "Has the issue been resolved?",
            ["Select an option", "Yes, issue resolved", "No, issue persists"],
            index=0
        )
        
        if resolution_status == "Yes, issue resolved":
            st.success("Great! The issue has been resolved. Remember to document this incident in your maintenance log.")
            
            # Additional clinical safety check
            st.markdown("""
            <div class="clinical-safety-check">
                <h4>❗ Clinical Safety Check</h4>
                <p>Before resuming treatment, verify:</p>
                <ul>
                    <li>All connections are secure</li>
                    <li>Dialysate temperature and conductivity are within range</li>
                    <li>Blood flow rate is set correctly</li>
                    <li>All alarms are functioning properly</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start New Troubleshooting Session"):
                reset_state()
                st.rerun()
                
        elif resolution_status == "No, issue persists":
            st.error("The issue persists. Consider the following options:")
            st.markdown("""
            1. Escalate to Technical Support
            2. Check for additional error codes
            3. Refer to manufacturer's service manual
            4. Replace the affected component
            5. In case of patient emergency, follow clinical protocol for returning blood and discontinuing treatment
            """)

def show_up7000_troubleshooting():
    st.markdown("""
    <div class="header">
        <h1>📊 UP-7000 Patient Monitor Troubleshooting</h1>
        <p class="subheader">Diagnose and resolve issues with patient monitoring systems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load UP-7000 data
    up7000_categories, error_details = load_up7000_data()
    
    # Sidebar for navigation
    with st.sidebar:
        st.image("https://img.freepik.com/free-vector/health-monitoring-abstract-concept-vector-illustration-remote-monitoring-device-smart-healthcare-diagnostic-system-wearable-technology-data-collection-personal-medical-service-abstract-metaphor_335657-2304.jpg", width=100)
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
            <strong>Technical Support:</strong> +1 (555) 456-7890</p>
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
        list(up7000_categories.keys()),
        index=0,
        key="category_select"
    )
    
    # Error selection
    st.markdown("### 2️⃣ Select Specific Error")
    selected_error = st.selectbox(
        "Choose the specific error:",
        up7000_categories[selected_category],
        index=0,
        key="error_select"
    )
    
    # Display error details
    if selected_error in error_details:
        st.markdown("### 3️⃣ Error Details")
        
        # Create a glowing box for the error name
        st.markdown(f"""
        <div class="glowing-box blue-glow">
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
        st.markdown(f"""
        <div class="info-box">
            <strong>📈 Clinical Impact:</strong> {error_details[selected_error]['impact']}
        </div>
        """, unsafe_allow_html=True)
        
        # Display steps
        st.markdown("### 4️⃣ Troubleshooting Steps")
        for i, step in enumerate(error_details[selected_error]['steps'], 1):
            # Animate the appearance of each step
            with st.empty():
                time.sleep(0.1)  # Small delay for animation effect
                st.markdown(f"""
                <div class="step-box animated-step blue-theme">
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
            
            if selected_category == "Display Issues":
                related_procedures.append("power_cycle")
                related_procedures.append("connections_check")
            
            elif selected_category == "ECG Issues":
                related_procedures.append("connections_check")
                related_procedures.append("system_check")
            
            elif selected_category == "NIBP (Blood Pressure) Issues":
                related_procedures.append("connections_check")
                related_procedures.append("system_check")
            
            elif selected_category == "SpO₂ (Oxygen Saturation) Issues":
                related_procedures.append("connections_check")
                related_procedures.append("system_check")
            
            elif selected_category == "CO₂ Monitoring Issues":
                related_procedures.append("connections_check")
                related_procedures.append("system_check")
            
            elif selected_category == "Printer Issues":
                related_procedures.append("power_cycle")
                related_procedures.append("connections_check")
            
            else:
                related_procedures.append("system_check")
                related_procedures.append("connections_check")
            
            # Add safety check for all procedures
            if "safety_systems" not in related_procedures:
                related_procedures.append("safety_systems")
            
            # Progress tracking
            current_step = st.session_state.get("troubleshoot_step", 0)
            max_steps = sum([len(common_procedures[p]["steps"]) for p in related_procedures])
            
            # Progress bar
            progress_bar = st.progress(current_step / max_steps if max_steps > 0 else 0)
            
            # Display procedures
            for proc_name in related_procedures:
                proc = common_procedures[proc_name]
                st.markdown(f"### {proc['title']}")
                
                for i, step in enumerate(proc['steps']):
                    step_index = sum([len(common_procedures[p]["steps"]) for p in related_procedures[:related_procedures.index(proc_name)]]) + i
                    
                    # Create a checkbox for each step
                    if st.checkbox(f"{step}", value=step_index < current_step, key=f"step_{proc_name}_{i}"):
                        if step_index >= current_step:
                            st.session_state.troubleshoot_step = step_index + 1
                            progress_bar.progress(st.session_state.troubleshoot_step / max_steps if max_steps > 0 else 0)
            
            # Reset progress button
            if st.button("Reset Progress"):
                st.session_state.troubleshoot_step = 0
                st.rerun()
        
        # Resolution confirmation
        st.markdown("---")
        st.markdown("### 5️⃣ Resolution Confirmation")
        
        resolution_status = st.radio(
            "Has the issue been resolved?",
            ["Select an option", "Yes, issue resolved", "No, issue persists"],
            index=0
        )
        
        if resolution_status == "Yes, issue resolved":
            st.success("Great! The issue has been resolved. Remember to document this incident in your maintenance log.")
            
            # Additional clinical safety check
            st.markdown("""
            <div class="clinical-safety-check blue-border">
                <h4>❗ Clinical Safety Check</h4>
                <p>Before returning to patient care, verify:</p>
                <ul>
                    <li>All waveforms are displaying normally</li>
                    <li>Alarms are properly configured and functional</li>
                    <li>Sensor readings are accurate</li>
                    <li>Data recording is functioning</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start New Troubleshooting Session"):
                reset_state()
                st.rerun()
                
        elif resolution_status == "No, issue persists":
            st.error("The issue persists. Consider the following options:")
            st.markdown("""
            1. Escalate to Technical Support
            2. Check for additional error codes
            3. Refer to manufacturer's service manual
            4. Replace the affected component or module
            5. Consider using backup monitoring equipment for critical patients
            """)

# Main app logic
# Main app logic
def main():
    # Apply custom CSS if available
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        margin-bottom: 20px;
    }
    .subheader {
        font-size: 1.2em;
        color: #555;
    }
    .machine-selection {
        margin-top: 30px;
    }
    .machine-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        transition: all 0.3s;
        background-color: #f9f9f9;
    }
    .machine-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }
    .machine-card img {
        width: 100%;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
        font-size: 0.8em;
        margin-top: 50px;
    }
    .glowing-box {
        position: relative;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4CAF50;
        margin-bottom: 20px;
        background-color: rgba(76, 175, 80, 0.05);
        overflow: hidden;
    }
    .red-glow {
        border: 1px solid #e74c3c;
        background-color: rgba(231, 76, 60, 0.05);
    }
    .blue-glow {
        border: 1px solid #3498db;
        background-color: rgba(52, 152, 219, 0.05);
    }
    .glow {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 5px;
        background: linear-gradient(90deg, #4CAF50, #8BC34A);
        animation: glow 1.5s infinite alternate;
    }
    .red-glow .glow {
        background: linear-gradient(90deg, #e74c3c, #ff9b95);
    }
    .blue-glow .glow {
        background: linear-gradient(90deg, #3498db, #85c1e9);
    }
    @keyframes glow {
        from {
            opacity: 0.8;
        }
        to {
            opacity: 0.3;
        }
    }
    .step-box {
        display: flex;
        margin-bottom: 15px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .step-number {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        font-weight: bold;
        display: flex;
        align-items: center;
        min-width: 80px;
        justify-content: center;
    }
    .red-theme .step-number {
        background-color: #e74c3c;
    }
    .blue-theme .step-number {
        background-color: #3498db;
    }
    .step-content {
        padding: 10px 15px;
        background-color: #f9f9f9;
        flex-grow: 1;
    }
    .animated-step {
        animation: fadeIn 0.5s;
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
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    .critical-reminder {
        background-color: #f8d7da;
        border: 2px dashed #dc3545;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .clinical-safety-check {
        background-color: #e9ecef;
        border: 2px solid #495057;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px;
    }
    .blue-border {
        border-color: #3498db;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check which machine is selected and display appropriate page
    if st.session_state.machine_selected is None:
        show_machine_selection()
    elif st.session_state.machine_selected == "PMS":
        show_pms_troubleshooting()
    elif st.session_state.machine_selected == "Hemodialysis":
        show_hemodialysis_troubleshooting()
    elif st.session_state.machine_selected == "UP7000":
        show_up7000_troubleshooting()

if __name__ == "__main__":
    main()
    
