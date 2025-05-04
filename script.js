document.addEventListener("DOMContentLoaded", async () => {
  const reportDiv = document.getElementById("report");

  // Simulated data (you can replace this with a fetch from your server or API)
  const reportData = {
    date: new Date().toLocaleDateString("en-IN"),
    nifty: "NIFTY 50: 22,450 ↑ +110 pts",
    sensex: "SENSEX: 74,050 ↑ +250 pts",
    global: "Dow +0.8%, Nasdaq +1.2%, SGX Nifty +0.6%",
    fii: "FII: +₹1,200 Cr | DII: -₹600 Cr",
    outlook: "Market likely to open higher amid strong global cues.",
  };

  reportDiv.innerHTML = `
    <p><strong>🗓 Date:</strong> ${reportData.date}</p>
    <p><strong>🔵 NIFTY:</strong> ${reportData.nifty}</p>
    <p><strong>🟠 SENSEX:</strong> ${reportData.sensex}</p>
    <p><strong>🌍 Global Markets:</strong> ${reportData.global}</p>
    <p><strong>📊 FII/DII Data:</strong> ${reportData.fii}</p>
    <p><strong>🧠 Market Outlook:</strong> ${reportData.outlook}</p>
  `;
});
