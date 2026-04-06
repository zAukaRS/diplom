document.getElementById("downloadReportBtn").addEventListener("click", async () => {

    const field = document.getElementById("fieldFilter").value;
    const year = document.getElementById("yearFilter").value;
    const month = document.getElementById("monthFilter").value;

    // получаем жителей
    const res = await fetch(`/api/residents?field=${field}&year=${year}&month=${month}`);
    const residents = await res.json();

    // получаем workplaces
    const wpRes = await fetch("/api/workplaces");
    const workplaces = await wpRes.json();

    // создаем счетчик
    const stats = {};

    workplaces.forEach(w => {
        stats[w.id] = {
            name: w.name,
            hostel: 0,
            wagon: 0
        };
    });

    // 🔥 считаем дни
    residents.forEach(r => {
        if (!r.days_info) return;

        Object.values(r.days_info).forEach(workplaceId => {
            if (!workplaceId) return;

            // определяем тип проживания
            const isWagon = (r.room_location || "").toLowerCase().includes("вагон");

            if (stats[workplaceId]) {
                if (isWagon) {
                    stats[workplaceId].wagon += 1;
                } else {
                    stats[workplaceId].hostel += 1;
                }
            }
        });
    });

    // --- создаем excel ---
    const wb = XLSX.utils.book_new();
    const wsData = [];

    // месяц
    wsData.push(["Январь", "", "", ""]);

    // заголовки
    wsData.push(["", "Общежитие", "Вагоны", "Итог"]);

    // строки
    Object.values(stats).forEach(w => {
        const total = w.hostel + w.wagon;

        wsData.push([
            w.name,
            w.hostel,
            w.wagon,
            total
        ]);
    });

    const ws = XLSX.utils.aoa_to_sheet(wsData);

    // merge
    ws["!merges"] = [
        { s: { r: 0, c: 0 }, e: { r: 0, c: 3 } }
    ];

    // ширина
    ws["!cols"] = [
        { wch: 30 },
        { wch: 15 },
        { wch: 15 },
        { wch: 15 }
    ];

    XLSX.utils.book_append_sheet(wb, ws, "Отчет");

    XLSX.writeFile(wb, "report.xlsx");
});