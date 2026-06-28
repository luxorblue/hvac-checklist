# Rex HVAC Checklist - Development Progress

## Session 1: June 28, 2026 - Initial Build ✅

### Completed Features ✅
- **Core GUI Framework**
  - Tkinter GUI optimized for Raspberry Pi 5 with 4.3" touchscreen (800x480)
  - Main menu with job management
  - Grid-based layout with fixed header, expandable content, fixed footer
  - Navigation buttons always visible

- **Job Management**
  - Create new jobs with custom name
  - Specify number of units (1-10)
  - Assign different system types to each unit (Heat Pump System, Furnace System)
  - Mixed unit types in single job

- **Checklist System**
  - Dynamic checklist based on system type:
    - Heat Pump System: 15 items
    - Furnace System: 18 items (includes furnace-specific)
  - Checkbox system for item completion
  - Value input fields for readings
  - Scrollable interface for many items

- **Data Persistence**
  - Save jobs to JSON files in `job_data/` directory
  - Load saved jobs from disk
  - View list of all saved jobs
  - Resume previously saved jobs with all data intact
  - Timestamps on saved files for version tracking

- **Navigation**
  - Main menu with 3 buttons: Start New Job, View Saved Jobs, Exit
  - Unit selector with visual feedback (green for active, blue for inactive)
  - Save Job and Back to Menu buttons always visible
  - Back button on saved jobs screen

### Current State
- ✅ 2 test jobs saved successfully
- ✅ Jobs can be loaded and reopened
- ✅ Full navigation workflow tested
- ✅ Touchscreen interaction working smoothly

### Known Issues / Limitations
- Saved jobs don't show which items were checked when reloaded (displays empty checklist)
- Voice input not yet integrated
- No quick "Resume Last Job" button on main menu
- Job list doesn't show useful metadata (unit count, system types)
- No export/report generation (CSV, PDF)

---

## TODO - Next Sessions 🚀

### High Priority (Recommended Next)
- [ ] **Display Saved Data on Load**
  - When loading a saved job, show previously entered values and checked items
  - Verify all readings persist correctly
  - Add visual indicator for complete items

- [ ] **Voice Input Integration**
  - Test Bluetooth microphone connection
  - Implement `voice.py` voice input with `speech_recognition`
  - Add "Record Reading" button to each checklist item
  - Implement voice commands (exit, save, next, skip)

- [ ] **Quick Resume Job**
  - Add "Resume Active Job" button to main menu
  - Show last active job name/units in status
  - Eliminate need to go through "View Saved Jobs" every time

### Medium Priority
- [ ] **Job Details Display**
  - Show unit count in saved jobs list
  - Show system types for each unit
  - Better formatted filenames or job summaries

- [ ] **Data Validation & Error Handling**
  - Input validation for reading values (numeric where needed)
  - Prevent accidental job overwrites
  - Recovery from corrupted JSON files

- [ ] **UI Enhancements**
  - Larger buttons/text for easier touchscreen tapping
  - Add job details summary screen before saving
  - Progress indicator for multi-unit jobs

### Low Priority / Future Features
- [ ] **Export/Reporting**
  - Export job to CSV
  - Generate PDF report with all readings
  - Email reports directly from Pi

- [ ] **Cloud Sync**
  - Backup jobs to cloud storage (Dropbox, Google Drive)
  - Sync between multiple devices
  - Version history

- [ ] **Advanced Features**
  - Photo/video attachment to readings
  - Handwritten notes with touchscreen
  - Offline mode with sync when online
  - Job templates for common configurations

- [ ] **Testing & Optimization**
  - Performance testing with large datasets
  - Battery optimization for long job days
  - Stress testing voice input in loud environments

---

## Architecture Notes

### File Structure
```
hvac-checklist/
├── main.py              # Entry point - initializes all components
├── ui.py                # Tkinter GUI - handles all user interaction
├── checklist.py         # JobManager - manages jobs, units, readings
├── voice.py             # VoiceHandler - speech recognition and TTS
├── config.py            # Configuration - system types, checklists, UI settings
├── job_data/            # Directory for saved JSON job files
└── TODO.md              # This file
```

### Key Classes
- **JobManager** (checklist.py)
  - `create_job_with_units()` - Create job with mixed unit types
  - `update_reading()` - Save reading values
  - `save_job()` - Persist to JSON
  - `load_job()` - Restore from JSON

- **VoiceHandler** (voice.py)
  - `listen()` - Capture speech from Bluetooth mic
  - `speak()` - Output via text-to-speech
  - `voice_command()` - Parse voice commands

- **UI** (ui.py)
  - `show_active_job()` - Display checklist screen
  - `show_unit_checklist()` - Render individual unit's items
  - `save_job()` / `load_saved_job()` - Handle data persistence UI

### Checklist Configuration (config.py)
```python
SYSTEM_TYPES = ["Heat Pump System", "Furnace System"]

COMMON_CHECKLIST = [
    "Outdoor fan capacitor",
    "Compressor capacitor",
    ...
]

FURNACE_ONLY_CHECKLIST = [
    "Inducer motor",
    "Furnace safeties",
    "CO detector",
]

CHECKLISTS = {
    "Heat Pump System": COMMON_CHECKLIST.copy(),
    "Furnace System": COMMON_CHECKLIST + FURNACE_ONLY_CHECKLIST,
}
```

---

## Testing Notes

### Tested Workflows ✅
1. Start new job → Enter name → Select units → Choose system types → View checklist → Save → Load
2. View saved jobs → Load previous job → See job details
3. Switch between units → Enter values → Save job
4. Back button navigation

### Not Yet Tested ❌
- Voice input (no Bluetooth mic connected yet)
- Large jobs (10 units with many items)
- Rapid user interactions
- Edge cases (corrupted files, missing directory)

---

## Hardware Setup

### Target Hardware
- **Device:** Raspberry Pi 5
- **Display:** OSOYOO 4.3" DSI Touchscreen (800x480)
- **Audio:** Bluetooth microphone (for voice input)
- **Optional:** Thermal camera, multimeter interface

### Dependencies
- `tkinter` - GUI framework
- `speech_recognition` - Voice input
- `espeak` - Text-to-speech

---

## Notes for Next Session
- Start by testing if saved job data displays correctly (priority #1)
- If data shows empty, debug the `update_reading()` and `save_job()` flow
- Then integrate voice input using the Bluetooth mic
- Consider adding a "Quick Stats" screen showing completed items %
