"""
Checklist management for Rex HVAC System
Manages jobs, units, and reading data
"""

import json
import os
from datetime import datetime
from copy import deepcopy
from config import CHECKLISTS, DATA_DIR

class JobManager:
    """Manages HVAC jobs, units, and readings"""
    
    def __init__(self):
        self.current_job = None
        self.jobs = {}
        self.ensure_data_dir()
        self.load_saved_jobs()
    
    def ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            print(f"Created data directory: {DATA_DIR}")
    
    def create_job_with_units(self, job_name, unit_types):
        """Create a new HVAC job with mixed unit types"""
        self.current_job = {
            "name": job_name,
            "created": datetime.now().isoformat(),
            "units": {}
        }
        
        # Initialize units with their specific system types
        for unit_num, system_type in unit_types.items():
            self.current_job["units"][unit_num] = {
                "unit_number": unit_num,
                "system_type": system_type,
                "readings": {},
                "notes": ""
            }
            # Initialize checklist items for this unit's system type
            for item in CHECKLISTS[system_type]:
                self.current_job["units"][unit_num]["readings"][item] = {
                    "value": "",
                    "notes": "",
                    "checked": False
                }
        
        return self.current_job
    
    def get_current_job(self):
        """Get the current active job"""
        return self.current_job
    
    def set_current_job(self, job):
        """Set the current active job"""
        self.current_job = job
    
    def get_unit(self, unit_number):
        """Get a specific unit from current job"""
        if self.current_job and unit_number in self.current_job["units"]:
            return self.current_job["units"][unit_number]
        return None
    
    def update_reading(self, unit_number, item_name, value, notes=""):
        """Update a reading for a unit"""
        if self.current_job and unit_number in self.current_job["units"]:
            if item_name in self.current_job["units"][unit_number]["readings"]:
                self.current_job["units"][unit_number]["readings"][item_name] = {
                    "value": value,
                    "notes": notes,
                    "checked": True
                }
                return True
        return False
    
    def get_reading(self, unit_number, item_name):
        """Get a reading value for a unit"""
        unit = self.get_unit(unit_number)
        if unit and item_name in unit["readings"]:
            return unit["readings"][item_name]
        return None
    
    def save_job(self, job_name=None):
        """Save current job to file"""
        if not self.current_job:
            print("ERROR: No current job to save")
            return False
        
        self.ensure_data_dir()
        
        # Create filename with timestamp
        base_name = job_name or self.current_job["name"]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{base_name}_{timestamp}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(self.current_job, f, indent=2)
            print(f"Job saved successfully: {filepath}")
            
            # Reload saved jobs to update the list
            self.load_saved_jobs()
            return True
        except Exception as e:
            print(f"Error saving job: {e}")
            return False
    
    def load_saved_jobs(self):
        """Load all saved jobs from directory"""
        self.jobs = {}
        if not os.path.exists(DATA_DIR):
            print(f"Data directory not found: {DATA_DIR}")
            return
        
        try:
            files = os.listdir(DATA_DIR)
            print(f"Found {len(files)} files in {DATA_DIR}")
            for filename in files:
                if filename.endswith(".json"):
                    filepath = os.path.join(DATA_DIR, filename)
                    try:
                        with open(filepath, 'r') as f:
                            job = json.load(f)
                            self.jobs[filename] = job
                            print(f"Loaded job: {filename}")
                    except Exception as e:
                        print(f"Error loading job {filename}: {e}")
        except Exception as e:
            print(f"Error reading data directory: {e}")
    
    def get_saved_jobs(self):
        """Return list of saved jobs"""
        jobs_list = list(self.jobs.keys())
        print(f"get_saved_jobs() returning: {jobs_list}")
        return jobs_list
    
    def load_job(self, job_filename):
        """Load a saved job as current job"""
        if job_filename in self.jobs:
            # Make a deep copy to avoid aliasing issues
            self.current_job = deepcopy(self.jobs[job_filename])
            
            # Convert unit keys from strings back to integers
            # (JSON serialization converts int keys to strings)
            if "units" in self.current_job:
                new_units = {}
                for k, v in self.current_job["units"].items():
                    unit_key = int(k) if isinstance(k, str) else k
                    new_units[unit_key] = v
                self.current_job["units"] = new_units
            
            print(f"Loaded current job: {job_filename}")
            return True
        print(f"Job not found: {job_filename}")
        return False



    
    def get_job_summary(self):
        """Get summary of current job"""
        if not self.current_job:
            return None
        
        return {
            "name": self.current_job["name"],
            "created": self.current_job["created"],
            "num_units": len(self.current_job["units"])
        }

# Test
if __name__ == "__main__":
    print("checklist.py loaded successfully")
