document.addEventListener("DOMContentLoaded", async () => {
    if (!getToken()) { window.location.href = "/login"; return; }

    const tbody       = document.querySelector("#requestsTable tbody");
    const table       = document.getElementById("requestsTable");
    const loadingMsg  = document.getElementById("loadingMsg");
    const noDataMsg   = document.getElementById("noDataMsg");
    const summaryEl   = document.getElementById("summary");

    let allRequests = [];   // полный список, загружается один раз

    // ── Загрузка ────────────────────────────────────────────────────────────
    async function loadAll() {
        loadingMsg.style.display = "";
        table.style.display = "none";
        noDataMsg.style.display = "none";

        try {
            const res = await apiFetch("/api/requests/all");
            if (!res.ok) {
                loadingMsg.textContent = "Ошибка загрузки заявок";
                return;
            }
            allRequests = await res.json();
        } catch (e) {
            loadingMsg.textContent = "Ошибка сервера";
            return;
        }

        loadingMsg.style.display = "none";
        renderTable(allRequests);
    }

    // ── Рендер таблицы ──────────────────────────────────────────────────────
    function renderTable(requests) {
        tbody.innerHTML = "";

        if (requests.length === 0) {
            table.style.display = "none";
            noDataMsg.style.display = "";
            summaryEl.textContent = "";
            return;
        }

        table.style.display = "";
        noDataMsg.style.display = "none";

        const counts = { pending: 0, approved: 0, rejected: 0 };

        for (const req of requests) {
            counts[req.status] = (counts[req.status] || 0) + 1;

            const statusBadge = {
                pending:  '<span class="badge badge-pending">Ожидает</span>',
                approved: '<span class="badge badge-approved">Одобрена</span>',
                rejected: '<span class="badge badge-rejected">Отклонена</span>',
            }[req.status] || req.status;

            const sourceLabel = req.source === "request"
                ? '<span class="src-req">✔ утверждённая</span>'
                : '<span class="src-rb">⏳ черновик</span>';

            // Кнопка «Отклонить» — только если статус не rejected
            const rejectBtn = req.status !== "rejected"
                ? `<button class="action-btn reject-btn"
                           data-id="${req.id}"
                           data-source="${req.source}">Отклонить</button>`
                : "";

            const tr = document.createElement("tr");
            tr.dataset.id     = req.id;
            tr.dataset.source = req.source;
            tr.dataset.status = req.status;

            tr.innerHTML = `
                <td>${req.id}</td>
                <td>${sourceLabel}</td>
                <td>${statusBadge}</td>
                <td>${req.user_id}</td>
                <td>${req.field_name || req.field_id}</td>
                <td>${req.full_name || "—"}</td>
                <td>${req.position || "—"}</td>
                <td style="white-space:nowrap">${req.check_in} — ${req.check_out}</td>
                <td>${req.room_id || "—"}</td>
                <td>${req.customer || "—"}</td>
                <td>${req.contract_num || "—"}</td>
                <td>${req.eol_fio || "—"}</td>
                <td>${req.comment || "—"}</td>
                <td>${req.admin_comment || "—"}</td>
                <td style="white-space:nowrap;font-size:11px">${req.created_at ? req.created_at.slice(0, 16) : "—"}</td>
                <td class="actions">${rejectBtn}</td>
            `;
            tbody.appendChild(tr);
        }

        summaryEl.textContent =
            `Всего: ${requests.length} | ` +
            `Ожидают: ${counts.pending || 0} | ` +
            `Одобрены: ${counts.approved || 0} | ` +
            `Отклонены: ${counts.rejected || 0}`;

        attachRejectHandlers();
    }

    // ── Обработчики «Отклонить» ─────────────────────────────────────────────
    function attachRejectHandlers() {
        document.querySelectorAll(".reject-btn").forEach(btn => {
            btn.addEventListener("click", async () => {
                const id     = btn.dataset.id;
                const source = btn.dataset.source;

                const comment = prompt("Комментарий к отклонению (необязательно):");
                if (comment === null) return;   // нажали «Отмена»

                try {
                    const res = await apiFetch(
                        `/api/requests/${id}/reject_admin?source=${encodeURIComponent(source)}`,
                        {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ admin_comment: comment }),
                        }
                    );
                    if (res.ok) {
                        // Обновляем локальные данные без повторного запроса
                        const item = allRequests.find(r => r.id == id && r.source === source);
                        if (item) {
                            item.status = "rejected";
                            item.admin_comment = comment;
                        }
                        applyFilters();
                    } else {
                        const err = await res.json().catch(() => ({}));
                        alert("Ошибка: " + (err.detail || res.status));
                    }
                } catch (e) {
                    alert("Ошибка сервера");
                }
            });
        });
    }

    // ── Фильтрация ──────────────────────────────────────────────────────────
    window.applyFilters = function () {
        const status  = document.getElementById("filterStatus").value;
        const source  = document.getElementById("filterSource").value;
        const search  = document.getElementById("filterSearch").value.trim().toLowerCase();

        const filtered = allRequests.filter(r => {
            if (status && r.status !== status) return false;
            if (source && r.source !== source) return false;
            if (search) {
                const haystack = [
                    r.full_name, r.eol_fio, r.customer,
                    r.contract_num, r.position, r.comment,
                ].join(" ").toLowerCase();
                if (!haystack.includes(search)) return false;
            }
            return true;
        });

        renderTable(filtered);
    };

    window.resetFilters = function () {
        document.getElementById("filterStatus").value  = "";
        document.getElementById("filterSource").value  = "";
        document.getElementById("filterSearch").value  = "";
        renderTable(allRequests);
    };

    // Применять фильтр по статусу при изменении (удобно)
    document.getElementById("filterStatus").addEventListener("change", applyFilters);
    document.getElementById("filterSource").addEventListener("change", applyFilters);
    document.getElementById("filterSearch").addEventListener("input",  applyFilters);

    loadAll();
});