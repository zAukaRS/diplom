// ===== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====
let editMode = false;
let dragStart = null;
let dragMode = null;
let workplaces = [];

const GENDER_OPTIONS = ["", "М", "Ж"];
const SHIFT_OPTIONS = ["", "дневная", "ночная"];
const POSITION_OPTIONS = ["", "Пекарь", "Повар", "Слесарь-ремонтник", "Инженер", "Техник", "Механик", "Электрик", "Оператор", "Мастер", "Рабочий"];
let customers = [];

// ===== ЗАГРУЗКА ДАННЫХ =====

async function loadWorkplaces() {
    try {
        const res = await fetch("/api/workplaces");
        workplaces = await res.json();
    } catch (err) {
        console.error("Ошибка загрузки workplaces:", err);
        workplaces = [];
    }
}

async function loadCustomers() {
    try {
        const res = await fetch("/api/customers");
        customers = await res.json();
    } catch (err) {
        console.error("Ошибка загрузки customers:", err);
        customers = [];
    }
}

async function loadFields() {
    try {
        const response = await fetch("/api/fields");
        const data = await response.json();
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

// ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====

function calculateDays(checkIn, checkOut) {
    if (!checkIn || !checkOut) return 0;
    const start = new Date(checkIn);
    const end = new Date(checkOut);
    const diffDays = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
    return diffDays > 0 ? diffDays : 0;
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
    for (let i = 1; i <= days; i++) {
        row += `<th>${i}</th>`;
    }
    row += "</tr>";
    head.innerHTML = row;
}

// ===== ГЛАВНЫЕ ФУНКЦИИ (ВЫЗЫВАЮТСЯ ИЗ HTML) =====

function searchResidents() {
    console.log("searchResidents вызвана!");
    loadCalendar();
}

function clearSearch() {
    console.log("clearSearch вызвана!");
    const searchWord = document.getElementById("searchWord");
    const fieldFilter = document.getElementById("fieldFilter");
    if (searchWord) searchWord.value = "";
    if (fieldFilter) fieldFilter.value = "";
    loadCalendar();
}

function downloadReport() {
    const dateFrom = document.getElementById("dateFrom")?.value;
    const dateTo = document.getElementById("dateTo")?.value;

    console.log("downloadReport:", dateFrom, dateTo);

    if (!dateFrom || !dateTo) {
        alert("Выберите обе даты!");
        return;
    }

    if (dateFrom > dateTo) {
        alert("Дата начала не может быть позже даты конца!");
        return;
    }

    const url = `/api/get_report?date_in=${dateFrom}&date_out=${dateTo}`;
    console.log("Запрос отчета:", url);
    window.open(url, "_blank");
}

function toggleEditMode() {
    editMode = !editMode;
    const btn = document.getElementById("editModeBtn");
    if (btn) {
        btn.textContent = editMode ? "Выйти из редактирования" : "Режим редактирования";
        btn.style.background = editMode ? "#4CAF50" : "";
        btn.style.color = editMode ? "white" : "";
    }

    const month = document.getElementById("monthFilter")?.value;
    const year = document.getElementById("yearFilter")?.value;
    if (month && year) loadCalendar();
}

async function loadCalendar() {
    console.log("loadCalendar вызвана!");
    
    await loadWorkplaces();
    await loadCustomers();
    
    const fieldSelect = document.getElementById("fieldFilter");
    const fieldId = fieldSelect?.value || "";
    const word = document.getElementById("searchWord")?.value || "";
    const year = document.getElementById("yearFilter")?.value || "2025";
    const month = document.getElementById("monthFilter")?.value || "1";
    
    const days = daysInMonth(month, year);
    generateCalendar(days);

    let url = `/api/residents?`;
    const params = [];
    if (fieldId) params.push(`by_field=${fieldId}`);
    if (word) params.push(`word=${encodeURIComponent(word)}`);
    url += params.join("&");
    
    console.log("Запрос:", url);

    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const residents = await response.json();
        const tbody = document.getElementById("calendarBody");
        if (!tbody) return;
        tbody.innerHTML = "";

        if (residents.error) {
            tbody.innerHTML = `<tr><td colspan="20" style="text-align:center; padding:20px;">${residents.error}</td></tr>`;
            return;
        }

        if (!residents || !residents.length) {
            tbody.innerHTML = '<tr><td colspan="20" style="text-align:center; padding:20px;">Ничего не найдено</td></tr>';
            return;
        }

        residents.forEach(r => {
            const row = document.createElement("tr");

            [
                r.room_location || "", 
                r.room_path || "", 
                r.room_number || "", 
                r.room_capacity || ""
            ].forEach(val => {
                const td = document.createElement("td");
                td.textContent = val;
                row.appendChild(td);
            });

            const tdGender = document.createElement("td");
            if (editMode) {
                tdGender.appendChild(makeEditSelect(GENDER_OPTIONS, r.gender, r.id, "gender"));
            } else {
                tdGender.textContent = r.gender || "";
            }
            row.appendChild(tdGender);

            const tdName = document.createElement("td");
            tdName.textContent = r.full_name || "";
            row.appendChild(tdName);

            const tdPosition = document.createElement("td");
            if (editMode) {
                tdPosition.appendChild(makeEditSelect(POSITION_OPTIONS, r.position, r.id, "position"));
            } else {
                tdPosition.textContent = r.position || "";
            }
            row.appendChild(tdPosition);

            const tdShift = document.createElement("td");
            if (editMode) {
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
                select.title = "Выберите рабочее место";
                select.innerHTML = `<option value="">-</option>` +
                    workplaces.map(w => `<option value="${w.id}" ${w.id == selectedId ? "selected" : ""}>${w.name}</option>`).join("");
                td.appendChild(select);
                row.appendChild(td);
            }

            tbody.appendChild(row);
        });

        initDragFill();
        
    } catch (err) {
        console.error("Ошибка загрузки данных:", err);
        const tbody = document.getElementById("calendarBody");
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="20" style="text-align:center; padding:20px; color:red;">Ошибка загрузки данных</td></tr>';
        }
    }
}

// ===== РЕЖИМ РЕДАКТИРОВАНИЯ =====

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
            const response = await fetch("/api/update_resident", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: residentId, [field]: select.value })
            });
            const result = await response.json();
            if (result.status !== "ok") {
                alert("Ошибка сохранения");
            }
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
        for (const sel of selList) {
            sel.value = dragMode === "fill" ? dragStart.value : "";
            await saveDay(sel);
        }
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
    const workplaceId = selectEl.value ? parseInt(selectEl.value) : null;

    if (!residentId || !day || !month || !year) return;

    try {
        await fetch("/api/update_day", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                resident_id: parseInt(residentId), 
                day: parseInt(day), 
                month: parseInt(month), 
                year: parseInt(year), 
                workplace_id: workplaceId 
            })
        });
    } catch (err) {
        console.error("Ошибка при сохранении дня:", err);
    }
}

// ===== ИНИЦИАЛИЗАЦИЯ ПРИ ЗАГРУЗКЕ =====

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM загружен!");
    
    await loadFields();
    await loadWorkplaces();
    await loadCustomers();
    
    const now = new Date();
    const monthEl = document.getElementById("monthFilter");
    const yearEl = document.getElementById("yearFilter");
    if (monthEl) monthEl.value = now.getMonth() + 1;
    if (yearEl) yearEl.value = now.getFullYear();
    
    const addBtn = document.getElementById("addResidentBtn");
    if (addBtn) {
        addBtn.addEventListener("click", function () {
            addNewRow();
        });
    }
    
    // Загружаем данные сразу
    await loadCalendar();
});

// ===== ДОБАВЛЕНИЕ НОВОГО РЕЗИДЕНТА =====

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
    if (!head?.innerHTML?.trim()) {
        generateCalendar(days);
    }
    
    const row = document.createElement("tr");
    row.id = "new-resident-row";

    [
        { key: "room_location", ph: "Расположение (Общежитие/Вагон)" },
        { key: "room_path", ph: "Путь" },
        { key: "room_number", ph: "№ комнаты" },
        { key: "room_capacity", ph: "К-во мест" }
    ].forEach(item => {
        const td = document.createElement("td");

        if (item.key === "room_location") {
            const select = document.createElement("select");
            select.className = "edit-select";
            select.dataset.field = "room_location";
            select.style.width = "100%";
            select.innerHTML = `
                <option value="">—</option>
                <option value="Общежитие">Общежитие</option>
                <option value="Вагон">Вагон</option>
            `;
            td.appendChild(select);
        } else {
            const input = document.createElement("input");
            input.type = "text";
            input.className = "edit-input";
            input.dataset.field = item.key;
            input.placeholder = item.ph;
            input.style.width = "100%";
            td.appendChild(input);
        }

        row.appendChild(td);
    });

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
            workplaces.map(w => `<option value="${w.id}">${w.name}</option>`).join("");
        td.appendChild(select);
        row.appendChild(td);
    }

    tbody.insertBefore(row, tbody.firstChild);
}

async function saveNewRow(row, month, year) {
    const getValue = (field) => {
        const el = row.querySelector(`[data-field="${field}"]`);
        return el ? el.value : "";
    };

    const full_name = getValue("full_name");
    if (!full_name) {
        alert("Введите ФИО!");
        return;
    }

    const check_in = `${year}-${String(month).padStart(2, "0")}-01`;
    const lastDay = daysInMonth(month, year);
    const check_out = `${year}-${String(month).padStart(2, "0")}-${String(lastDay).padStart(2, "0")}`;

    const data = {
        field: getValue("room_location") || "—",
        customer: "—",
        full_name,
        position: getValue("position"),
        gender: getValue("gender"),
        shift: getValue("shift"),
        check_in,
        check_out,
        days: lastDay
    };

    try {
        const response = await fetch("/api/add_resident", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (!response.ok) {
            alert(result.error || "Ошибка");
            return;
        }

        const residentId = result.resident_id;

        if (residentId) {
            const daySelects = row.querySelectorAll(".day-select-new");
            for (const sel of daySelects) {
                if (sel.value) {
                    await fetch("/api/update_day", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            resident_id: residentId,
                            day: parseInt(sel.dataset.day),
                            month,
                            year,
                            workplace_id: parseInt(sel.value)
                        })
                    });
                }
            }
        }

        alert("Запись добавлена!");
        loadCalendar();

    } catch (err) {
        alert("Ошибка: " + err.message);
    }
}

// ===== ОБРАБОТЧИКИ СОБЫТИЙ =====

document.addEventListener("change", async (e) => {
    if (e.target.classList.contains("day-select")) {
        const residentId = e.target.dataset.resident;
        if (!residentId) return;
        
        const day = e.target.dataset.day;
        const month = document.getElementById("monthFilter")?.value;
        const year = document.getElementById("yearFilter")?.value;
        const workplaceId = e.target.value ? parseInt(e.target.value) : null;

        if (!day || !month || !year) return;

        try {
            await fetch("/api/update_day", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    resident_id: parseInt(residentId), 
                    day: parseInt(day), 
                    month: parseInt(month), 
                    year: parseInt(year), 
                    workplace_id: workplaceId 
                })
            });
        } catch (err) {
            console.error("Ошибка:", err);
        }
    }
});