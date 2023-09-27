const locationConfigOverlayElement = document.getElementById("config-overlay");
const backdropElement = document.getElementById("backdrop");
const formElement = document.querySelector("form");



const editLocationBtnElement = document.getElementById("edit-location-btn");
const cancelConfigBtnElement = document.getElementById("cancel-config-btn");

function openLocationConfig() {
  locationConfigOverlayElement.style.display = "block";
  backdropElement.style.display = "block";

}

function closeLocationConfig() {
  locationConfigOverlayElement.style.display = "none";
  backdropElement.style.display = "none";

  
}

editLocationBtnElement.addEventListener("click", openLocationConfig);
cancelConfigBtnElement.addEventListener("click", closeLocationConfig);
backdropElement.addEventListener("click", closeLocationConfig);
formElement.addEventListener("submit", saveLocationConfig);
