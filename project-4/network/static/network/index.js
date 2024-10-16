document.addEventListener("DOMContentLoaded", function () {
    // Use buttons to toggle between views
    document.querySelector("#timeline-button").addEventListener("click", () => load_view("timeline"));
    document.querySelector("#following-button").addEventListener("click", () => load_view("following"));

    // By default, load the inbox
    load_view("timeline");
  });

  function load_view(view) {
    document.querySelector("#timeline").style.display = "block";

    // Clear cards before adding new ones
    document.querySelector("#timeline").innerHTML = "";
}