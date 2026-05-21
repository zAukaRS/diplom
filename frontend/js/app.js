// ===== JWT АВТОРИЗАЦИЯ =====
function getToken() { return localStorage.getItem("access_token"); }
function setTokens(access, refresh) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
}
function clearTokens() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}
async function refreshAccessToken() {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) return false;
    try {
        const res = await fetch("/api/auth/refresh", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh_token: refresh })
        });
        if (!res.ok) return false;
        const data = await res.json();
        setTokens(data.access_token, data.refresh_token);
        return true;
    } catch { return false; }
}
async function apiFetch(url, options = {}) {
    const token = getToken();
    const headers = {
        ...(options.headers || {}),
        ...(token ? { "Authorization": `Bearer ${token}` } : {})
    };
    let response = await fetch(url, { ...options, headers });
    if (response.status === 401) {
        const refreshed = await refreshAccessToken();
        if (refreshed) {
            const newHeaders = {
                ...(options.headers || {}),
                "Authorization": `Bearer ${getToken()}`
            };
            response = await fetch(url, { ...options, headers: newHeaders });
        } else {
            clearTokens();
            window.location.href = "/login";
            return null;
        }
    }
    return response;
}
async function logout() {
    const refresh = localStorage.getItem("refresh_token");
    if (refresh) {
        try {
            await fetch("/api/auth/logout", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ refresh_token: refresh })
            });
        } catch(e) { console.warn("Logout failed", e); }
    }
    clearTokens();
    window.location.href = "/login";
}
// ===== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====
let editMode = false;
let dragStart = null;
let dragMode = null;
const GENDER_OPTIONS = ["", "М", "Ж"];
const SHIFT_OPTIONS = ["", "дневная", "ночная"];
const POSITION_OPTIONS = ["", "Пекарь", "Повар", "Слесарь-ремонтник", "Инженер", "Техник", "Механик", "Электрик", "Оператор", "Мастер", "Рабочий"];
let customers = [];
let fieldsList = [];
// Пагинация
let currentOffset = 0;
let currentLimit = 30;
let isLoading = false;
let hasMore = true;
let currentMonth = null;
let currentYear = null;
let currentFieldId = "";
let currentWord = "";
// ===== ЗАГРУЗКА ДАННЫХ =====
async function loadCustomers() {
    try {
        const res = await apiFetch("/api/customers");
        customers = await res.json();
    } catch (err) {
        console.error("Ошибка загрузки customers:", err);
        customers = [];
    }
}
async function loadFields() {
    try {
        const response = await apiFetch("/api/fields");
        const data = await response.json();
        fieldsList = data;
        const select = document.getElementById("fieldFilter");
        if (select) {
            select.innerHTML = '<option value="">Выберите месторождение</option>';
            data.forEach(field => {
                const option = document.createElement("option");
                option.value = field.id;
                option.textContent = field.name;
                select.appendChild(option);
            });
        }
    } catch (err) {
        console.error("Ошибка загрузки месторождений:", err);
    }
}
function daysInMonth(month, year) {
    return new Date(year, month, 0).getDate();
}
function generateCalendar(days) {
    const head = document.getElementById("calendarHead");
    if (!head) return;
    let row = "<tr>";
    row += "<th>Расположение</th>";
    row += "<th>Путь</th>";
    row += "<th>№ комнаты</th>";
    row += "<th>К-во мест</th>";
    row += "<th>Пол</th>";
    row += "<th>ФИО</th>";
    row += "<th>Должность</th>";
    row += "<th>Смена</th>";
    for (let i = 1; i <= days; i++) row += `<th>${i}</th>`;
    row += "<th>Заказчик</th>";
    row += "<th>Месторождение</th>";
    row += "</table>";
    head.innerHTML = row;
}
function searchResidents() { loadCalendar(true); }
function clearSearch() {
    document.getElementById("searchWord").value = "";
    document.getElementById("fieldFilter").value = "";
    loadCalendar(true);
}
function downloadReport() {
    const dateFrom = document.getElementById("dateFrom")?.value;
    const dateTo = document.getElementById("dateTo")?.value;
    if (!dateFrom || !dateTo) { alert("Выберите обе даты!"); return; }
    if (dateFrom > dateTo) { alert("Дата начала не может быть позже даты конца!"); return; }
    window.open(`/api/get_report?date_in=${dateFrom}&date_out=${dateTo}`, "_blank");
}
function toggleEditMode() {
    editMode = !editMode;
    const btn = document.getElementById("editModeBtn");
    if (btn) {
        btn.textContent = editMode ? "Выйти из редактирования" : "Режим редактирования";
        btn.style.background = editMode ? "#4CAF50" : "";
        btn.style.color = editMode ? "white" : "";
    }
    loadCalendar(true); // перезагрузить таблицу с новым режимом
}
// Создание строки жильца
function createResidentRow(r, days, editModeFlag) {
    const row = document.createElement("tr");
    const tdLocation = document.createElement("td");
    tdLocation.textContent = r.room_location || "";
    row.appendChild(tdLocation);
    const tdPath = document.createElement("td");
    tdPath.textContent = r.room_path || "";
    row.appendChild(tdPath);
    const tdRoomNumber = document.createElement("td");
    tdRoomNumber.textContent = r.room_number || "";
    row.appendChild(tdRoomNumber);
    const tdCapacity = document.createElement("td");
    tdCapacity.textContent = r.room_capacity || "";
    row.appendChild(tdCapacity);
    const tdGender = document.createElement("td");
    if (editModeFlag) {
        tdGender.appendChild(makeEditSelect(GENDER_OPTIONS, r.gender, r.id, "gender"));
    } else {
        tdGender.textContent = r.gender || "";
    }
    row.appendChild(tdGender);
    const tdName = document.createElement("td");
    tdName.textContent = r.full_name || "";
    row.appendChild(tdName);
    const tdPosition = document.createElement("td");
    if (editModeFlag) {
        tdPosition.appendChild(makeEditSelect(POSITION_OPTIONS, r.position, r.id, "position"));
    } else {
        tdPosition.textContent = r.position || "";
    }
    row.appendChild(tdPosition);
    const tdShift = document.createElement("td");
    if (editModeFlag) {
        tdShift.appendChild(makeEditSelect(SHIFT_OPTIONS, r.shift, r.id, "shift"));
    } else {
        tdShift.textContent = r.shift || "";
    }
    row.appendChild(tdShift);
    for (let i = 1; i <= days; i++) {
        const selectedId = r.days_info?.[i] || "";
        const td = document.createElement("td");
        const select = document.createElement("select");
        select.className = "day-select";
        select.dataset.resident = r.id;
        select.dataset.day = i;
        select.title = "Выберите заказчика";
        select.innerHTML = `<option value="">-</option>` +
            customers.map(c => `<option value="${c.id}" ${c.id == selectedId ? "selected" : ""}>${c.name}</option>`).join("");
        td.appendChild(select);
        row.appendChild(td);
    }
    const tdCustomer = document.createElement("td");
    tdCustomer.textContent = r.customer || "";
    row.appendChild(tdCustomer);
    const tdField = document.createElement("td");
    tdField.textContent = r.field || "";
    row.appendChild(tdField);
    return row;
}
function makeEditSelect(options, currentValue, residentId, field) {
    const select = document.createElement("select");
    select.className = "edit-select";
    options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt;
        option.textContent = opt || "—";
        if (opt === currentValue) option.selected = true;
        select.appendChild(option);
    });
    select.addEventListener("change", async () => {
        try {
            const response = await apiFetch("/api/update_resident", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: residentId, [field]: select.value })
            });
            const result = await response.json();
            if (result.status !== "ok") alert("Ошибка сохранения");
        } catch (err) {
            console.error("Ошибка:", err);
        }
    });
    return select;
}
// ===== DRAG FILL =====
function initDragFill() {
    const tbody = document.getElementById("calendarBody");
    if (!tbody) return;
    tbody.addEventListener("mousedown", (e) => {
        const td = e.target.closest("td");
        if (!td) return;
        if (e.target.tagName === "SELECT") return;
        const sel = td.querySelector(".day-select");
        if (!sel) return;
        dragStart = {
            residentId: sel.dataset.resident,
            day: parseInt(sel.dataset.day),
            value: sel.value
        };
        dragMode = dragStart.value ? "fill" : "clear";
        sel.classList.add("drag-highlight");
        e.preventDefault();
    });
    tbody.addEventListener("mouseover", (e) => {
        if (!dragStart) return;
        const td = e.target.closest("td");
        if (!td) return;
        const sel = td.querySelector(".day-select");
        if (!sel || sel.dataset.resident !== dragStart.residentId) return;
        const currentDay = parseInt(sel.dataset.day);
        const start = Math.min(dragStart.day, currentDay);
        const end = Math.max(dragStart.day, currentDay);
        tbody.querySelectorAll(`.day-select[data-resident='${dragStart.residentId}']`).forEach(s => s.classList.remove("drag-highlight"));
        for (let i = start; i <= end; i++) {
            const cell = tbody.querySelector(`.day-select[data-resident='${dragStart.residentId}'][data-day='${i}']`);
            if (cell) cell.classList.add("drag-highlight");
        }
    });
    document.addEventListener("mouseup", async () => {
        if (!dragStart) return;
        const selList = tbody.querySelectorAll(`.day-select[data-resident='${dragStart.residentId}'].drag-highlight`);
        const saves = [];
        for (const sel of selList) {
            sel.value = dragMode === "fill" ? dragStart.value : "";
            saves.push(saveDay(sel));
        }
        await Promise.all(saves);
        selList.forEach(s => s.classList.remove("drag-highlight"));
        dragStart = null;
        dragMode = null;
    });
}
async function saveDay(selectEl) {
    const residentId = selectEl.dataset.resident;
    const day = selectEl.dataset.day;
    const month = document.getElementById("monthFilter")?.value;
    const year = document.getElementById("yearFilter")?.value;
    const customerId = selectEl.value ? parseInt(selectEl.value) : null;
    if (!residentId || !day || !month || !year) return;
    try {
        await apiFetch("/api/update_day", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                resident_id: parseInt(residentId),
                day: parseInt(day),
                month: parseInt(month),
                year: parseInt(year),
                customer_id: customerId
            })
        });
    } catch (err) {
        console.error("Ошибка при сохранении дня:", err);
    }
}
// ===== ПАГИНАЦИЯ И ЗАГРУЗКА ТАБЛИЦЫ =====
function showLoader(show) {
    let loader = document.getElementById("tableLoader");
    if (!loader && show) {
        const container = document.querySelector(".table-section");
        loader = document.createElement("div");
        loader.id = "tableLoader";
        loader.className = "loader";
        loader.textContent = "Загрузка...";
        container.appendChild(loader);
    }
    if (loader) loader.style.display = show ? "block" : "none";
}
function ensureLoadMoreButton() {
    if (document.getElementById("loadMoreBtn")) return;
    const btn = document.createElement("button");
    btn.id = "loadMoreBtn";
    btn.textContent = "Загрузить ещё";
    btn.className = "stardartButton";
    btn.style.marginTop = "10px";
    btn.onclick = () => loadCalendar(false);
    const container = document.querySelector(".table-section");
    container.appendChild(btn);
}
function removeLoadMoreButton() {
    const btn = document.getElementById("loadMoreBtn");
    if (btn) btn.remove();
}
function clearTable() {
    const tbody = document.getElementById("calendarBody");
    if (tbody) tbody.innerHTML = "";
    removeLoadMoreButton();
}
async function loadCalendar(reset = true) {
    if (isLoading) return;
    isLoading = true;
    showLoader(true);
    const year = document.getElementById("yearFilter")?.value || "2025";
    const month = document.getElementById("monthFilter")?.value || "1";
    const fieldId = document.getElementById("fieldFilter")?.value || "";
    const word = document.getElementById("searchWord")?.value || "";
    const days = daysInMonth(parseInt(month), parseInt(year));
    if (reset) {
        currentOffset = 0;
        hasMore = true;
        currentMonth = month;
        currentYear = year;
        currentFieldId = fieldId;
        currentWord = word;
        generateCalendar(days);
        clearTable();
    } else if (
        month !== currentMonth ||
        year !== currentYear ||
        fieldId !== currentFieldId ||
        word !== currentWord
    ) {
        // параметры изменились – сбрасываем
        loadCalendar(true);
        isLoading = false;
        return;
    }
    let url = `/api/residents?month=${month}&year=${year}&limit=${currentLimit}&offset=${currentOffset}`;
    if (fieldId) url += `&by_field=${fieldId}`;
    if (word) url += `&word=${encodeURIComponent(word)}`;
    try {
        const response = await apiFetch(url);
        if (!response) return;
        const residents = await response.json();
        if (!residents || residents.length === 0) {
            hasMore = false;
            if (reset && residents.length === 0) {
                const tbody = document.getElementById("calendarBody");
                if (tbody) tbody.innerHTML = '<tr><td colspan="20" style="text-align:center;">Ничего не найдено</td></tr>';
            }
            removeLoadMoreButton();
        } else {
            const tbody = document.getElementById("calendarBody");
            residents.forEach(r => {
                const row = createResidentRow(r, days, editMode);
                tbody.appendChild(row);
            });
            currentOffset += residents.length;
            hasMore = residents.length === currentLimit;
            if (hasMore) ensureLoadMoreButton();
            else removeLoadMoreButton();
        }
    } catch (err) {
        console.error("Ошибка загрузки:", err);
        const tbody = document.getElementById("calendarBody");
        if (tbody && reset) tbody.innerHTML = '<tr><td colspan="20" style="color:red;">Ошибка загрузки</td></tr>';
    } finally {
        isLoading = false;
        showLoader(false);
    }
}
// ===== ДОБАВЛЕНИЕ НОВОГО РЕЗИДЕНТА =====
function addNewRow() {
    const tbody = document.getElementById("calendarBody");
    if (!tbody) return;
    const oldNewRow = document.getElementById("new-resident-row");
    if (oldNewRow) oldNewRow.remove();
    const month = parseInt(document.getElementById("monthFilter")?.value, 10);
    const year = parseInt(document.getElementById("yearFilter")?.value, 10);
    if (!month || !year) {
        alert("Сначала выберите месяц и год, затем нажмите Показать");
        return;
    }
    const days = daysInMonth(month, year);
    const head = document.getElementById("calendarHead");
    if (!head?.innerHTML?.trim()) generateCalendar(days);
    const row = document.createElement("tr");
    row.id = "new-resident-row";
    const tdLocation = document.createElement("td");
    const locationSelect = document.createElement("select");
    locationSelect.dataset.field = "location";
    locationSelect.className = "edit-select";
    locationSelect.innerHTML = `<option value="">—</option>
                                <option value="Общежитие">Общежитие</option>
                                <option value="Вагон">Вагон</option>`;
    tdLocation.appendChild(locationSelect);
    row.appendChild(tdLocation);
    const tdPath = document.createElement("td");
    const pathInput = document.createElement("input");
    pathInput.type = "text";
    pathInput.className = "edit-input";
    pathInput.dataset.field = "path";
    pathInput.placeholder = "Путь";
    pathInput.style.width = "100%";
    tdPath.appendChild(pathInput);
    row.appendChild(tdPath);
    const tdRoomNumber = document.createElement("td");
    const roomNumberInput = document.createElement("input");
    roomNumberInput.type = "text";
    roomNumberInput.className = "edit-input";
    roomNumberInput.dataset.field = "room_number";
    roomNumberInput.placeholder = "№ комнаты";
    roomNumberInput.style.width = "100%";
    tdRoomNumber.appendChild(roomNumberInput);
    row.appendChild(tdRoomNumber);
    const tdCapacity = document.createElement("td");
    const capacityInput = document.createElement("input");
    capacityInput.type = "number";
    capacityInput.className = "edit-input";
    capacityInput.dataset.field = "room_unique_id";
    capacityInput.placeholder = "К-во мест";
    capacityInput.style.width = "100%";
    tdCapacity.appendChild(capacityInput);
    row.appendChild(tdCapacity);
    const tdGender = document.createElement("td");
    tdGender.appendChild(makeEditSelectNew(GENDER_OPTIONS, "gender"));
    row.appendChild(tdGender);
    const tdName = document.createElement("td");
    const nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.className = "edit-input";
    nameInput.dataset.field = "full_name";
    nameInput.placeholder = "ФИО";
    const saveBtn = document.createElement("button");
    saveBtn.type = "button";
    saveBtn.className = "btn-compact";
    saveBtn.textContent = "Сохранить";
    saveBtn.style.marginLeft = "6px";
    saveBtn.onclick = () => saveNewRow(row, month, year);
    tdName.appendChild(nameInput);
    tdName.appendChild(saveBtn);
    row.appendChild(tdName);
    const tdPosition = document.createElement("td");
    tdPosition.appendChild(makeEditSelectNew(POSITION_OPTIONS, "position"));
    row.appendChild(tdPosition);
    const tdShift = document.createElement("td");
    tdShift.appendChild(makeEditSelectNew(SHIFT_OPTIONS, "shift"));
    row.appendChild(tdShift);
    for (let i = 1; i <= days; i++) {
        const td = document.createElement("td");
        const select = document.createElement("select");
        select.className = "day-select-new";
        select.dataset.day = i;
        select.innerHTML = `<option value="">-</option>` +
            customers.map(c => `<option value="${c.id}">${c.name}</option>`).join("");
        td.appendChild(select);
        row.appendChild(td);
    }
    const tdCustomer = document.createElement("td");
    const custSelect = document.createElement("select");
    custSelect.dataset.field = "customer";
    custSelect.className = "edit-select";
    custSelect.innerHTML = '<option value="">Выберите заказчика</option>' +
        customers.map(c => `<option value="${c.name}">${c.name}</option>`).join("");
    tdCustomer.appendChild(custSelect);
    row.appendChild(tdCustomer);
    const tdField = document.createElement("td");
    const fieldSelect = document.createElement("select");
    fieldSelect.dataset.field = "field";
    fieldSelect.className = "edit-select";
    fieldSelect.innerHTML = '<option value="">Выберите месторождение</option>' +
        fieldsList.map(f => `<option value="${f.name}">${f.name}</option>`).join("");
    tdField.appendChild(fieldSelect);
    row.appendChild(tdField);
    tbody.insertBefore(row, tbody.firstChild);
}
function makeEditSelectNew(options, field) {
    const select = document.createElement("select");
    select.className = "edit-select";
    select.dataset.field = field;
    options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt;
        option.textContent = opt || "—";
        select.appendChild(option);
    });
    return select;
}
async function saveNewRow(row, month, year) {
    const getValue = (field) => {
        const el = row.querySelector(`[data-field="${field}"]`);
        return el ? el.value : "";
    };
    const full_name = getValue("full_name");
    if (!full_name) { alert("Введите ФИО!"); return; }
    const field = getValue("field");
    if (!field) { alert("Выберите месторождение!"); return; }
    const customer = getValue("customer");
    if (!customer) { alert("Выберите заказчика!"); return; }
    const room_unique_id = getValue("room_unique_id");
    if (!room_unique_id) { alert("Укажите количество мест в комнате!"); return; }
    const daySelects = row.querySelectorAll(".day-select-new");
    const filled = Array.from(daySelects)
        .map(sel => ({ day: parseInt(sel.dataset.day), customerId: sel.value }))
        .filter(item => item.customerId && item.customerId !== "");
    if (filled.length === 0) {
        alert("Выберите хотя бы один день проживания!");
        return;
    }
    let minDay = Math.min(...filled.map(f => f.day));
    let maxDay = Math.max(...filled.map(f => f.day));
    let expectedCount = maxDay - minDay + 1;
    if (filled.length !== expectedCount) {
        alert(`Ошибка: заполнены не все дни с ${minDay} по ${maxDay}. Должны быть заполнены все дни подряд одним заказчиком.`);
        return;
    }
    const firstCustomer = filled[0].customerId;
    for (let i = 1; i < filled.length; i++) {
        if (filled[i].customerId !== firstCustomer) {
            alert(`Ошибка: в интервале с ${minDay} по ${maxDay} присутствуют разные заказчики. Должен быть один заказчик.`);
            return;
        }
    }
    const check_in = `${year}-${String(month).padStart(2, "0")}-${String(minDay).padStart(2, "0")}`;
    const check_out = `${year}-${String(month).padStart(2, "0")}-${String(maxDay).padStart(2, "0")}`;
    const data = {
        field: field,
        customer: customer,
        full_name: full_name,
        position: getValue("position") || "",
        gender: getValue("gender") || "",
        shift: getValue("shift") || "",
        room_number: getValue("room_number") || "—",
        room_unique_id: room_unique_id,
        location: getValue("location") || "Общежитие",
        path: getValue("path") || "",
        check_in: check_in,
        check_out: check_out,
    };
    try {
        const response = await apiFetch("/api/add_resident", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            alert(result.detail || result.error || "Ошибка");
            return;
        }
        const residentId = result.resident_id;
        for (const sel of daySelects) {
            if (sel.value) {
                await apiFetch("/api/update_day", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        resident_id: residentId,
                        day: parseInt(sel.dataset.day),
                        month: month,
                        year: year,
                        customer_id: parseInt(sel.value)
                    })
                });
            }
        }
        alert("Запись добавлена!");
        loadCalendar(true);
    } catch (err) {
        alert("Ошибка: " + err.message);
    }
}
// ===== ЗАГРУЗКА EXCEL =====
async function uploadExcel() {
    const fileInput = document.getElementById("excelFile");
    if (!fileInput) { alert("Элемент выбора файла не найден!"); return; }
    const file = fileInput.files[0];
    if (!file) { alert("Выберите файл!"); return; }
    const formData = new FormData();
    formData.append("file", file);
    try {
        const response = await apiFetch("/api/upload_excel", { method: "POST", body: formData });
        const result = await response.json();
        if (response.ok && result.message) {
            alert("✅ " + result.message);
            fileInput.value = "";
            loadCalendar(true);
        } else if (result.error) {
            alert("❌ Ошибка: " + result.error);
        } else {
            alert("⚠️ Неизвестный ответ от сервера");
        }
    } catch (err) {
        console.error("Ошибка загрузки:", err);
        alert("Ошибка загрузки: " + err.message);
    }
}
// ===== ОТЧЁТ ПО ПЕРЕРАБОТКАМ =====
async function loadOvertimeFields() {
    try {
        const response = await apiFetch("/api/fields");
        const data = await response.json();
        const select = document.getElementById("overtimeFieldFilter");
        if (!select) return;
        const selectedValue = select.value;
        select.innerHTML = '<option value="">Все</option>';
        data.forEach(field => {
            const option = document.createElement("option");
            option.value = field.name;
            option.textContent = field.name;
            select.appendChild(option);
        });
        if (selectedValue) select.value = selectedValue;
    } catch (err) {
        console.error("Ошибка загрузки месторождений для overtime:", err);
    }
}
function toggleMainView(showOvertime) {
    const defaultSections = document.getElementById("defaultSections");
    const overtimeContainer = document.getElementById("overtimeContainer");
    if (showOvertime) {
        defaultSections.style.display = "none";
        overtimeContainer.style.display = "block";
        loadOvertimeFields();
        const now = new Date();
        const firstDay = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().slice(0,10);
        const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString().slice(0,10);
        const startInput = document.getElementById("overtimeStartDate");
        const endInput = document.getElementById("overtimeEndDate");
        if (startInput && !startInput.value) startInput.value = firstDay;
        if (endInput && !endInput.value) endInput.value = lastDay;
    } else {
        defaultSections.style.display = "block";
        overtimeContainer.style.display = "none";
    }
}
function downloadOvertimeReport() {
    const startDate = document.getElementById("overtimeStartDate").value;
    const endDate = document.getElementById("overtimeEndDate").value;
    if (!startDate || !endDate) {
        alert("Выберите обе даты!");
        return;
    }
    const normDays = document.getElementById("normDays").value || 15;
    const fieldName = document.getElementById("overtimeFieldFilter").value;
    let url = `/api/get_overtime_report?date_from=${startDate}&date_to=${endDate}&norm_days=${normDays}`;
    if (fieldName) url += `&field_name=${encodeURIComponent(fieldName)}`;
    window.open(url, '_blank');
}
// ===== ОБРАБОТЧИКИ =====
document.addEventListener("change", async (e) => {
    if (e.target.classList.contains("day-select")) await saveDay(e.target);
});
document.addEventListener("DOMContentLoaded", async function () {
    if (!getToken()) { window.location.href = "/login"; return; }
    await loadFields();
    await loadCustomers();
    const now = new Date();
    const monthEl = document.getElementById("monthFilter");
    const yearEl = document.getElementById("yearFilter");
    if (monthEl) monthEl.value = now.getMonth() + 1;
    if (yearEl) yearEl.value = now.getFullYear();
    const addBtn = document.getElementById("addResidentBtn");
    if (addBtn) addBtn.addEventListener("click", addNewRow);
    initDragFill();
    await loadCalendar(true);
    await loadOvertimeFields();
    const mainLink = document.getElementById("mainMenuLink");
    const overtimeLink = document.getElementById("overtimeReportLink");
    const generateBtn = document.getElementById("generateOvertimeBtn");
    const backBtn = document.getElementById("backToMainBtn");
    if (mainLink) mainLink.addEventListener("click", () => toggleMainView(false));
    if (overtimeLink) overtimeLink.addEventListener("click", () => toggleMainView(true));
    if (generateBtn) generateBtn.addEventListener("click", downloadOvertimeReport);
    if (backBtn) backBtn.addEventListener("click", () => toggleMainView(false));
});