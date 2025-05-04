document.getElementById("date").textContent = new Date().toLocaleDateString("en-IN");

async function fetchNiftyPrice() {
  const res = await fetch("https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI");
  const data = await res.json();
  const price = data.chart.result[0].meta.regularMarketPrice;
  document.getElementById("nifty-price").textContent = `₹${price}`;
}

fetchNiftyPrice();
