// function to handle when clicking the Download button
function handleDownloadClick() {
  const query = d3.select('#search_query').property("value");

  if (query) {
    console.log(query)
    document.getElementById("search_query").placeholder=query;

    // base url
    var baseURL = "https://th6n0jtotb.execute-api.eu-south-1.amazonaws.com/dev/guardian?download=True&puzzle_url=";
    var downloadURL = baseURL + query;

    // Simulate an HTTP redirect:
    window.location.replace(downloadURL);

  };
}

// Attach an event to listen for the search recipes button
d3.select("#search-btn").on("click", handleDownloadClick);
