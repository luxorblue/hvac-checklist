"""
Diagnostic script to check saved job data
"""

import json
import os
from config import DATA_DIR

def check_saved_jobs():
    """Check what's actually in the saved job files"""
    print("=" * 60)
    print("CHECKING SAVED JOB FILES")
    print("=" * 60)
    
    if not os.path.exists(DATA_DIR):
        print(f"Data directory not found: {DATA_DIR}")
        return
    
    files = os.listdir(DATA_DIR)
    print(f"\nFound {len(files)} files in {DATA_DIR}:")
    
    for filename in files:
        if filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            print(f"\n--- {filename} ---")
            
            try:
                with open(filepath, 'r') as f:
                    job = json.load(f)
                
                print(f"Job name: {job.get('name', 'N/A')}")
                print(f"Units in file: {list(job.get('units', {}).keys())}")
                
                # Check first unit
                units = job.get('units', {})
                if units:
                    first_unit_key = list(units.keys())[0]
                    first_unit = units[first_unit_key]
                    
                    print(f"\nFirst unit key: '{first_unit_key}' (type: {type(first_unit_key).__name__})")
                    print(f"Unit number: {first_unit.get('unit_number')}")
                    print(f"System type: {first_unit.get('system_type')}")
                    
                    readings = first_unit.get('readings', {})
                    print(f"Number of readings: {len(readings)}")
                    
                    if readings:
                        print("\nFirst 3 readings:")
                        for i, (item_name, reading_data) in enumerate(list(readings.items())[:3]):
                            print(f"  - {item_name}: value='{reading_data.get('value')}', checked={reading_data.get('checked')}")
                    else:
                        print("NO READINGS FOUND!")
                        
            except Exception as e:
                print(f"Error reading file: {e}")

if __name__ == "__main__":
    check_saved_jobs()
