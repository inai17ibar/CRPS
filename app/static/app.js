// Highlight code blocks on load
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
  });
});

let selectedChoice = null;

function selectChoice(btn, index) {
  // Clear previous selection
  document.querySelectorAll(".choice-btn").forEach((b) => b.classList.remove("selected"));
  btn.classList.add("selected");
  selectedChoice = index;
  document.getElementById("submit-btn").disabled = false;
}

async function submitAnswer(language, exerciseId) {
  if (selectedChoice === null) return;

  const submitBtn = document.getElementById("submit-btn");
  submitBtn.disabled = true;
  submitBtn.textContent = "判定中...";

  try {
    const res = await fetch(`/api/exercises/${language}/${exerciseId}/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selected: selectedChoice }),
    });
    const data = await res.json();

    showResult(data);
    highlightChoices(data.expected, selectedChoice);
  } catch {
    submitBtn.textContent = "回答する";
    submitBtn.disabled = false;
  }
}

function showResult(data) {
  const el = document.getElementById("result");
  el.classList.remove("hidden", "correct-result", "wrong-result");

  if (data.correct) {
    el.classList.add("correct-result");
    el.innerHTML = `<h3>正解!</h3><p>${data.explanation}</p>`;
  } else {
    el.classList.add("wrong-result");
    el.innerHTML = `<h3>不正解</h3><p>${data.explanation}</p>`;
  }
}

function highlightChoices(correctIndex, selectedIndex) {
  const buttons = document.querySelectorAll(".choice-btn");
  buttons.forEach((btn, i) => {
    btn.classList.remove("selected");
    btn.classList.add("disabled");
    if (i === correctIndex) btn.classList.add("correct");
    if (i === selectedIndex && i !== correctIndex) btn.classList.add("wrong");
  });
}
