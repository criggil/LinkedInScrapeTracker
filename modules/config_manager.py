import json
import os
import uuid

class ConfigManager:
    def __init__(self):
        self.config_file = "config/searches.json"
        self._ensure_config_directory()
        self._load_config()

    def _ensure_config_directory(self):
        """
        Create the config directory if it doesn't exist
        """
        os.makedirs("config", exist_ok=True)
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w') as f:
                json.dump({}, f)

    def _load_config(self):
        """
        Load the configuration from file
        """
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}

    def _save_config(self):
        """
        Save the configuration to file
        """
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def add_search(self, name, criteria, notify=False):
        """
        Add a new saved search
        """
        search_id = str(uuid.uuid4())
        self.config[search_id] = {
            'name': name,
            'criteria': criteria,
            'notify': notify
        }
        self._save_config()
        return search_id

    def get_all_searches(self):
        """
        Get all saved searches
        """
        return self.config

    def get_search(self, search_id):
        """
        Get a specific saved search
        """
        return self.config.get(search_id)

    def update_search(self, search_id, name=None, criteria=None, notify=None):
        """
        Update an existing saved search
        """
        if search_id not in self.config:
            return False
        
        if name is not None:
            self.config[search_id]['name'] = name
        if criteria is not None:
            self.config[search_id]['criteria'] = criteria
        if notify is not None:
            self.config[search_id]['notify'] = notify
        
        self._save_config()
        return True
