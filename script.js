function addFood() {
  const name = document.getElementById('foodName').value.trim();
  const expiry = document.getElementById('expiryDate').value;

  if (!name || !expiry) {
    alert("Please enter both food name and expiry date!");
    return;
  }

  const expDate = new Date(expiry);
  const today = new Date();
  const diffDays = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));

  const item = document.createElement('li');
  if (diffDays >= 0) {
    item.textContent = `${name} - ${diffDays} days left`;
    document.getElementById('freshList').appendChild(item);
  } else {
    item.innerHTML = `${name} (Expired) <button class="suggest" onclick="getSuggestion('${name}')">Get Suggestion</button>`;
    document.getElementById('expiredList').appendChild(item);
  }

  document.getElementById('foodName').value = '';
  document.getElementById('expiryDate').value = '';
}

// Fetch compost/suggestion ideas from Flask
function getSuggestion(food) {
  fetch('/suggestions', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({food: food})
  })
  .then(res => res.json())
  .then(data => {
    const box = document.getElementById('suggestion-list');
    box.innerHTML = '';
    data.ideas.forEach(i => {
      const li = document.createElement('li');
      li.textContent = i;
      box.appendChild(li);
    });
  });
}
function analyzeNutrition() {
  const foods = document.getElementById('foodInput').value.split(',').map(f => f.trim());
  fetch('/analyze_nutrition', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({foods})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('nutrition-totals').innerText =
      `Protein: ${data.totals.protein}g | Carbs: ${data.totals.carbs}g | Fat: ${data.totals.fat}g`;

    const list = document.getElementById('nutrition-advice');
    list.innerHTML = '';
    data.advice.forEach(tip => {
      const li = document.createElement('li');
      li.textContent = tip;
      list.appendChild(li);
    });
  });
}
