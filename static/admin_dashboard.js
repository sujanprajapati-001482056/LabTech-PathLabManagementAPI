// Lab Tech Admin Dashboard JavaScript

document.addEventListener("DOMContentLoaded", () => {
  // Load dashboard statistics
  loadDashboardStats()

  // Refresh stats every 5 minutes
  setInterval(loadDashboardStats, 300000)
})

function loadDashboardStats() {
  fetch("/api/dashboard/stats/")
    .then((response) => response.json())
    .then((data) => {
      updateStatCard("total-patients", data.total_patients || 0)
      updateStatCard("pending-orders", data.pending_orders || 0)
      updateStatCard("completed-tests", data.completed_tests || 0)
      updateStatCard("revenue-today", "$" + (data.revenue_today || "0.00"))
    })
    .catch((error) => {
      console.log("Dashboard stats not available:", error)
    })
}

function updateStatCard(elementId, value) {
  const element = document.getElementById(elementId)
  if (element) {
    element.textContent = value

    // Add animation effect
    element.style.transform = "scale(1.1)"
    setTimeout(() => {
      element.style.transform = "scale(1)"
    }, 200)
  }
}

// Function to format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount)
}

// Function to format numbers with commas
function formatNumber(num) {
  return new Intl.NumberFormat().format(num)
}
