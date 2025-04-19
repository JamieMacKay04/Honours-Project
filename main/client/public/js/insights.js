fetch('/api/latest-week')
.then(res => res.json())
.then(data => {
  const footnote = document.querySelector('.footnote');
  if (footnote && data.week) {
    footnote.innerText = `Based on historical data up to Week ${data.week}. Updated every Monday.`;
  } else {
    console.warn("Footnote element or week data missing.");
  }
})
.catch(err => {
  console.error("Error fetching latest week:", err);
});