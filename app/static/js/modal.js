document.addEventListener("DOMContentLoaded", () => {

    // ───────── ELEMENTOS ─────────
    const modal = document.getElementById("modal");
    const modalBody = document.getElementById("modalBody");
    const modalTitle = document.getElementById("modalTitle");
    const closeModalBtn = document.getElementById("closeModal");
    const overlay = document.getElementById("modalOverlay");

    // ───────── MODAL ─────────
    function openModal({ title = "Modal", content = "" }) {
        modalTitle.innerText = title;
        modalBody.innerHTML = content;
        modal.classList.add("active");
    }

    function closeModal() {
        modal.classList.remove("active");
        modalBody.innerHTML = "";
    }

    if (closeModalBtn) closeModalBtn.addEventListener("click", closeModal);
    if (overlay) overlay.addEventListener("click", closeModal);

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") closeModal();
    });

    // ───────── CLICK GLOBAL (MODAL + DELETE) ─────────
    document.addEventListener("click", async (e) => {

        // 🔹 ABRIR MODAL
        const modalBtn = e.target.closest("[data-modal]");
        if (modalBtn) {
            e.preventDefault();

            const title = modalBtn.dataset.title || "Formulario";

            if (modalBtn.dataset.url) {
                try {
                    const res = await fetch(modalBtn.dataset.url);
                    const html = await res.text();
                    openModal({ title, content: html });
                } catch (err) {
                    console.error("Error cargando modal:", err);
                }
            }

            return;
        }

        // 🔥 DELETE
        const deleteBtn = e.target.closest(".btn-delete");
        if (deleteBtn) {

            const id = deleteBtn.dataset.id;
            const type = deleteBtn.dataset.type;
            const plural = type === "category" ? "categories" : type + "s";

            const result = await Swal.fire({
                title: "¿Estás seguro?",
                text: "Esta acción no se puede deshacer",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#3D5A80",
                cancelButtonColor: "#aaa",
                confirmButtonText: "Sí, eliminar"
            });

            if (!result.isConfirmed) return;

            try {
                const res = await fetch(`/admin/${plural}/delete/${id}`, {
                    method: "POST"
                });

                const data = await res.json();

                if (data.success) {

                    // eliminar del DOM
                    const item = deleteBtn.closest(".accordion");
                    if (item) item.remove();

                    Swal.fire({
                        icon: "success",
                        title: "Eliminado",
                        text: data.message,
                        timer: 1500,
                        showConfirmButton: false
                    });
                }

            } catch (err) {
                console.error("Error eliminando:", err);
            }

            return;
        }

    });

    // ───────── SUBMIT GLOBAL ─────────
    document.addEventListener("submit", async (e) => {

        const form = e.target;

        if (!form.classList.contains("ajax-form")) return;

        e.preventDefault();

        const formData = new FormData(form);
        const url = form.getAttribute("action");
        const method = form.getAttribute("method") || "POST";

        try {
            const res = await fetch(url, {
                method,
                body: formData
            });

            const data = await res.json();

            closeModal();

            if (data.success) {
                location.reload();
            }

        } catch (err) {
            console.error("Error en submit:", err);
        }

    });

});