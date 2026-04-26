document.addEventListener("DOMContentLoaded", () => {

    // ───────── CLICK GLOBAL ─────────
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
                    await sweetAlert.error({ text: "Error cargando el formulario" });
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

            const result = await sweetAlert.confirm();
            if (!result.isConfirmed) return;

            try {
                const res = await fetch(`/admin/${plural}/delete/${id}`, { method: "POST" });
                const data = await res.json();

                if (data.success) {
                    deleteBtn.closest(".accordion")?.remove();
                    await sweetAlert.success({ title: "Eliminado", text: data.message });
                } else {
                    await sweetAlert.error({ text: data.message });
                }

            } catch (err) {
                await sweetAlert.error({ text: "Error al eliminar" });
            }

            return;
        }

    });

    // ───────── SUBMIT GLOBAL ─────────
    document.addEventListener("submit", async (e) => {

        const form = e.target;
        if (!form.classList.contains("ajax-form")) return;
        e.preventDefault();

        if (form.dataset.confirm) {
            const result = await sweetAlert.confirm({
                title: form.dataset.confirmTitle || "¿Confirmar cambios?",
                text: form.dataset.confirmText || "Se guardarán los cambios"
            });
            if (!result.isConfirmed) return;
        }

        try {
            const res = await fetch(form.action, {
                method: form.method || "POST",
                body: new FormData(form)
            });
            const data = await res.json();
            closeModal();

            if (data.success) {
                await sweetAlert.success({ title: "Guardado", text: data.message });
                location.reload();
            } else {
                await sweetAlert.error({ text: data.message });
            }

        } catch (err) {
            await sweetAlert.error({ text: "Error al guardar" });
        }

    });

});