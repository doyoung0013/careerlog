const STATUSES = ["지원 예정", "지원 완료", "면접 예정", "면접 완료", "탈락", "합격"];
const COVER_STATUSES = ["초안", "수정 중", "제출 완료"];

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
  search: document.querySelector("#searchInput"),
  statusFilter: document.querySelector("#statusFilter"),
  sort: document.querySelector("#sortSelect"),
  dashboard: document.querySelector("#dashboard"),
  exportButton: document.querySelector("#exportButton"),
  importInput: document.querySelector("#importInput"),
  importButton: document.querySelector("#importButton"),
  detailTitle: document.querySelector("#detailTitle"),
  detailSubtitle: document.querySelector("#detailSubtitle"),
  tabButtons: document.querySelectorAll("[data-tab-target]"),
  tabPanels: document.querySelectorAll("[data-tab-panel]"),
  interviewForm: document.querySelector("#interviewForm"),
  interviewId: document.querySelector("#interviewId"),
  interviewDate: document.querySelector("#interviewDate"),
  interviewType: document.querySelector("#interviewType"),
  interviewResult: document.querySelector("#interviewResult"),
  interviewQuestions: document.querySelector("#interviewQuestions"),
  interviewNotes: document.querySelector("#interviewNotes"),
  interviewList: document.querySelector("#interviewList"),
  clearInterviewButton: document.querySelector("#clearInterviewButton"),
  coverForm: document.querySelector("#coverForm"),
  coverId: document.querySelector("#coverId"),
  coverQuestion: document.querySelector("#coverQuestion"),
  coverAnswer: document.querySelector("#coverAnswer"),
  coverStatus: document.querySelector("#coverStatus"),
  coverList: document.querySelector("#coverList"),
  clearCoverButton: document.querySelector("#clearCoverButton"),
  eventForm: document.querySelector("#eventForm"),
  eventId: document.querySelector("#eventId"),
  eventDate: document.querySelector("#eventDate"),
  eventType: document.querySelector("#eventType"),
  eventNote: document.querySelector("#eventNote"),
  eventList: document.querySelector("#eventList"),
  clearEventButton: document.querySelector("#clearEventButton"),
};

let applications = [];
let selectedId = null;
let interviews = [];
let coverLetters = [];
let events = [];

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function initializeOptions() {
  elements.status.innerHTML = STATUSES.map(
    (status) => `<option value="${status}">${status}</option>`,
  ).join("");
  elements.statusFilter.innerHTML = [
    '<option value="">전체 상태</option>',
    ...STATUSES.map((status) => `<option value="${status}">${status}</option>`),
  ].join("");
  elements.coverStatus.innerHTML = COVER_STATUSES.map(
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

  if (response.status === 204) return null;
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

function todayDate() {
  const now = new Date();
  now.setHours(0, 0, 0, 0);
  return now;
}

function parseDate(value) {
  if (!value) return null;
  const date = new Date(`${value}T00:00:00`);
  return Number.isNaN(date.getTime()) ? null : date;
}

function getDday(deadline) {
  const date = parseDate(deadline);
  if (!date) return { label: "마감일 없음", tone: "muted" };
  const diff = Math.ceil((date - todayDate()) / 86400000);
  if (diff < 0) return { label: `D+${Math.abs(diff)}`, tone: "danger" };
  if (diff === 0) return { label: "오늘 마감", tone: "danger" };
  if (diff <= 7) return { label: `D-${diff}`, tone: "warning" };
  return { label: `D-${diff}`, tone: "default" };
}

function formatDate(value) {
  return value || "날짜 없음";
}

function renderDashboard(summary) {
  const statusLine = STATUSES.map(
    (status) => `
      <span class="mini-stat">
        <span>${status}</span>
        <strong>${summary.status_counts?.[status] || 0}</strong>
      </span>
    `,
  ).join("");

  elements.dashboard.innerHTML = `
    <article class="metric">
      <span>전체 지원</span>
      <strong>${summary.total}</strong>
    </article>
    <article class="metric">
      <span>7일 내 마감</span>
      <strong>${summary.upcoming_deadlines}</strong>
    </article>
    <article class="metric">
      <span>마감 지남</span>
      <strong>${summary.overdue}</strong>
    </article>
    <article class="metric">
      <span>면접 기록</span>
      <strong>${summary.interviews}</strong>
    </article>
    <div class="status-summary">${statusLine}</div>
  `;
}

function formatDeadline(deadline) {
  const dday = getDday(deadline);
  return deadline ? `${deadline} · ${dday.label}` : dday.label;
}

function renderList() {
  elements.count.textContent = `${applications.length}개`;

  if (applications.length === 0) {
    elements.list.innerHTML = '<p class="empty">조건에 맞는 지원 기업이 없습니다.</p>';
    return;
  }

  elements.list.innerHTML = applications
    .map((item) => {
      const dday = getDday(item.deadline);
      return `
        <button class="application-item ${item.id === selectedId ? "active" : ""}" data-id="${item.id}" type="button">
          <span class="item-title">
            <span>${escapeHtml(item.company_name)}</span>
            <span class="status-chip">${escapeHtml(item.status)}</span>
          </span>
          <span class="item-meta">${escapeHtml(item.position)} · ${escapeHtml(formatDeadline(item.deadline))}</span>
          <span class="dday-chip ${dday.tone}">${escapeHtml(dday.label)}</span>
        </button>
      `;
    })
    .join("");
}

function updateDetailHeader(application = null) {
  elements.detailTitle.textContent = application ? application.company_name : "지원 상세";
  elements.detailSubtitle.textContent = application
    ? `${application.position} · ${formatDeadline(application.deadline)}`
    : "기업을 선택하거나 새 지원 항목을 추가하세요.";
}

function requireSelected() {
  if (!selectedId) {
    showToast("먼저 지원 기업을 저장하세요.");
    return false;
  }
  return true;
}

function clearForm() {
  selectedId = null;
  elements.form.reset();
  elements.id.value = "";
  elements.status.value = "지원 예정";
  updateDetailHeader();
  clearInterviewForm();
  clearCoverForm();
  clearEventForm();
  interviews = [];
  coverLetters = [];
  events = [];
  renderRecords();
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
  updateDetailHeader(application);
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

function getListQuery() {
  const params = new URLSearchParams();
  if (elements.search.value.trim()) params.set("q", elements.search.value.trim());
  if (elements.statusFilter.value) params.set("status_filter", elements.statusFilter.value);
  if (elements.sort.value) params.set("sort", elements.sort.value);
  const query = params.toString();
  return query ? `?${query}` : "";
}

async function loadDashboard() {
  const summary = await request("/api/dashboard");
  renderDashboard(summary);
}

async function loadApplications() {
  applications = await request(`/api/applications${getListQuery()}`);
  renderList();

  if (selectedId) {
    const selected = applications.find((item) => item.id === selectedId);
    if (selected) fillForm(selected);
  }
}

async function loadRecords() {
  if (!selectedId) return;
  const [loadedInterviews, loadedCovers, loadedEvents] = await Promise.all([
    request(`/api/applications/${selectedId}/interviews`),
    request(`/api/applications/${selectedId}/cover-letters`),
    request(`/api/applications/${selectedId}/events`),
  ]);
  interviews = loadedInterviews;
  coverLetters = loadedCovers;
  events = loadedEvents;
  renderRecords();
}

async function refreshAll() {
  await Promise.all([loadDashboard(), loadApplications()]);
  if (selectedId) await loadRecords();
}

async function selectApplication(id) {
  const application = await request(`/api/applications/${id}`);
  fillForm(application);
  await loadRecords();
}

function renderRecords() {
  renderInterviews();
  renderCoverLetters();
  renderEvents();
}

function renderInterviews() {
  if (!selectedId) {
    elements.interviewList.innerHTML = '<p class="empty compact">지원 기업 저장 후 면접 기록을 추가할 수 있습니다.</p>';
    return;
  }
  if (interviews.length === 0) {
    elements.interviewList.innerHTML = '<p class="empty compact">아직 면접 기록이 없습니다.</p>';
    return;
  }
  elements.interviewList.innerHTML = interviews
    .map(
      (item) => `
        <article class="record-item">
          <div>
            <strong>${escapeHtml(item.interview_type)}</strong>
            <span>${escapeHtml(formatDate(item.interview_date))} · ${escapeHtml(item.result)}</span>
          </div>
          <p>${escapeHtml(item.questions || "질문 기록 없음")}</p>
          <div class="record-actions">
            <button type="button" data-edit-interview="${item.id}">수정</button>
            <button type="button" class="danger" data-delete-interview="${item.id}">삭제</button>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderCoverLetters() {
  if (!selectedId) {
    elements.coverList.innerHTML = '<p class="empty compact">지원 기업 저장 후 자소서 문항을 추가할 수 있습니다.</p>';
    return;
  }
  if (coverLetters.length === 0) {
    elements.coverList.innerHTML = '<p class="empty compact">아직 자기소개서 문항이 없습니다.</p>';
    return;
  }
  elements.coverList.innerHTML = coverLetters
    .map(
      (item) => `
        <article class="record-item">
          <div>
            <strong>${escapeHtml(item.question)}</strong>
            <span>${escapeHtml(item.status)} · ${item.answer.length}자</span>
          </div>
          <p>${escapeHtml(item.answer || "답변 초안 없음")}</p>
          <div class="record-actions">
            <button type="button" data-edit-cover="${item.id}">수정</button>
            <button type="button" class="danger" data-delete-cover="${item.id}">삭제</button>
          </div>
        </article>
      `,
    )
    .join("");
}

function renderEvents() {
  if (!selectedId) {
    elements.eventList.innerHTML = '<p class="empty compact">지원 기업 저장 후 타임라인을 추가할 수 있습니다.</p>';
    return;
  }
  if (events.length === 0) {
    elements.eventList.innerHTML = '<p class="empty compact">아직 타임라인 기록이 없습니다.</p>';
    return;
  }
  elements.eventList.innerHTML = events
    .map(
      (item) => `
        <article class="timeline-item">
          <time>${escapeHtml(formatDate(item.event_date))}</time>
          <div>
            <strong>${escapeHtml(item.event_type)}</strong>
            <p>${escapeHtml(item.note || "메모 없음")}</p>
            <div class="record-actions">
              <button type="button" data-edit-event="${item.id}">수정</button>
              <button type="button" class="danger" data-delete-event="${item.id}">삭제</button>
            </div>
          </div>
        </article>
      `,
    )
    .join("");
}

function clearInterviewForm() {
  elements.interviewForm.reset();
  elements.interviewId.value = "";
  elements.interviewType.value = "면접";
  elements.interviewResult.value = "예정";
}

function clearCoverForm() {
  elements.coverForm.reset();
  elements.coverId.value = "";
  elements.coverStatus.value = "초안";
}

function clearEventForm() {
  elements.eventForm.reset();
  elements.eventId.value = "";
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
  await refreshAll();
  fillForm(saved);
  showToast("저장했습니다.");
});

elements.status.addEventListener("change", async () => {
  if (!elements.id.value) return;
  const saved = await request(`/api/applications/${elements.id.value}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status: elements.status.value }),
  });
  await refreshAll();
  fillForm(saved);
  showToast("지원 상태를 변경했습니다.");
});

elements.memoButton.addEventListener("click", async () => {
  if (!requireSelected()) return;
  const saved = await request(`/api/applications/${selectedId}/memo`, {
    method: "PATCH",
    body: JSON.stringify({ memo: elements.memo.value }),
  });
  await refreshAll();
  fillForm(saved);
  showToast("메모를 저장했습니다.");
});

elements.deleteButton.addEventListener("click", async () => {
  if (!elements.id.value) {
    clearForm();
    return;
  }
  if (!window.confirm("이 지원 기업을 삭제할까요?")) return;
  await request(`/api/applications/${selectedId}`, { method: "DELETE" });
  clearForm();
  await refreshAll();
  showToast("삭제했습니다.");
});

elements.search.addEventListener("input", () => {
  window.clearTimeout(elements.search.timer);
  elements.search.timer = window.setTimeout(() => {
    loadApplications().catch((error) => showToast(error.message));
  }, 180);
});
elements.statusFilter.addEventListener("change", () => {
  loadApplications().catch((error) => showToast(error.message));
});
elements.sort.addEventListener("change", () => {
  loadApplications().catch((error) => showToast(error.message));
});

elements.tabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    elements.tabButtons.forEach((item) => item.classList.remove("active"));
    elements.tabPanels.forEach((panel) => panel.classList.remove("active"));
    button.classList.add("active");
    document.querySelector(`[data-tab-panel="${button.dataset.tabTarget}"]`).classList.add("active");
  });
});

elements.interviewForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!requireSelected()) return;
  const payload = {
    interview_date: elements.interviewDate.value || null,
    interview_type: elements.interviewType.value.trim(),
    result: elements.interviewResult.value.trim(),
    questions: elements.interviewQuestions.value,
    notes: elements.interviewNotes.value,
  };
  const id = elements.interviewId.value;
  await request(
    id
      ? `/api/applications/${selectedId}/interviews/${id}`
      : `/api/applications/${selectedId}/interviews`,
    { method: id ? "PUT" : "POST", body: JSON.stringify(payload) },
  );
  clearInterviewForm();
  await refreshAll();
  showToast("면접 기록을 저장했습니다.");
});

elements.interviewList.addEventListener("click", async (event) => {
  const editId = event.target.dataset.editInterview;
  const deleteId = event.target.dataset.deleteInterview;
  if (editId) {
    const item = interviews.find((record) => record.id === Number(editId));
    elements.interviewId.value = item.id;
    elements.interviewDate.value = item.interview_date || "";
    elements.interviewType.value = item.interview_type;
    elements.interviewResult.value = item.result;
    elements.interviewQuestions.value = item.questions || "";
    elements.interviewNotes.value = item.notes || "";
  }
  if (deleteId && window.confirm("면접 기록을 삭제할까요?")) {
    await request(`/api/applications/${selectedId}/interviews/${deleteId}`, { method: "DELETE" });
    await refreshAll();
    showToast("면접 기록을 삭제했습니다.");
  }
});

elements.clearInterviewButton.addEventListener("click", clearInterviewForm);

elements.coverForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!requireSelected()) return;
  const payload = {
    question: elements.coverQuestion.value.trim(),
    answer: elements.coverAnswer.value,
    status: elements.coverStatus.value,
  };
  const id = elements.coverId.value;
  await request(
    id
      ? `/api/applications/${selectedId}/cover-letters/${id}`
      : `/api/applications/${selectedId}/cover-letters`,
    { method: id ? "PUT" : "POST", body: JSON.stringify(payload) },
  );
  clearCoverForm();
  await refreshAll();
  showToast("자기소개서 문항을 저장했습니다.");
});

elements.coverList.addEventListener("click", async (event) => {
  const editId = event.target.dataset.editCover;
  const deleteId = event.target.dataset.deleteCover;
  if (editId) {
    const item = coverLetters.find((record) => record.id === Number(editId));
    elements.coverId.value = item.id;
    elements.coverQuestion.value = item.question;
    elements.coverAnswer.value = item.answer || "";
    elements.coverStatus.value = item.status;
  }
  if (deleteId && window.confirm("자기소개서 문항을 삭제할까요?")) {
    await request(`/api/applications/${selectedId}/cover-letters/${deleteId}`, { method: "DELETE" });
    await refreshAll();
    showToast("자기소개서 문항을 삭제했습니다.");
  }
});

elements.clearCoverButton.addEventListener("click", clearCoverForm);

elements.eventForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!requireSelected()) return;
  const payload = {
    event_date: elements.eventDate.value || null,
    event_type: elements.eventType.value.trim(),
    note: elements.eventNote.value,
  };
  const id = elements.eventId.value;
  await request(
    id ? `/api/applications/${selectedId}/events/${id}` : `/api/applications/${selectedId}/events`,
    { method: id ? "PUT" : "POST", body: JSON.stringify(payload) },
  );
  clearEventForm();
  await refreshAll();
  showToast("타임라인을 저장했습니다.");
});

elements.eventList.addEventListener("click", async (event) => {
  const editId = event.target.dataset.editEvent;
  const deleteId = event.target.dataset.deleteEvent;
  if (editId) {
    const item = events.find((record) => record.id === Number(editId));
    elements.eventId.value = item.id;
    elements.eventDate.value = item.event_date || "";
    elements.eventType.value = item.event_type;
    elements.eventNote.value = item.note || "";
  }
  if (deleteId && window.confirm("타임라인 기록을 삭제할까요?")) {
    await request(`/api/applications/${selectedId}/events/${deleteId}`, { method: "DELETE" });
    await refreshAll();
    showToast("타임라인 기록을 삭제했습니다.");
  }
});

elements.clearEventButton.addEventListener("click", clearEventForm);

elements.exportButton.addEventListener("click", () => {
  window.location.href = "/api/applications.csv";
});

elements.importButton.addEventListener("click", () => {
  elements.importInput.click();
});

elements.importInput.addEventListener("change", async () => {
  const file = elements.importInput.files[0];
  if (!file) return;
  const csvText = await file.text();
  const result = await request("/api/applications/import-csv", {
    method: "POST",
    body: JSON.stringify({ csv_text: csvText }),
  });
  elements.importInput.value = "";
  await refreshAll();
  showToast(`${result.imported}개 항목을 가져왔습니다.`);
});

initializeOptions();
clearForm();
refreshAll().catch((error) => showToast(error.message));
