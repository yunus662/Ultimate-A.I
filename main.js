// main.js
// Handles UI interaction for admin_ui.html

async function runCommand() {
  const command = document.getElementById("commandInput").value;
  const resultBox = document.getElementById("commandResult");

  if (!command) {
    resultBox.textContent = "[Info] Please enter a command.";
    return;
  }

  resultBox.textContent = "[Running] Executing command...";
  try {
    const response = await fetch("/api/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command })
    });

    const data = await response.json();
    resultBox.textContent = data.result || "[No Output]";
    logToConsole(`[Command] ${command}\n[Result] ${data.result}`);
  } catch (err) {
    resultBox.textContent = "[Error] Could not contact backend.";
    logToConsole(`[Error] ${err.message}`);
  }
}

function logToConsole(text) {
  const log = document.getElementById("logConsole");
  const timestamp = new Date().toLocaleTimeString();
  log.textContent += `\n[${timestamp}] ${text}`;
  log.scrollTop = log.scrollHeight;
}

async function saveFile() {
  const path = document.getElementById("filepath").value;
  const content = document.getElementById("fileContent").value;
  const fileStatus = document.getElementById("fileStatus");

  if (!path || !content) {
    fileStatus.textContent = "[Info] File path and content required.";
    return;
  }

  fileStatus.textContent = "[Saving] Sending update...";
  try {
    const response = await fetch("/api/update_file", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path, content })
    });

    const data = await response.json();
    fileStatus.textContent = data.message || "[Success] File updated.";
    logToConsole(`[File Save] ${path}\n[Status] ${data.message}`);
  } catch (err) {
    fileStatus.textContent = "[Error] Could not update file.";
    logToConsole(`[Error] ${err.message}`);
  }
}
