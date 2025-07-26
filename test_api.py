#!/usr/bin/env python3
"""
Simple test script to debug the issue creation API
"""

import requests
import json

# API base URL
BASE_URL = "https://issue-tracker-jywg.onrender.com/api"

def test_get_services():
    """Test getting all services"""
    print("=== Testing GET /api/services/ ===")
    try:
        response = requests.get(f"{BASE_URL}/services/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            services = response.json()
            print(f"Found {len(services)} services:")
            for service in services:
                print(f"  - ID: {service.get('id')}")
                print(f"    Name: {service.get('name')}")
                print(f"    Description: {service.get('description')}")
                print()
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def test_get_offices():
    """Test getting all offices"""
    print("=== Testing GET /api/offices/ ===")
    try:
        response = requests.get(f"{BASE_URL}/offices/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            offices = response.json()
            print(f"Found {len(offices)} offices:")
            for office in offices:
                print(f"  - ID: {office.get('id')}")
                print(f"    Name: {office.get('name')}")
                print(f"    Location: {office.get('location')}")
                print()
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def test_get_users():
    """Test getting all users"""
    print("=== Testing GET /api/users/ ===")
    try:
        response = requests.get(f"{BASE_URL}/users/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"Found {len(users)} users:")
            for user in users:
                print(f"  - ID: {user.get('id')}")
                print(f"    Username: {user.get('username')}")
                print(f"    Phone: {user.get('phone_number')}")
                print()
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def test_create_service():
    """Test creating a service"""
    print("=== Testing POST /api/services/create/ ===")
    service_data = {
        "name": "IT Support",
        "description": "IT and technical support services"
    }
    try:
        response = requests.post(f"{BASE_URL}/services/create/", json=service_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"Service created successfully!")
            print(f"ID: {result.get('id')}")
            print(f"Name: {result.get('name')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

def test_create_issue_with_valid_data():
    """Test creating an issue with valid data"""
    print("=== Testing POST /api/issues/create/ with valid data ===")
    
    # First get available services
    services_response = requests.get(f"{BASE_URL}/services/")
    if services_response.status_code != 200:
        print("Cannot get services, skipping issue creation test")
        return
    
    services = services_response.json()
    if not services:
        print("No services available, creating one first...")
        test_create_service()
        services_response = requests.get(f"{BASE_URL}/services/")
        services = services_response.json()
    
    if services:
        service_id = services[0]['id']
        issue_data = {
            "type": "Test Issue",
            "description": "This is a test issue for debugging",
            "status": "unsolved",
            "service": service_id
        }
        
        try:
            response = requests.post(f"{BASE_URL}/issues/create/", json=issue_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print(f"Issue created successfully!")
                print(f"ID: {result.get('id')}")
                print(f"Type: {result.get('type')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    print("API Debug Test Script")
    print("=" * 50)
    
    # Test getting available data
    test_get_services()
    test_get_offices()
    test_get_users()
    
    # Test creating service if needed
    test_create_service()
    
    # Test creating issue
    test_create_issue_with_valid_data() 