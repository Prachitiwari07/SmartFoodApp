document.addEventListener("DOMContentLoaded", () => {
  const foodForm = document.getElementById("foodForm");
  const foodList = document.getElementById("foodList");

  foodForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value.trim();
    const days = parseInt(document.getElementById("days").value);

    if (name && days > 0) {
      const li = document.createElement("li");
      li.textContent = `${name} — ${days} days left`;
      li.classList.add("food-item");
      foodList.appendChild(li);

      foodForm.reset();
    }
  });
});
