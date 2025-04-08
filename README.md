# Hemodialysis Machine Troubleshooting Assistant

## Project Overview

This Streamlit application serves as an AI-powered diagnostic support tool for biomedical engineers working with hemodialysis machines. The application provides troubleshooting guidance for various alarms and issues that can occur during hemodialysis procedures, helping technicians quickly identify and resolve problems to ensure patient safety and minimize treatment disruptions.

## Features

### Core Functionality
- **Machine State Selection**: Choose the current operational state of the machine
- **Alarm/Issue Selection**: Select from a list of known alarms or issues based on the machine state
- **Guided Troubleshooting**: View step-by-step instructions to diagnose and resolve the issue
- **Interactive Troubleshooting Mode**: For complex problems, use the detailed interactive guide with progress tracking
- **Technical Resources**: Access common reference points, documentation links, and testing information

### User Experience
- **Modern, Responsive UI**: Clean interface with animations and visual feedback
- **Progress Tracking**: Follow your troubleshooting progress with visual indicators
- **Contextual Help**: Different troubleshooting paths based on alarm types
- **Resolution Confirmation**: Verify whether the issue has been resolved

## Technical Details

### Data Management
- **Excel-Based Knowledge Base**: Troubleshooting steps are stored in a structured Excel file
- **Dynamic Content Loading**: Procedures are loaded based on machine state and alarm type
- **Cached Data Access**: Efficient data handling with Streamlit's caching mechanism

### UI Components
- **Custom CSS**: Enhanced visual styling with animations and responsive design
- **Interactive Elements**: Checkboxes, progress bars, and expandable sections
- **Glowing Alarm Display**: Visual emphasis on the current alarm being diagnosed
- **Animated Step Appearance**: Steps appear with a sliding animation for better readability

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hemodialysis-troubleshooting.git
   cd hemodialysis-troubleshooting
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Prepare your data file:
   - Ensure you have the `MachineDataAnalytics.xlsx` file in the project directory
   - The Excel file should contain sheets for different machine states and columns for alarms and troubleshooting steps

4. Create a `style.css` file in the project directory with the provided CSS code

5. Run the application:
   ```
   streamlit run app.py
   ```

## Dependencies

- streamlit
- pandas
- openpyxl
- time

## File Structure

```
├── app.py                     # Main application code
├── style.css                  # CSS styling for the application
├── MachineDataAnalytics.xlsx  # Excel file with troubleshooting data
├── requirements.txt           # Dependencies list
└── README.md                  # Project documentation
```

## Excel File Format

The application expects an Excel file with the following structure:

- Each sheet represents a different machine state
- Each sheet contains columns:
  - `Alarms / Reasons`: The name of the alarm or issue
  - `Reason 1` through `Reason 10`: Step-by-step troubleshooting instructions

## Common Troubleshooting Procedures

The application includes built-in procedures for common issues:

1. **Power Cycling Procedure**:
   - Safe power-down and restart sequence
   - Capacitor discharge waiting period
   - Boot sequence verification

2. **Fluid System Check**:
   - Verification of all fluid pathways and connections
   - Dialysate concentrate inspection
   - Water supply validation

3. **Pressure System Testing**:
   - Diagnostic tests for pressure-related components
   - Transducer connection verification
   - Pressure sensor calibration checks

4. **Safety Systems Check**:
   - Verification of critical safety sensors and alarms
   - Blood leak detector testing
   - Air detector validation

## Usage Instructions

1. Select the current machine state from the dropdown
2. Choose the specific alarm or issue you're troubleshooting
3. Follow the guided steps provided by the application
4. For complex issues, enable the interactive troubleshooting mode
5. Mark steps as completed as you perform them
6. Confirm resolution or get escalation guidance if needed
7. Access technical resources for additional support

## User Roles

This application is designed primarily for:
- Biomedical Engineering Technicians
- Hospital Equipment Maintenance Staff
- Dialysis Center Technical Personnel
- Field Service Engineers

## Safety Considerations

- The application provides guidance only and does not replace proper training
- Always follow hospital protocols and manufacturer guidelines
- Ensure proper PPE is worn when servicing medical equipment
- Document all maintenance actions in appropriate logs

## Future Enhancements

- Integration with machine logs for automated diagnosis
- Mobile-optimized interface for technicians on the move
- Machine learning-based prediction of potential failures
- Barcode/QR code scanning for quick machine identification
- Integration with inventory systems for parts ordering

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Inspired by the need for faster troubleshooting in critical care settings
- Special thanks to the biomedical engineering community for their input
- Icon credits: [Flaticon](https://www.flaticon.com)

## Contact

For support or questions, please contact:
- Email: dhineshsaff@gmail.com
- GitHub Issues: [Create a new issue](https://github.com/yourusername/hemodialysis-troubleshooting/issues)

---

**Note**: This application is for educational and support purposes only. Always refer to manufacturer documentation for official troubleshooting procedures.
