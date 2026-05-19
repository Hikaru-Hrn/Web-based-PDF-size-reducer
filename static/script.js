document.addEventListener("DOMContentLoaded", () => {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const fileNameDisplay = document.getElementById("file-name");

  // 1. Клик по зоне открывает окно выбора файла
  dropZone.addEventListener("click", () => fileInput.click());

  // 2. Обновление текста при ручном выборе файла
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length) {
      fileNameDisplay.textContent = `Выбран файл: ${fileInput.files[0].name}`;
    }
  });

  // 3. Обработка Drag-and-Drop
  ["dragover", "dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  // Визуальный эффект при наведении
  dropZone.addEventListener("dragover", () =>
    dropZone.classList.add("drag-over"),
  );
  dropZone.addEventListener("dragleave", () =>
    dropZone.classList.remove("drag-over"),
  );

  dropZone.addEventListener("drop", (e) => {
    dropZone.classList.remove("drag-over");
    const files = e.dataTransfer.files;
    if (files.length) {
      fileInput.files = files; // Передаем файлы в скрытый инпут
      fileNameDisplay.textContent = `Выбран файл: ${files[0].name}`;
    }
  });
});

// Функция отправки (остается прежней)[cite: 1]
async function startCompression() {
  const fileInput = document.getElementById("file-input");
  const quality = document.getElementById("quality").value;
  const statusDiv = document.getElementById("status-area");

  if (!fileInput.files[0]) return alert("Сначала выберите файл!");

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("quality", quality);

  statusDiv.innerHTML = '<div class="loader"></div> Обработка в очереди...';

  try {
    const response = await fetch("/compress", {
      method: "POST",
      body: formData,
    });
    const { task_id } = await response.json();

    const checkStatus = setInterval(async () => {
      const res = await fetch(`/status/${task_id}`);
      const data = await res.json();

      if (data.status === "SUCCESS") {
        clearInterval(checkStatus);
        statusDiv.innerHTML = `<a href="${data.download_url}" class="btn success-btn">⬇️ Скачать сжатый PDF</a>`;
      } else if (data.status === "FAILURE") {
        clearInterval(checkStatus);
        statusDiv.innerHTML = "❌ Ошибка при сжатии";
      }
    }, 2000);
  } catch (e) {
    statusDiv.innerHTML = "❌ Ошибка связи с сервером";
  }
}
