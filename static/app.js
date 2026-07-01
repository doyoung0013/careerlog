const STATUSES = ["지원 예정", "지원 완료", "면접 예정", "면접 완료", "탈락", "합격"];

const elements = {
  form: document.querySelector("#applicationForm"),
  id: document.querySelector("#applicationId"),
  companyName: document.querySelector("#companyName"),
  position: document.querySelector("#position"),
  deadline: document.querySelector("#deadline"),
  status: document.querySelector("#status"),
  memo: document.querySelector("#memo"),
  list: document.querySelector("#applicationList"),
  count: document.querySelector("#countBadge"),
  newButton: document.querySelector("#newButton"),
  memoButton: document.querySelector("#memoButton"),
  deleteButton: document.querySelector("#deleteButton"),
  toast: document.querySelector("#toast"),
};

let applications = [];
let selectedId = null;

function initializeStatusOptions() {
  elements.status.innerHTML = STATUSES.map(
    (status) => `<option value="${status}">${status}</option>`,
  ).join("");
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "요청을 처리하지 못했습니다.");
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add("show");
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    elements.toast.classList.remove("show");
  }, 2200);
}

function formatDeadline(deadline) {
  return deadline ? `마감 ${deadline}` : "마감일 없음";
}

function renderList() {
  elements.count.textContent = `${applications.length}개`;

  if (applications.length === 0) {
    elements.list.innerHTML = '<p class="empty">아직 등록된 지원 기업이 없습니다.</p>';
    return;
  }

  elements.list.innerHTML = applications
    .map(
      (item) => `
        <button class="application-item ${item.id === selectedId ? "active" : ""}" data-id="${item.id}" type="button">
          <span class="item-title">
            <span>${item.company_name}</span>
            <span class="status-chip">${item.status}</span>
          </span>
          <span class="item-meta">${item.position} · ${formatDeadline(item.deadline)}</span>
        </button>
      `,
    )
    .join("");
}

function clearForm() {
  selectedId = null;
  elements.form.reset();
  elements.id.value = "";
  elements.status.value = "지원 예정";
  renderList();
}

function fillForm(application) {
  selectedId = application.id;
  elements.id.value = application.id;
  elements.companyName.value = application.company_name;
  elements.position.value = application.position;
  elements.deadline.value = application.deadline || "";
  elements.status.value = application.status;
  elements.memo.value = application.memo || "";
  renderList();
}

function getPayload() {
  return {
    company_name: elements.companyName.value.trim(),
    position: elements.position.value.trim(),
    deadline: elements.deadline.value || null,
    status: elements.status.value,
    memo: elements.memo.value,
  };
}

async function loadApplications() {
  applications = await request("/api/applications");
  renderList();

  if (selectedId) {
    const selected = applications.find((item) => item.id === selectedId);
    if (selected) fillForm(selected);
  }
}

async function selectApplication(id) {
  const application = await request(`/api/applications/${id}`);
  fillForm(application);
}

elements.list.addEventListener("click", (event) => {
  const item = event.target.closest(".application-item");
  if (!item) return;
  selectApplication(Number(item.dataset.id)).catch((error) => showToast(error.message));
});

elements.newButton.addEventListener("click", () => {
  clearForm();
  elements.companyName.focus();
});

elements.form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = getPayload();
  const id = elements.id.value;

  const saved = id
    ? await request(`/api/applications/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      })
    : await request("/api/applications", {
        method: "POST",
        body: JSON.stringify(payload),
      });

  selectedId = saved.id;
  await loadApplications();
  fillForm(saved);
  showToast("저장했습니다.");
});

elements.status.addEventListener("change", async () => {
  if (!elements.id.value) return;
  const saved = await request(`/api/applications/${elements.id.value}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status: elements.status.value }),
  });
  await loadApplications();
  fillForm(saved);
  showToast("지원 상태를 변경했습니다.");
});

elements.memoButton.addEventListener("click", async () => {
  if (!elements.id.value) {
    showToast("먼저 지원 기업을 저장하세요.");
    return;
  }

  const saved = await request(`/api/applications/${elements.id.value}/memo`, {
    method: "PATCH",
    body: JSON.stringify({ memo: elements.memo.value }),
  });
  await loadApplications();
  fillForm(saved);
  showToast("메모를 저장했습니다.");
});

elements.deleteButton.addEventListener("click", async () => {
  if (!elements.id.value) {
    clearForm();
    return;
  }

  const confirmed = window.confirm("이 지원 기업을 삭제할까요?");
  if (!confirmed) return;

  await request(`/api/applications/${elements.id.value}`, { method: "DELETE" });
  clearForm();
  await loadApplications();
  showToast("삭제했습니다.");
});

initializeStatusOptions();
clearForm();
loadApplications().catch((error) => showToast(error.message));
