document.addEventListener("DOMContentLoaded", () => {

    // ───────── ELEMENTOS ─────────
    const modal = document.getElementById("modal");
    const modalBody = document.getElementById("modalBody");
    const modalTitle = document.getElementById("modalTitle");
    const closeModalBtn = document.getElementById("closeModal");
    const overlay = document.getElementById("modalOverlay");

    // ───────── FUNCIONES ─────────
    window.openModal = function({ title = "Modal", content = "" }) {
        modalTitle.innerText = title;
        modalBody.innerHTML = content;
        modal.classList.add("active");
    };

    window.closeModal = function() {
        modal.classList.remove("active");
        modalBody.innerHTML = "";
    };

    // ───────── EVENTOS ─────────
    if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);
    if (overlay) overlay.addEventListener("click", closeModal);

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeModal();
    });

});