const form = document.getElementById("upload-form");
const responseDiv = document.getElementById("response");

let spinnerInterval = null;
const spinnerFrames = ["|", "/", "-", "\\"];

function startSpinner() {
  let frame = 0;
  responseDiv.innerHTML = "Processing... " + spinnerFrames[frame];

  spinnerInterval = setInterval(() => {
    frame = (frame + 1) % spinnerFrames.length;
    responseDiv.innerHTML = "Processing... " + spinnerFrames[frame];
  }, 120);
}

function stopSpinner() {
  clearInterval(spinnerInterval);
  spinnerInterval = null;
}

function openTab(event, tabName) {
  const contents = document.querySelectorAll(".tabcontent");
  contents.forEach((c) => (c.style.display = "none"));

  const links = document.querySelectorAll(".tablinks");
  links.forEach((l) => l.classList.remove("active"));

  document.getElementById(tabName).style.display = "block";
  event.currentTarget.classList.add("active");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);

  // clear previous output
  responseDiv.innerHTML = "";

  // start spinner
  startSpinner();

  try {
    const res = await fetch("/api/check/pdf", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    // stop spinner
    stopSpinner();

    // Tabs container
    const tabs = document.createElement("div");
    tabs.className = "tabs";

    const formattedTab = document.createElement("button");
    formattedTab.className = "tablinks";
    formattedTab.innerText = "Formatted";

    const rawTab = document.createElement("button");
    rawTab.className = "tablinks";
    rawTab.innerText = "Raw";

    // Tab contents
    const formattedContent = document.createElement("div");
    formattedContent.className = "tabcontent";
    formattedContent.id = "formatted";

    const rawContent = document.createElement("div");
    rawContent.className = "tabcontent";
    rawContent.id = "raw";

    // Append to DOM
    responseDiv.innerHTML = "";
    // tab
    responseDiv.appendChild(tabs);
    // tabs button
    tabs.appendChild(formattedTab);
    tabs.appendChild(rawTab);
    // content
    responseDiv.appendChild(formattedContent);
    responseDiv.appendChild(rawContent);

    // Tab button onclick
    formattedTab.onclick = (e) => openTab(e, "formatted");
    rawTab.onclick = (e) => openTab(e, "raw");

    // RAW JSON
    rawContent.textContent = JSON.stringify(data, null, 2);

    // FORMATTED TABLE
    const table = document.createElement("table");

    const headerRow = document.createElement("tr");
    const headers = Object.keys(data.result[0]);

    headers.forEach((h) => {
      const th = document.createElement("th");
      th.innerText = h;
      headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    data.result.forEach((item) => {
      const row = document.createElement("tr");

      headers.forEach((h) => {
        const td = document.createElement("td");
        td.innerText = item[h];
        row.appendChild(td);
      });

      table.appendChild(row);
    });

    formattedContent.appendChild(table);

    // Default tab -> Formatted
    formattedTab.click();
  } catch (err) {
    stopSpinner();
    responseDiv.textContent = err.message;
  }
});
