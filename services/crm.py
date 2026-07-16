"""
HubSpot CRM Integration
Handles syncing leads, contacts, and deals with HubSpot.
"""

import requests
import json
from config.settings import settings


class CRMService:
    """
    HubSpot CRM client for managing contacts, deals, and pipelines.
    """

    def __init__(self):
        self.access_token = settings.HUBSPOT_ACCESS_TOKEN
        self.base_url = "https://api.hubapi.com"
        self.available = settings.has_hubspot

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def create_contact(self, email, first_name="", last_name="", phone=""):
        """
        Create or update a contact in HubSpot.
        Returns the contact ID.
        """
        if not self.available:
            return {"success": False, "error": "HubSpot not configured"}

        url = f"{self.base_url}/crm/v3/objects/contacts"
        properties = {"email": email}
        if first_name:
            properties["firstname"] = first_name
        if last_name:
            properties["lastname"] = last_name
        if phone:
            properties["phone"] = phone

        payload = {"properties": properties}

        try:
            response = requests.post(url, json=payload, headers=self._headers(), timeout=10)
            data = response.json()

            if response.status_code in [200, 201]:
                return {"success": True, "id": data.get("id"), "status": "created"}
            else:
                error_msg = data.get("message", "Unknown error")
                return {"success": False, "error": error_msg, "code": response.status_code}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def create_deal(self, deal_name, amount, contact_id, pipeline="default"):
        """
        Create a deal in HubSpot.
        """
        if not self.available:
            return {"success": False, "error": "HubSpot not configured"}

        url = f"{self.base_url}/crm/v3/objects/deals"
        payload = {
            "properties": {
                "dealname": deal_name,
                "amount": str(amount),
                "pipeline": pipeline,
                "dealstage": "appointmentscheduled",
            },
            "associations": [
                {
                    "to": {"id": contact_id},
                    "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 3}],
                }
            ],
        }

        try:
            response = requests.post(url, json=payload, headers=self._headers(), timeout=10)
            data = response.json()

            if response.status_code in [200, 201]:
                return {"success": True, "id": data.get("id"), "status": "created"}
            else:
                error_msg = data.get("message", "Unknown error")
                return {"success": False, "error": error_msg}

        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

    def sync_lead(self, name, email, phone, interest, message):
        """
        Sync a lead to HubSpot as a contact + deal.
        """
        if not self.available:
            return {"success": False, "error": "HubSpot not configured"}

        # Split name into first/last
        parts = name.strip().split(" ", 1)
        first_name = parts[0] if parts else ""
        last_name = parts[1] if len(parts) > 1 else ""

        # Create contact
        contact_result = self.create_contact(email, first_name, last_name, phone)
        if not contact_result.get("success"):
            return contact_result

        contact_id = contact_result["id"]

        # Create deal
        deal_result = self.create_deal(f"Lead: {name}", 0, contact_id)
        return deal_result

    def get_contacts(self, limit=10):
        """
        Fetch recent contacts from HubSpot.
        """
        if not self.available:
            return {"success": False, "error": "HubSpot not configured"}

        url = f"{self.base_url}/crm/v3/objects/contacts?limit={limit}"
        try:
            response = requests.get(url, headers=self._headers(), timeout=10)
            data = response.json()
            if response.status_code == 200:
                return {"success": True, "contacts": data.get("results", [])}
            else:
                return {"success": False, "error": data.get("message", "Unknown error")}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}


# Singleton instance
crm_service = CRMService()