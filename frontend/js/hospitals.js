/**
 * MediR AI - Nearby Hospital Finder with Interactive Leaflet Map
 */

let mapInstance = null;
let markersGroup = null;
let userCoordinates = null;

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  setupLocationButton();
  setupCitySelector();
  setupCategoryFilter();
  // Fetch default hospital listings
  fetchHospitals();
});

function initMap() {
  const mapEl = document.getElementById('hospitalMap');
  if (!mapEl) return;

  // Default center: New Delhi
  mapInstance = L.map('hospitalMap').setView([28.5672, 77.2100], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors | MediR'
  }).addTo(mapInstance);

  markersGroup = L.layerGroup().addTo(mapInstance);
}

function setupLocationButton() {
  const gpsBtn = document.getElementById('btnDetectLocation');
  if (!gpsBtn) return;

  gpsBtn.addEventListener('click', () => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser.");
      return;
    }

    gpsBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Locating...';

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        userCoordinates = {
          lat: pos.coords.latitude,
          lng: pos.coords.longitude
        };

        gpsBtn.innerHTML = '<i class="bi bi-geo-alt-fill"></i> Location Detected';
        gpsBtn.classList.replace('btn-outline-primary', 'btn-success');

        // Center map on user
        mapInstance.setView([userCoordinates.lat, userCoordinates.lng], 13);
        
        // Add user marker
        L.marker([userCoordinates.lat, userCoordinates.lng], {
          icon: L.divIcon({
            className: 'user-gps-marker',
            html: '<div style="background-color: #0284c7; width: 18px; height: 18px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 8px rgba(0,0,0,0.4);"></div>'
          })
        }).addTo(mapInstance).bindPopup("<strong>You are here</strong>").openPopup();

        fetchHospitals(userCoordinates.lat, userCoordinates.lng);
      },
      (err) => {
        gpsBtn.innerHTML = '<i class="bi bi-geo-alt"></i> Use GPS Location';
        alert("Location access denied or timed out. Please select a city manually from the dropdown.");
      },
      { timeout: 10000 }
    );
  });
}

function setupCitySelector() {
  const citySelect = document.getElementById('hospitalCitySelect');
  if (!citySelect) return;

  citySelect.addEventListener('change', () => {
    const city = citySelect.value;
    fetchHospitals(userCoordinates?.lat, userCoordinates?.lng, city);
  });
}

function setupCategoryFilter() {
  const catSelect = document.getElementById('hospitalCategorySelect');
  if (!catSelect) return;

  catSelect.addEventListener('change', () => {
    const city = document.getElementById('hospitalCitySelect')?.value || '';
    fetchHospitals(userCoordinates?.lat, userCoordinates?.lng, city, catSelect.value);
  });
}

function fetchHospitals(lat = null, lng = null, city = '', category = '') {
  let url = '/api/hospitals?';
  if (lat && lng) url += `lat=${lat}&lng=${lng}&`;
  if (city) url += `city=${encodeURIComponent(city)}&`;
  if (category) url += `category=${encodeURIComponent(category)}&`;

  fetch(url)
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        renderHospitalsList(data.hospitals);
        renderMapMarkers(data.hospitals);
      }
    })
    .catch(() => alert("Failed to retrieve nearby hospital locations."));
}

function renderHospitalsList(hospitals) {
  const listContainer = document.getElementById('hospitalCardsContainer');
  if (!listContainer) return;

  if (hospitals.length === 0) {
    listContainer.innerHTML = '<div class="alert alert-info">No medical facilities found matching your search.</div>';
    return;
  }

  listContainer.innerHTML = hospitals.map(h => `
    <div class="hospital-card" onclick="focusHospital(${h.lat}, ${h.lng})">
      <div class="d-flex justify-content-between align-items-start mb-1">
        <h5 class="fw-bold mb-0 text-primary">${h.name}</h5>
        ${h.has_emergency ? '<span class="badge bg-danger">24/7 Emergency</span>' : ''}
      </div>
      <p class="small text-muted mb-2"><i class="bi bi-geo-alt"></i> ${h.address}</p>
      <div class="d-flex justify-content-between align-items-center small mb-2">
        <span class="text-success fw-bold"><i class="bi bi-star-fill text-warning"></i> ${h.rating} / 5</span>
        <span class="fw-bold text-secondary">${h.distance_display}</span>
      </div>
      <div class="d-flex gap-2 mt-2">
        <a href="tel:${h.phone}" class="btn btn-sm btn-outline-success"><i class="bi bi-telephone"></i> Call</a>
        <a href="https://www.google.com/maps/dir/?api=1&destination=${h.lat},${h.lng}" target="_blank" class="btn btn-sm btn-outline-primary">
          <i class="bi bi-compass"></i> Directions
        </a>
      </div>
    </div>
  `).join('');
}

function renderMapMarkers(hospitals) {
  if (!markersGroup || !mapInstance) return;
  markersGroup.clearLayers();

  if (hospitals.length === 0) return;

  const bounds = [];
  hospitals.forEach(h => {
    const marker = L.marker([h.lat, h.lng])
      .bindPopup(`
        <strong>${h.name}</strong><br>
        ${h.address}<br>
        <strong>Phone:</strong> <a href="tel:${h.phone}">${h.phone}</a><br>
        ${h.has_emergency ? '<span class="badge bg-danger text-white">24/7 Emergency</span>' : ''}
      `);
    markersGroup.addLayer(marker);
    bounds.push([h.lat, h.lng]);
  });

  if (bounds.length > 0) {
    mapInstance.fitBounds(bounds, { padding: [40, 40] });
  }
}

function focusHospital(lat, lng) {
  if (mapInstance) {
    mapInstance.setView([lat, lng], 15);
  }
}
