// ========== АВТОРИЗАЦИЯ ==========
function getToken() { return localStorage.getItem("access_token"); }
function setAccessToken(access) { localStorage.setItem("access_token", access); }
function clearAccessToken() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
}

async function refreshAccessToken() {
    try {
        const res = await fetch("/api/auth/refresh", {
            method: "POST",
            credentials: "include"
        });
        if (!res.ok) return false;
        const data = await res.json();
        setAccessToken(data.access_token);
        return true;
    } catch { return false; }
}

async function apiFetch(url, options = {}) {
    const token = getToken();
    const headers = {
        ...(options.headers || {}),
        ...(token ? { "Authorization": `Bearer ${token}` } : {})
    };
    let response = await fetch(url, { ...options, headers, credentials: "include" });
    if (response.status === 401) {
        const refreshed = await refreshAccessToken();
        if (refreshed) {
            const newToken = getToken();
            headers["Authorization"] = `Bearer ${newToken}`;
            response = await fetch(url, { ...options, headers, credentials: "include" });
        } else {
            clearAccessToken();
            if (!window.location.pathname.startsWith("/login")) {
                window.location.href = "/login";
            }
            return null;
        }
    }
    return response;
}

async function logout() {
    try {
        await fetch("/api/auth/logout", { method: "POST", credentials: "include" });
    } catch(e) { console.warn("Logout failed", e); }
    clearAccessToken();
    window.location.href = "/login";
}

// ========== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ==========
let editMode = false;
let dragStart = null;
let dragMode = null;
const GENDER_OPTIONS = ["", "М", "Ж"];
const SHIFT_OPTIONS = ["", "дневная", "ночная"];
const POSITION_OPTIONS = ["", "Пекарь", "Повар", "Слесарь-ремонтник", "Инженер", "Техник", "Механик", "Электрик", "Оператор", "Мастер", "Рабочий"];
let customers = [];
let fieldsList = [];
let currentOffset = 0;
let currentLimit = 30;
let isLoading = false;
let hasMore = true;
let currentMonth = null;
let currentYear = null;
let currentFieldId = "";
let currentWord = "";

// ========== ЗАГРУЗКА ДАННЫХ ==========
async function loadCustomers() {
    try {
        const res = await apiFetch("/api/customers");
        if (!res) return;
        customers = await res.json();
    } catch (err) {
        console.error("Ошибка загрузки customers:", err);
        customers = [];
    }
}

async function loadFields() {
    try {
        const response = await apiFetch("/api/fields");
        if (!response) return;
        const data = await response.json();
        fieldsList = data;
        const select = document.getElementById("fieldFilter");
        if (select) {
            select.innerHTML = '<option value="">Все месторождения</option>';
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

function generateCalendar() {
    const head = document.getElementById("calendarHead");
    if (!head) return;
    let row = "<tr>";
    row += "<th>Расположение</th><th>Путь</th><th>№ комнаты</th><th>К-во мест</th><th>Пол</th><th>ФИО</th><th>Должность</th><th>Дата заезда</th><th>Дата выезда</th><th>Дней</th><th>Заказчик</th><th>Действия</th>";
    row += "</tr>";
    head.innerHTML = row;
}

function searchResidents() { loadCalendar(true); }
function clearSearch() {
    document.getElementById("searchWord").value = "";
    document.getElementById("fieldFilter").value = "";
    loadCalendar(true);
}

// ========== СКАЧИВАНИЕ ОТЧЁТА ==========
async function downloadReport() {
    const dateFrom = document.getElementById("dateFrom")?.value;
    const dateTo = document.getElementById("dateTo")?.value;
    const costPerDay = document.getElementById("costPerDay")?.value;

    if (!dateFrom || !dateTo) { alert("Выберите обе даты!"); return; }
    if (dateFrom > dateTo) { alert("Дата начала не может быть позже даты конца!"); return; }

    let url = `/api/get_report?date_in=${dateFrom}&date_out=${dateTo}`;
    if (costPerDay && !isNaN(parseInt(costPerDay))) {
        url += `&cost_of_day=${parseInt(costPerDay)}`;
    }

    try {
        const response = await apiFetch(url);
        if (!response) return;
        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            alert(err.detail || "Ошибка загрузки отчёта");
            return;
        }
        const blob = await response.blob();
        const urlBlob = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = urlBlob;
        a.download = `report_${dateFrom}_${dateTo}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(urlBlob);
    } catch (err) {
        console.error(err);
        alert("Не удалось скачать отчёт");
    }
}

function toggleEditMode() {
    editMode = !editMode;
    const btn = document.getElementById("editModeBtn");
    if (btn) {
        btn.textContent = editMode ? "Выйти из редактирования" : "Режим редактирования";
        btn.style.background = editMode ? "#4CAF50" : "";
        btn.style.color = editMode ? "white" : "";
    }
    loadCalendar(true);
}

// ========== СТРОКА ТАБЛИЦЫ ==========
function createResidentRow(r, editModeFlag) {
    const row = document.createElement("tr");
    if (r.status == 1) row.classList.add("row-repair");

    const tdLocation = document.createElement("td");
    if (editModeFlag) {
        tdLocation.appendChild(makeStatusSelect(r.status, r.id, r.type));
    } else {
        tdLocation.textContent = r.room_location || "";
    }
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
        tdGender.appendChild(makeEditSelect(GENDER_OPTIONS, r.gender, r.id, "gender", r.type));
    } else {
        tdGender.textContent = r.gender || "";
    }
    row.appendChild(tdGender);

    const tdName = document.createElement("td");
    tdName.textContent = r.full_name || "";
    row.appendChild(tdName);

    const tdPosition = document.createElement("td");
    if (editModeFlag) {
        tdPosition.appendChild(makeEditSelect(POSITION_OPTIONS, r.position, r.id, "position", r.type));
    } else {
        tdPosition.textContent = r.position || "";
    }
    row.appendChild(tdPosition);

    const tdCheckIn = document.createElement("td");
    tdCheckIn.textContent = r.check_in || "";
    row.appendChild(tdCheckIn);

    const tdCheckOut = document.createElement("td");
    tdCheckOut.textContent = r.check_out || "";
    row.appendChild(tdCheckOut);

    const tdDays = document.createElement("td");
    tdDays.textContent = r.days || "";
    row.appendChild(tdDays);

    const tdCustomer = document.createElement("td");
    tdCustomer.textContent = r.customer || "";
    row.appendChild(tdCustomer);

    const tdActions = document.createElement("td");
    if (editModeFlag) {
        const convertBtn = document.createElement("button");
        convertBtn.textContent = r.type === "formal" ? "➡ В гостевые" : "⬅ В формальные";
        convertBtn.className = "btn-compact";
        convertBtn.style.background = "#ff9800";
        convertBtn.onclick = async () => {
            if (!confirm(`Преобразовать запись "${r.full_name}" из ${r.type === "formal" ? "формальной" : "гостевой"} в ${r.type === "formal" ? "гостевую" : "формальную"}?`)) return;
            const target = r.type === "formal" ? "guest" : "formal";
            const resp = await apiFetch("/api/convert_resident_type", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: r.id, target_type: target })
            });
            if (resp && resp.ok) {
                alert("Тип записи изменён");
                loadCalendar(true);
            } else {
                alert("Ошибка конвертации");
            }
        };
        tdActions.appendChild(convertBtn);
    }
    row.appendChild(tdActions);
    return row;
}

function makeEditSelect(options, currentValue, residentId, field, recordType) {
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
                body: JSON.stringify({ id: residentId, type: recordType, [field]: select.value })
            });
            if (!response) return;
            const result = await response.json();
            if (result.status !== "ok") alert("Ошибка сохранения");
        } catch (err) {
            console.error("Ошибка:", err);
        }
    });
    return select;
}

function makeStatusSelect(currentStatus, residentId, recordType) {
    const select = document.createElement("select");
    select.className = "edit-select status-select";
    const options = [
        { value: 0, text: "✓ Норма" },
        { value: 1, text: "🔧 Ремонт" }
    ];
    options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.text;
        if (currentStatus == opt.value) option.selected = true;
        select.appendChild(option);
    });
    select.addEventListener("change", async () => {
        try {
            const response = await apiFetch("/api/update_resident", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: residentId, type: recordType, status: parseInt(select.value) })
            });
            if (!response) return;
            const result = await response.json();
            if (result.status !== "ok") alert("Ошибка обновления статуса");
            else {
                const row = select.closest("tr");
                if (parseInt(select.value) === 1) row.classList.add("row-repair");
                else row.classList.remove("row-repair");
            }
        } catch (err) {
            console.error("Ошибка:", err);
            alert("Ошибка сохранения статуса");
        }
    });
    return select;
}

// ========== ПАГИНАЦИЯ И ЗАГРУЗКА ТАБЛИЦЫ ==========
function showLoader(show) {
    let loader = document.getElementById("tableLoader");
    if (!loader && show) {
        const container = document.querySelector(".table-section");
        if (!container) return;
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
    if (container) container.appendChild(btn);
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

    const year = document.getElementById("yearFilter")?.value || new Date().getFullYear();
    const month = document.getElementById("monthFilter")?.value || (new Date().getMonth() + 1);
    let fieldId = document.getElementById("fieldFilter")?.value || "";
    const word = document.getElementById("searchWord")?.value || "";

    if (!fieldId || fieldId === "") {
        const firstOption = document.querySelector("#fieldFilter option:not([value=''])");
        if (firstOption) {
            fieldId = firstOption.value;
            document.getElementById("fieldFilter").value = fieldId;
        }
    }

    if (reset) {
        currentOffset = 0;
        hasMore = true;
        currentMonth = month;
        currentYear = year;
        currentFieldId = fieldId;
        currentWord = word;
        generateCalendar();
        clearTable();
    }

    let url = `/api/residents?month=${month}&year=${year}&limit=${currentLimit}&offset=${currentOffset}`;
    if (fieldId) url += `&by_field=${fieldId}`;
    if (word) url += `&word=${encodeURIComponent(word)}`;

    try {
        const response = await apiFetch(url);
        if (!response) return;
        const residents = await response.json();

        if (!Array.isArray(residents) || residents.length === 0) {
            hasMore = false;
            if (reset) {
                const tbody = document.getElementById("calendarBody");
                if (tbody) tbody.innerHTML = '<tr><td colspan="12" style="text-align:center;padding:20px;">Ничего не найдено</td></tr>';
            }
            removeLoadMoreButton();
        } else {
            const tbody = document.getElementById("calendarBody");
            residents.forEach(r => {
                const row = createResidentRow(r, editMode);
                if (tbody) tbody.appendChild(row);
            });
            currentOffset += residents.length;
            hasMore = residents.length === currentLimit;
            if (hasMore) ensureLoadMoreButton();
            else removeLoadMoreButton();
        }
    } catch (err) {
        console.error("Ошибка загрузки:", err);
        const tbody = document.getElementById("calendarBody");
        if (tbody && reset) tbody.innerHTML = '<tr><td colspan="12" style="color:red;padding:20px;">Ошибка загрузки данных</td></tr>';
    } finally {
        isLoading = false;
        showLoader(false);
    }
}

// ========== ФОРМА ДОБАВЛЕНИЯ ЗАПИСИ ==========
function addNewRow() {
    const tbody = document.getElementById("calendarBody");
    if (!tbody) return;
    const oldNewRow = document.getElementById("new-resident-row");
    if (oldNewRow) oldNewRow.remove();

    const month = parseInt(document.getElementById("monthFilter")?.value, 10);
    const year = parseInt(document.getElementById("yearFilter")?.value, 10);
    if (!month || !year) {
        alert("Сначала выберите месяц и год");
        return;
    }

    const row = document.createElement("tr");
    row.id = "new-resident-row";

    const td = document.createElement("td");
    td.colSpan = 12;
    td.style.padding = "10px";
    td.style.background = "#f0f9ff";

    const form = document.createElement("div");
    form.style.display = "flex";
    form.style.flexWrap = "wrap";
    form.style.gap = "10px";
    form.style.alignItems = "center";

    // --- ФИО (с автодополнением) ---
    const nameInput = makeFormInput("ФИО *", "full_name", "text");
    form.appendChild(nameInput.wrapper);
    setupEmployeeAutocomplete(nameInput, posInputRef => {
        if (posInputRef && posInputRef.position && posInput.select) {
            if (POSITION_OPTIONS.includes(posInputRef.position)) {
                posInput.select.value = posInputRef.position;
            }
        }
        if (posInputRef && posInputRef.gender && genderInput.select) {
            if (GENDER_OPTIONS.includes(posInputRef.gender)) {
                genderInput.select.value = posInputRef.gender;
            }
        }
    });

    const posInput = makeFormSelect("Должность", "position", POSITION_OPTIONS);
    form.appendChild(posInput.wrapper);

    const genderInput = makeFormSelect("Пол", "gender", GENDER_OPTIONS);
    form.appendChild(genderInput.wrapper);

    const custInput = makeFormSelectFromList("Заказчик *", "customer_name", customers, "name");
    form.appendChild(custInput.wrapper);

    const fieldInput = makeFormSelectFromListId("Месторождение *", "field_id", fieldsList);
    form.appendChild(fieldInput.wrapper);
    const currentFieldFilter = document.getElementById("fieldFilter")?.value;
    if (currentFieldFilter && fieldsList.some(f => f.id == currentFieldFilter)) {
        fieldInput.select.value = currentFieldFilter;
    }

    const checkInInput = makeFormInput("Дата заезда *", "check_in", "date");
    const firstDayOfMonth = `${year}-${String(month).padStart(2, "0")}-01`;
    checkInInput.input.value = firstDayOfMonth;
    form.appendChild(checkInInput.wrapper);

    const checkOutInput = makeFormInput("Дата выезда *", "check_out", "date");
    const lastDay = daysInMonth(month, year);
    const lastDayOfMonth = `${year}-${String(month).padStart(2, "0")}-${String(lastDay).padStart(2, "0")}`;
    checkOutInput.input.value = lastDayOfMonth;
    form.appendChild(checkOutInput.wrapper);

    const commentInput = makeFormInput("Комментарий", "comment", "text");
    form.appendChild(commentInput.wrapper);

    // --- Выбор комнаты ---
    const roomWrapper = document.createElement("div");
    roomWrapper.style.display = "flex";
    roomWrapper.style.flexDirection = "column";
    roomWrapper.style.gap = "4px";
    const roomLabel = document.createElement("label");
    roomLabel.textContent = "Комната *";
    roomLabel.style.fontSize = "12px";
    roomLabel.style.fontWeight = "600";
    const roomRow = document.createElement("div");
    roomRow.style.display = "flex";
    roomRow.style.gap = "4px";
    const roomSelect = document.createElement("select");
    roomSelect.className = "edit-select";
    roomSelect.style.padding = "4px 8px";
    roomSelect.innerHTML = `<option value="">— сначала найдите свободные места —</option>`;
    const findRoomsBtn = document.createElement("button");
    findRoomsBtn.type = "button";
    findRoomsBtn.className = "btn-compact";
    findRoomsBtn.textContent = "🔍 Найти места";
    findRoomsBtn.onclick = async () => {
        await refreshAvailableRooms();
    };
    roomRow.appendChild(roomSelect);
    roomRow.appendChild(findRoomsBtn);
    roomWrapper.appendChild(roomLabel);
    roomWrapper.appendChild(roomRow);
    form.appendChild(roomWrapper);

    async function refreshAvailableRooms() {
        const fieldId = parseInt(fieldInput.select.value);
        const checkIn = checkInInput.input.value;
        const checkOut = checkOutInput.input.value;
        if (!fieldId || isNaN(fieldId) || fieldId <= 0) {
            alert("Выберите месторождение!");
            return;
        }
        if (!checkIn || !checkOut) {
            alert("Укажите даты заезда и выезда!");
            return;
        }
        if (checkIn > checkOut) {
            alert("Дата заезда не может быть позже даты выезда!");
            return;
        }
        roomSelect.innerHTML = `<option value="">— поиск... —</option>`;
        try {
            const resp = await apiFetch(
                `/api/requests/available?field_id=${fieldId}&check_in=${checkIn}&check_out=${checkOut}`
            );
            if (!resp || !resp.ok) {
                roomSelect.innerHTML = `<option value="">— ошибка поиска —</option>`;
                return;
            }
            const rooms = await resp.json();
            if (!rooms || rooms.length === 0) {
                roomSelect.innerHTML = `<option value="">— нет свободных мест —</option>`;
                return;
            }
            const options = [];
            rooms.forEach(r => {
                const variants = (r.variants && r.variants.length) ? r.variants : [{
                    id: r.id,
                    room_unique_id: r.room_unique_id,
                    capacity: r.capacity,
                    occupied: r.occupied,
                    free_places: r.free_places,
                }];
                variants.forEach(v => {
                    const uniquePart = v.room_unique_id ? ` / ${v.room_unique_id}` : "";
                    options.push(
                        `<option value="${v.id}">№ ${r.room_number}${uniquePart} — свободно ${r.free_places} из ${r.capacity} (в этом варианте: ${v.free_places} из ${v.capacity})</option>`
                    );
                });
            });
            roomSelect.innerHTML = options.join("");
        } catch (err) {
            roomSelect.innerHTML = `<option value="">— ошибка поиска —</option>`;
            console.error("Ошибка поиска комнат:", err);
        }
    }

    fieldInput.select.addEventListener("change", refreshAvailableRooms);
    checkInInput.input.addEventListener("change", refreshAvailableRooms);
    checkOutInput.input.addEventListener("change", refreshAvailableRooms);
    refreshAvailableRooms();

    // Тип записи
    const typeDiv = document.createElement("div");
    typeDiv.style.display = "flex";
    typeDiv.style.gap = "15px";
    typeDiv.style.alignItems = "center";
    typeDiv.style.flexBasis = "100%";
    typeDiv.style.marginTop = "5px";

    const typeLabel = document.createElement("span");
    typeLabel.textContent = "Тип записи:";
    typeLabel.style.fontWeight = "600";
    typeDiv.appendChild(typeLabel);

    const radioOfficial = document.createElement("input");
    radioOfficial.type = "radio";
    radioOfficial.name = "addType";
    radioOfficial.value = "official";
    radioOfficial.id = "addTypeOfficial";
    radioOfficial.checked = true;
    const labelOfficial = document.createElement("label");
    labelOfficial.htmlFor = "addTypeOfficial";
    labelOfficial.textContent = "Официальный (сотрудник)";
    labelOfficial.style.marginRight = "5px";

    const radioGuest = document.createElement("input");
    radioGuest.type = "radio";
    radioGuest.name = "addType";
    radioGuest.value = "guest";
    radioGuest.id = "addTypeGuest";
    const labelGuest = document.createElement("label");
    labelGuest.htmlFor = "addTypeGuest";
    labelGuest.textContent = "Гостевой (без привязки к сотруднику)";

    typeDiv.appendChild(radioOfficial);
    typeDiv.appendChild(labelOfficial);
    typeDiv.appendChild(radioGuest);
    typeDiv.appendChild(labelGuest);
    form.appendChild(typeDiv);

    const btnWrapper = document.createElement("div");
    btnWrapper.style.display = "flex";
    btnWrapper.style.gap = "8px";
    btnWrapper.style.alignItems = "flex-end";
    btnWrapper.style.marginTop = "auto";

    const saveBtn = document.createElement("button");
    saveBtn.type = "button";
    saveBtn.className = "btn-compact";
    saveBtn.textContent = "💾 Сохранить";
    saveBtn.onclick = () => {
        const isOfficial = document.querySelector('input[name="addType"]:checked')?.value === "official";
        saveNewResidentRow({
            full_name: nameInput.input.value.trim(),
            position: posInput.select.value,
            gender: genderInput.select.value,
            customer_name: custInput.select.value,
            field_id: parseInt(fieldInput.select.value),
            check_in: checkInInput.input.value,
            check_out: checkOutInput.input.value,
            room_id: parseInt(roomSelect.value),
            comment: commentInput.input.value,
            eol_fio: nameInput.input.value.trim(),
            add_in_official: isOfficial
        });
    };

    const cancelBtn = document.createElement("button");
    cancelBtn.type = "button";
    cancelBtn.className = "btn-compact";
    cancelBtn.style.background = "#6c757d";
    cancelBtn.textContent = "✖ Отмена";
    cancelBtn.onclick = () => row.remove();

    btnWrapper.appendChild(saveBtn);
    btnWrapper.appendChild(cancelBtn);
    form.appendChild(btnWrapper);

    td.appendChild(form);
    row.appendChild(td);
    tbody.insertBefore(row, tbody.firstChild);
}

function setupEmployeeAutocomplete(fieldObj, onSelect) {
    const { wrapper, input } = fieldObj;
    wrapper.style.position = "relative";

    const dropdown = document.createElement("div");
    dropdown.style.position = "absolute";
    dropdown.style.top = "100%";
    dropdown.style.left = "0";
    dropdown.style.right = "0";
    dropdown.style.zIndex = "1000";
    dropdown.style.background = "#fff";
    dropdown.style.border = "1px solid #ccc";
    dropdown.style.borderRadius = "4px";
    dropdown.style.maxHeight = "180px";
    dropdown.style.overflowY = "auto";
    dropdown.style.display = "none";
    dropdown.style.boxShadow = "0 2px 6px rgba(0,0,0,0.15)";
    wrapper.appendChild(dropdown);

    let debounceTimer = null;
    function hideDropdown() {
        dropdown.style.display = "none";
        dropdown.innerHTML = "";
    }

    input.addEventListener("input", () => {
        const q = input.value.trim();
        if (debounceTimer) clearTimeout(debounceTimer);
        if (q.length < 2) {
            hideDropdown();
            return;
        }
        debounceTimer = setTimeout(async () => {
            try {
                const resp = await apiFetch(`/api/employees/search?q=${encodeURIComponent(q)}`);
                if (!resp || !resp.ok) {
                    hideDropdown();
                    return;
                }
                const employees = await resp.json();
                if (!employees || employees.length === 0) {
                    hideDropdown();
                    return;
                }
                dropdown.innerHTML = "";
                employees.forEach(emp => {
                    const item = document.createElement("div");
                    item.textContent = emp.full_name;
                    item.style.padding = "6px 10px";
                    item.style.cursor = "pointer";
                    item.addEventListener("mouseenter", () => item.style.background = "#f0f9ff");
                    item.addEventListener("mouseleave", () => item.style.background = "#fff");
                    item.addEventListener("mousedown", (e) => {
                        e.preventDefault();
                        input.value = emp.full_name;
                        hideDropdown();
                        if (typeof onSelect === "function") {
                            onSelect(emp);
                        }
                    });
                    dropdown.appendChild(item);
                });
                dropdown.style.display = "block";
            } catch (err) {
                console.error("Ошибка поиска сотрудников:", err);
                hideDropdown();
            }
        }, 250);
    });

    input.addEventListener("blur", () => {
        setTimeout(hideDropdown, 150);
    });
}

function makeFormInput(label, field, type) {
    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.flexDirection = "column";
    wrapper.style.gap = "4px";
    const lbl = document.createElement("label");
    lbl.textContent = label;
    lbl.style.fontSize = "12px";
    lbl.style.fontWeight = "600";
    const input = document.createElement("input");
    input.type = type;
    input.dataset.field = field;
    input.className = "edit-input";
    input.style.padding = "4px 8px";
    wrapper.appendChild(lbl);
    wrapper.appendChild(input);
    return { wrapper, input };
}

function makeFormSelect(label, field, options) {
    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.flexDirection = "column";
    wrapper.style.gap = "4px";
    const lbl = document.createElement("label");
    lbl.textContent = label;
    lbl.style.fontSize = "12px";
    lbl.style.fontWeight = "600";
    const select = document.createElement("select");
    select.dataset.field = field;
    select.className = "edit-select";
    options.forEach(opt => {
        const o = document.createElement("option");
        o.value = opt;
        o.textContent = opt || "—";
        select.appendChild(o);
    });
    wrapper.appendChild(lbl);
    wrapper.appendChild(select);
    return { wrapper, select };
}

function makeFormSelectFromList(label, field, list, nameKey) {
    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.flexDirection = "column";
    wrapper.style.gap = "4px";
    const lbl = document.createElement("label");
    lbl.textContent = label;
    lbl.style.fontSize = "12px";
    lbl.style.fontWeight = "600";
    const select = document.createElement("select");
    select.dataset.field = field;
    select.className = "edit-select";
    select.innerHTML = `<option value="">— выберите —</option>` +
        list.map(item => `<option value="${item[nameKey]}">${item[nameKey]}</option>`).join("");
    wrapper.appendChild(lbl);
    wrapper.appendChild(select);
    return { wrapper, select };
}

function makeFormSelectFromListId(label, field, list) {
    const wrapper = document.createElement("div");
    wrapper.style.display = "flex";
    wrapper.style.flexDirection = "column";
    wrapper.style.gap = "4px";
    const lbl = document.createElement("label");
    lbl.textContent = label;
    lbl.style.fontSize = "12px";
    lbl.style.fontWeight = "600";
    const select = document.createElement("select");
    select.dataset.field = field;
    select.className = "edit-select";
    select.innerHTML = `<option value="">— выберите —</option>` +
        list.map(f => `<option value="${f.id}">${f.name}</option>`).join("");
    wrapper.appendChild(lbl);
    wrapper.appendChild(select);
    return { wrapper, select };
}

async function saveNewResidentRow(data) {
    if (!data.full_name) { alert("Введите ФИО!"); return; }
    if (!data.customer_name) { alert("Выберите заказчика!"); return; }
    if (isNaN(data.field_id) || data.field_id <= 0) { alert("Выберите месторождение из списка!"); return; }
    if (!data.check_in || !data.check_out) { alert("Укажите даты!"); return; }
    if (data.check_in > data.check_out) { alert("Дата заезда не может быть позже даты выезда!"); return; }
    if (!data.add_in_official && !data.eol_fio) { alert("Для гостя укажите ФИО ответственного лица (eol_fio)"); return; }
    if (isNaN(data.room_id) || data.room_id <= 0) { alert("Выберите комнату из списка свободных мест! Нажмите «Найти места», если список пуст."); return; }

    try {
        const response = await apiFetch("/api/add_resident", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        if (!response) return;
        const result = await response.json();
        if (!response.ok) {
            alert(result.detail || result.error || "Ошибка при сохранении");
            return;
        }
        const newRow = document.getElementById("new-resident-row");
        if (newRow) newRow.remove();
        alert("✅ Запись добавлена!");
        loadCalendar(true);
    } catch (err) {
        alert("Ошибка: " + err.message);
    }
}

// ========== ЗАГРУЗКА EXCEL ==========
async function uploadExcel() {
    const fileInput = document.getElementById("excelFile");
    if (!fileInput) { alert("Элемент выбора файла не найден!"); return; }
    const file = fileInput.files[0];
    if (!file) { alert("Выберите файл!"); return; }
    const formData = new FormData();
    formData.append("file", file);
    try {
        const response = await apiFetch("/api/upload_excel", { method: "POST", body: formData });
        if (!response) return;
        const result = await response.json();
        if (response.ok) {
            // Новый ответ содержит message, approved_formal, approved_guest, rejected_no_room, rows_skipped, errors
            let msg = result.message || "Импорт выполнен";
            if (result.errors && result.errors.length > 0) {
                msg += "\n\nОшибки:\n" + result.errors.slice(0, 5).join("\n");
                if (result.errors.length > 5) msg += `\n... и ещё ${result.errors.length - 5}`;
            }
            alert("✅ " + msg);
            fileInput.value = "";
            loadCalendar(true);
        } else {
            alert("❌ Ошибка: " + (result.error || result.detail || "Неизвестная ошибка"));
        }
    } catch (err) {
        console.error("Ошибка загрузки:", err);
        alert("Ошибка загрузки: " + err.message);
    }
}

// ========== ОТЧЁТ ПО ПЕРЕРАБОТКАМ ==========
async function loadOvertimeFields() {
    try {
        const response = await apiFetch("/api/fields");
        if (!response) return;
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
        if (defaultSections) defaultSections.style.display = "none";
        if (overtimeContainer) overtimeContainer.style.display = "block";
        loadOvertimeFields();
        const now = new Date();
        const firstDay = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().slice(0, 10);
        const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString().slice(0, 10);
        const startInput = document.getElementById("overtimeStartDate");
        const endInput = document.getElementById("overtimeEndDate");
        if (startInput && !startInput.value) startInput.value = firstDay;
        if (endInput && !endInput.value) endInput.value = lastDay;
    } else {
        if (defaultSections) defaultSections.style.display = "block";
        if (overtimeContainer) overtimeContainer.style.display = "none";
    }
}

async function downloadOvertimeReport() {
    const startDate = document.getElementById("overtimeStartDate").value;
    const endDate = document.getElementById("overtimeEndDate").value;
    if (!startDate || !endDate) { alert("Выберите обе даты!"); return; }
    if (startDate > endDate) { alert("Дата начала не может быть позже даты конца!"); return; }
    const normDays = document.getElementById("normDays").value || 15;
    const fieldName = document.getElementById("overtimeFieldFilter").value;

    let url = `/api/get_overtime_report?check_in=${startDate}&check_out=${endDate}&norm_days=${normDays}`;
    if (fieldName) url += `&field_name=${encodeURIComponent(fieldName)}`;

    try {
        const response = await apiFetch(url);
        if (!response) return;
        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            alert(err.detail || "Ошибка формирования отчёта");
            return;
        }
        const blob = await response.blob();
        const blobUrl = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = blobUrl;
        a.download = `overtime_${startDate}_${endDate}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
        console.error(err);
        alert("Не удалось скачать отчёт по переработкам");
    }
}

// ========== ИНИЦИАЛИЗАЦИЯ ==========
document.addEventListener("DOMContentLoaded", async function () {
    if (window.location.pathname === '/login' || window.location.pathname === '/register') {
        return;
    }
    if (!getToken()) {
        window.location.href = "/login";
        return;
    }
    try {
        const userRes = await apiFetch("/api/current_user");
        if (!userRes) return;
        const currentUser = await userRes.json();
        const isAdmin = currentUser.role === "admin";

        if (!isAdmin) {
            const adminSelectors = [
                '.cards', '.report-section', '#editModeBtn', '#addResidentBtn', '#excelFile',
                'button[onclick="uploadExcel()"]', 'a[href="/admin_management"]', 'a[href="/moderate_requests"]',
                '#overtimeReportLink', '.table-section'
            ];
            adminSelectors.forEach(sel => {
                const el = document.querySelector(sel);
                if (el) el.style.display = 'none';
            });
            document.querySelectorAll('.sidebar li').forEach(li => {
                const link = li.querySelector('a');
                if (link) {
                    const href = link.getAttribute('href');
                    if (href && !['/home', '/request_form', '/my_requests', '/logout'].includes(href)) {
                        li.style.display = 'none';
                    }
                } else if (li.id && !['mainMenuLink', 'themeToggleBtn'].includes(li.id)) {
                    li.style.display = 'none';
                }
            });
            return;
        }

        // ========== АДМИНИСТРАТОР (внутри try) ==========
        await loadFields();
        await loadCustomers();

        const now = new Date();
        const monthEl = document.getElementById("monthFilter");
        const yearEl = document.getElementById("yearFilter");
        if (monthEl) monthEl.value = now.getMonth() + 1;
        if (yearEl) yearEl.value = now.getFullYear();

        if (fieldsList.length > 0 && document.getElementById("fieldFilter")) {
            const firstFieldId = fieldsList[0].id;
            document.getElementById("fieldFilter").value = firstFieldId;
        }

        const addBtn = document.getElementById("addResidentBtn");
        if (addBtn) addBtn.addEventListener("click", addNewRow);

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

        // Статистика с выбором периода
        const nowStats = new Date();
        const firstDayStats = new Date(nowStats.getFullYear(), nowStats.getMonth(), 1).toISOString().slice(0,10);
        const lastDayStats = new Date(nowStats.getFullYear(), nowStats.getMonth() + 1, 0).toISOString().slice(0,10);
        const statsFrom = document.getElementById("statsDateFrom");
        const statsTo = document.getElementById("statsDateTo");
        if (statsFrom && !statsFrom.value) statsFrom.value = firstDayStats;
        if (statsTo && !statsTo.value) statsTo.value = lastDayStats;

        const updateStatsBtn = document.getElementById("updateStatsBtn");
        if (updateStatsBtn) {
            updateStatsBtn.addEventListener("click", () => loadStats());
        }

        const fieldFilter = document.getElementById("fieldFilter");
        if (fieldFilter) {
            fieldFilter.addEventListener("change", () => loadStats());
        }

        const monthFilter = document.getElementById("monthFilter");
        const yearFilterSelect = document.getElementById("yearFilter");
        const fieldFilterForTable = document.getElementById("fieldFilter");
        if (monthFilter) monthFilter.addEventListener("change", () => loadCalendar(true));
        if (yearFilterSelect) yearFilterSelect.addEventListener("change", () => loadCalendar(true));
        if (fieldFilterForTable) fieldFilterForTable.addEventListener("change", () => loadCalendar(true));

    } catch (err) {
        console.warn("Ошибка инициализации:", err);
    }

    // Переключатель темы (вне try, но может быть и внутри – без разницы)
    const themeToggleBtn = document.getElementById("themeToggleBtn");
    if (themeToggleBtn) {
        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark-theme");
            themeToggleBtn.textContent = "☀️ Светлая тема";
        } else {
            themeToggleBtn.textContent = "🌙 Тёмная тема";
        }
        themeToggleBtn.addEventListener("click", () => {
            document.body.classList.toggle("dark-theme");
            const isDark = document.body.classList.contains("dark-theme");
            localStorage.setItem("theme", isDark ? "dark" : "light");
            themeToggleBtn.textContent = isDark ? "☀️ Светлая тема" : "🌙 Тёмная тема";
        });
    }
});