const thread_bottom = document.querySelector("#thread-bottom");
console.log(thread_bottom)
/** @type {HTMLElement | null} */
let inputElement = null;
/** @type {HTMLButtonElement | null} */
let submitButton = null;
const existInput = document.querySelector("#prompt-textarea");
console.log(existInput)

const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    for (const node of mutation.addedNodes) {
      if (!(node instanceof HTMLElement)) continue;

      if (node.id === "prompt-textarea") {
        inputElement = node
        console.log(inputElement)
      } else if (node.id === "composer-submit-button") {
        submitButton = node;

        if (document.getElementById("clone-buton")) return;

        const cloneButton = submitButton.cloneNode(true);
        submitButton.disabled = false;
        cloneButton.id = "clone-buton";
        cloneButton.style.backgroundColor = "green";
        submitButton.style.display = "none";
        submitButton.parentElement.appendChild(cloneButton);


        cloneButton.addEventListener("click", async (event) => {
          event.preventDefault();

          const promptText = inputElement.firstChild.textContent
          try {
            // Appel à /analyze pour détecter la sensibilité
            const res = await fetch("http://localhost:5000/analyze", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ prompt: promptText })
            });
            const data = await res.json();
            console.log(data)

            if (data.sensitive) {
              const userChoice = confirm("⚠️ Données sensibles détectées. Anonymiser ?");
              if (!userChoice) return;

              // Appel à /process pour anonymiser et récupérer réponse LLM
              const processRes = await fetch("http://localhost:5000/process", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: promptText })
              });
              const processData = await processRes.json();

              // Remplacer le texte dans le champ contenteditable
              inputElement.firstChild.textContent = processData.anonymized;
              setTimeout(() => {
               // Cliquer sur le vrai bouton d’envoi
                submitButton.click();
              }, 100);
              setTimeout(() => location.reload(), 10000); // 10 seconde de délai
            }
            else {
              submitButton.click();
              setTimeout(() => location.reload(), 10000); // 10 seconde de délai
            }
          } catch (err) {
            console.error("Erreur lors de la requête au serveur SafePrompt:", err);
            alert("Erreur de communication avec le serveur SafePrompt.", err);
          }
        }, { capture: true });
      }
    }
  }
});

if (thread_bottom) {
  observer.observe(thread_bottom, { subtree: true, childList: true });
} else {
  console.warn("#thread-bottom non trouvé !");
}
