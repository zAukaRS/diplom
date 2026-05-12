document.addEventListener("DOMContentLoaded", function () {

    // Если токен уже есть — сразу на главную
    if (localStorage.getItem("access_token")) {
        window.location.href = "/home";
        return;
    }

    const form = document.getElementById("loginForm");
    const errorEl = document.getElementById("errorMessage");

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        errorEl.textContent = "";

        const formData = new FormData(form);

        try {
            const res = await fetch("/api/auth/login", {
                method: "POST",
                body: new URLSearchParams({
                    username: formData.get("username"),
                    password: formData.get("password")
                })
            });

            if (!res.ok) {
                const data = await res.json().catch(() => ({}));
                errorEl.textContent = data.detail || "Неверный логин или пароль";
                return;
            }

            const data = await res.json();
            localStorage.setItem("access_token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);
            window.location.href = "/home";

        } catch (err) {
            errorEl.textContent = "Ошибка соединения с сервером";
            console.error("Ошибка входа:", err);
        }
    });
});