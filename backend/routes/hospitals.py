import math
from flask import Blueprint, request, jsonify

hospitals_bp = Blueprint('hospitals', __name__, url_prefix='/api/hospitals')

# Verified curated regional hospital nodes for major Indian hubs
MUNICIPAL_HOSPITALS = [
    # New Delhi
    {
        "id": "del-1",
        "name": "All India Institute of Medical Sciences (AIIMS)",
        "city": "New Delhi",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 28.5672,
        "lng": 77.2100,
        "address": "Sri Aurobindo Marg, Ansari Nagar, New Delhi 110029",
        "phone": "+91-11-26588500",
        "rating": 4.8,
        "hours": "24/7 Emergency Care"
    },
    {
        "id": "del-2",
        "name": "Safdarjung Hospital",
        "city": "New Delhi",
        "category": "Emergency Department",
        "has_emergency": True,
        "lat": 28.5702,
        "lng": 77.2078,
        "address": "Ring Road, opposite AIIMS, New Delhi 110029",
        "phone": "+91-11-26165060",
        "rating": 4.3,
        "hours": "24/7 Emergency & Trauma"
    },
    {
        "id": "del-3",
        "name": "Max Super Speciality Hospital",
        "city": "New Delhi",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 28.5284,
        "lng": 77.2114,
        "address": "1, 2, Press Enclave Marg, Saket, New Delhi 110017",
        "phone": "+91-11-26515050",
        "rating": 4.6,
        "hours": "24/7 Available"
    },
    # Mumbai
    {
        "id": "mum-1",
        "name": "KEM Hospital (King Edward Memorial)",
        "city": "Mumbai",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 19.0028,
        "lng": 72.8427,
        "address": "Acharya Donde Marg, Parel, Mumbai 400012",
        "phone": "+91-22-24107000",
        "rating": 4.5,
        "hours": "24/7 Emergency Care"
    },
    {
        "id": "mum-2",
        "name": "Lilavati Hospital & Research Centre",
        "city": "Mumbai",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 19.0514,
        "lng": 72.8291,
        "address": "A-791, Bandra Reclamation, Bandra West, Mumbai 400050",
        "phone": "+91-22-26751000",
        "rating": 4.6,
        "hours": "24/7 Emergency Care"
    },
    # Bengaluru
    {
        "id": "blr-1",
        "name": "NIMHANS Hospital",
        "city": "Bengaluru",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 12.9432,
        "lng": 77.5969,
        "address": "Hosur Road, Lakkasandra, Bengaluru 560029",
        "phone": "+91-80-26995000",
        "rating": 4.7,
        "hours": "24/7 Emergency Care"
    },
    {
        "id": "blr-2",
        "name": "Manipal Hospital",
        "city": "Bengaluru",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 12.9592,
        "lng": 77.6499,
        "address": "98, HAL Old Airport Rd, Kodihalli, Bengaluru 560017",
        "phone": "+91-80-25024444",
        "rating": 4.5,
        "hours": "24/7 Emergency Care"
    },
    # Hyderabad
    {
        "id": "hyd-1",
        "name": "Apollo Hospitals Jubilee Hills",
        "city": "Hyderabad",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 17.4172,
        "lng": 78.4116,
        "address": "Road No. 72, Film Nagar, Jubilee Hills, Hyderabad 500033",
        "phone": "+91-40-23607777",
        "rating": 4.6,
        "hours": "24/7 Emergency Care"
    },
    # Pune
    {
        "id": "pun-1",
        "name": "Ruby Hall Clinic",
        "city": "Pune",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 18.5323,
        "lng": 73.8778,
        "address": "40, Sassoon Rd, Sangamvadi, Pune 411001",
        "phone": "+91-20-66455100",
        "rating": 4.5,
        "hours": "24/7 Emergency Care"
    },
    # Chennai
    {
        "id": "chn-1",
        "name": "Apollo Main Hospital Greams Road",
        "city": "Chennai",
        "category": "Hospital",
        "has_emergency": True,
        "lat": 13.0604,
        "lng": 80.2518,
        "address": "21 Greams Lane, Thousand Lights, Chennai 600006",
        "phone": "+91-44-28290200",
        "rating": 4.7,
        "hours": "24/7 Emergency Care"
    }
]

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in kilometers between two GPS coordinates."""
    r = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(r * c, 2)

@hospitals_bp.route('', methods=['GET'])
def search_hospitals():
    user_lat = request.args.get('lat', type=float)
    user_lng = request.args.get('lng', type=float)
    city_filter = request.args.get('city', '').strip().lower()
    category_filter = request.args.get('category', '').strip().lower()
    
    results = []
    for h in MUNICIPAL_HOSPITALS:
        if city_filter and city_filter not in h["city"].lower() and city_filter not in h["address"].lower():
            continue
        if category_filter and category_filter not in h["category"].lower():
            continue
            
        dist_km = None
        if user_lat is not None and user_lng is not None:
            dist_km = calculate_haversine_distance(user_lat, user_lng, h["lat"], h["lng"])
            
        results.append({
            **h,
            "distance_km": dist_km,
            "distance_display": f"{dist_km} km away" if dist_km is not None else "Distance calculated upon location permission"
        })
        
    if user_lat is not None and user_lng is not None:
        results.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else 99999)
        
    return jsonify({
        "success": True,
        "count": len(results),
        "hospitals": results,
        "emergency_disclaimer": "⚠️ IN LIFE-THREATENING EMERGENCIES: Dial emergency services immediately (India: 108 or 112) rather than waiting for map routing."
    })
