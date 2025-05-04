document.addEventListener("DOMContentLoaded", async () => {
  const reportDiv = document.getElementById("report");

  try {
    const res = await fetch("https://your-app.up.railway.app/api/premarket");
    const data = await res.json();

    reportDiv.innerHTML = `
      <p><strong>🗓 Date:</strong> ${new Date().toLocaleDateString("en-IN")}</p>
      <p><strong>🔵 NIFTY:</strong> ${data.nifty}</p>
      <p><strong>🟠 SENSEX:</strong> ${data.sensex}</p>
      <p><strong>🌍 Global Markets:</strong> ${data.global}</p>
      <p><strong>📊 FII/DII Data:</strong> ${data.fii}</p>
      <p><strong>🧠 Market Outlook:</strong> ${data.outlook}</p>
    `;
  } catch (error) {
    reportDiv.innerHTML = `<p>Error loading data. Try again later.</p>`;
  }
});
