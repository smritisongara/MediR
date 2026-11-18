/**
 * MediR AI - Nearby Hospital Finder Controller
 */

let mapInstance = null;
let markersGroup = null;
let userCoordinates = null;
let activeCategory = 'all';

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  setupGpsButton();
  setupSearchInput();
  setupCityDropdown();
  setupCategoryFilters();
  fetchHospitals();
});

function initMap() {
  const mapEl = document.getElementById('hospitalMap');
  if (!mapEl) return;

  // Initial center: New Delhi
  mapInstance = L.map('hospitalMap').setView([28.5672, 77.2100], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors | MediR AI'
  }).addTo(mapInstance);

  markersGroup = L.layerGroup().addTo(mapInstance);
}

function setupGpsButton() {
  const gpsBtn = document.getElementById('btnGpsLocate');
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
        gpsBtn.classList.replace('btn-medir-secondary', 'btn-success');

        mapInstance.setView([userCoordinates.lat, userCoordinates.lng], 13);

        // Add GPS user marker
        L.marker([userCoordinates.lat, userCoordinates.lng], {
          icon: L.divIcon({
            className: 'user-pin-marker',
            html: '<div style="background-color: #198754; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(0,0,0,0.4);"></div>'
          })
        }).addTo(mapInstance).bindPopup("<strong>Your Detected Location</strong>").openPopup();

        fetchHospitals();
      },
      (err) => {
        gpsBtn.innerHTML = '<i class="bi bi-geo-alt"></i> Use GPS Location';
        alert("GPS location permission was denied. You can search by City or PIN code in the search bar.");
      },
      { timeout: 10000 }
    );
  });
}

function setupSearchInput() {
  const searchInput = document.getElementById('hospitalSearchInput');
  const searchBtn = document.getElementById('btnSearchHospitals');

  if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', () => fetchHospitals());
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') fetchHospitals();
    });
  }
}

function setupCityDropdown() {
  const citySelect = document.getElementById('hospitalCityDropdown');
  if (citySelect) {
    citySelect.addEventListener('change', () => fetchHospitals());
  }
}

function setupCategoryFilters() {
  document.querySelectorAll('.filter-category-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.filter-category-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeCategory = btn.getAttribute('data-cat') || 'all';
      fetchHospitals();
    });
  });
}

function fetchHospitals() {
  const query = document.getElementById('hospitalSearchInput')?.value.trim() || '';
  const city = document.getElementById('hospitalCityDropdown')?.value || '';

  let url = '/api/hospitals?';
  if (query) url += `q=${encodeURIComponent(query)}&`;
  if (city) url += `city=${encodeURIComponent(city)}&`;
  if (activeCategory && activeCategory !== 'all') url += `category=${encodeURIComponent(activeCategory)}&`;
  if (userCoordinates) {
    url += `lat=${userCoordinates.lat}&lng=${userCoordinates.lng}&`;
  }

  fetch(url)
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        renderHospitalCards(data.hospitals);
        renderMapMarkers(data.hospitals);
      }
    })
    .catch(() => alert("Failed to retrieve nearby hospitals."));
}

function renderHospitalCards(hospitals) {
  const container = document.getElementById('hospitalListContainer');
  const countBadge = document.getElementById('hospitalCountBadge');
  if (!container) return;

  if (countBadge) countBadge.innerText = hospitals.length;

  if (hospitals.length === 0) {
    container.innerHTML = `
      <div class="alert alert-info text-center py-4">
        <i class="bi bi-info-circle display-6 d-block mb-2"></i>
        <strong>No medical facilities found</strong> matching your search criteria.
        <p class="small mb-0 mt-1">Try searching by City (e.g. New Delhi, Mumbai) or selecting 'All Facilities'.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = hospitals.map(h => `
    <div class="hospital-card" id="card-${h.id}">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <div>
          <h5 class="fw-bold text-success mb-1">${h.name}</h5>
          <span class="badge ${h.ownership === 'Government' ? 'bg-primary' : 'bg-success'} me-1">${h.ownership}</span>
          <span class="badge bg-secondary me-1">${h.type}</span>
          ${h.has_emergency ? '<span class="badge bg-danger">24/7 Emergency</span>' : ''}
        </div>
        <div class="text-end">
          <span class="text-warning fw-bold"><i class="bi bi-star-fill"></i> ${h.rating}</span>
          <div class="small text-muted">(${h.review_count} reviews)</div>
        </div>
      </div>

      <!-- Complete Street Address Breakdown -->
      <div class="p-2 rounded mb-2 small" style="background-color: var(--mint-bg);">
        <i class="bi bi-geo-alt-fill text-danger me-1"></i>
        <strong>Complete Address:</strong> ${h.full_address}
        <div class="text-muted mt-1">
          <strong>Building/Road:</strong> ${h.building_no}, ${h.road} &bull; 
          <strong>PIN Code:</strong> <span class="badge bg-light text-dark border">${h.pincode}</span>
        </div>
      </div>

      <!-- Distance and Travel Time -->
      <div class="d-flex justify-content-between align-items-center small text-muted mb-2">
        <span><i class="bi bi-car-front-fill text-success"></i> ${h.estimated_travel_time}</span>
        <span class="fw-bold" style="color: var(--primary-green);">${h.distance_display}</span>
      </div>

      <!-- Opening Hours / Status -->
      <div class="small text-muted mb-3">
        <i class="bi bi-clock-history me-1 text-primary"></i> <strong>Hours:</strong> ${h.opening_hours} 
        <span class="text-success ms-1">(${h.current_status})</span>
      </div>

      <!-- Action Buttons -->
      <div class="d-flex flex-wrap gap-2 pt-2 border-top">
        <a href="hospital-details.html?id=${h.id}" class="btn btn-sm btn-medir-primary">
          <i class="bi bi-card-text"></i> View Details
        </a>
        <button onclick="focusHospital(${h.lat}, ${h.lng}, '${h.id}')" class="btn btn-sm btn-outline-success">
          <i class="bi bi-pin-map"></i> View on Map
        </button>
        <a href="${h.google_maps_url}" target="_blank" class="btn btn-sm btn-outline-primary">
          <i class="bi bi-compass"></i> Directions
        </a>
        <a href="tel:${h.phone}" class="btn btn-sm btn-outline-secondary">
          <i class="bi bi-telephone"></i> Call
        </a>
        ${h.website ? `<a href="${h.website}" target="_blank" class="btn btn-sm btn-outline-dark"><i class="bi bi-globe"></i> Website</a>` : ''}
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
        <div style="min-width: 200px;">
          <h6 class="fw-bold mb-1" style="color: #198754;">${h.name}</h6>
          <div class="small text-muted mb-2">${h.full_address}</div>
          <div class="small mb-1"><strong>Phone:</strong> <a href="tel:${h.phone}">${h.phone}</a></div>
          <div class="small mb-2"><strong>Status:</strong> ${h.current_status}</div>
          <a href="hospital-details.html?id=${h.id}" class="btn btn-sm btn-success text-white py-0 px-2 w-100">
            View Full Hospital Details
          </a>
        </div>
      `);
    markersGroup.addLayer(marker);
    bounds.push([h.lat, h.lng]);
  });

  if (bounds.length > 0) {
    mapInstance.fitBounds(bounds, { padding: [40, 40] });
  }
}

function focusHospital(lat, lng, cardId) {
  if (mapInstance) {
    mapInstance.setView([lat, lng], 15);
  }
  const el = document.getElementById(`card-${cardId}`);
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    el.style.borderColor = 'var(--primary-green)';
  }
}
