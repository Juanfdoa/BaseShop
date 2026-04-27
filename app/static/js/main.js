document.addEventListener("DOMContentLoaded", () => {

    // ───────── INIT EDITORES ─────────
    function initRichEditors(container = document) {
        container.querySelectorAll('[data-rich-editor]').forEach(function (input) {
            if (input.dataset.richEditorInit) return;
            input.dataset.richEditorInit = 'true';

            // Toolbar (solo bold)
            const toolbar = document.createElement('div');
            toolbar.innerHTML = `<button type="button"><b>B</b></button>`;

            // Editor
            const editor = document.createElement('div');
            editor.contentEditable = 'true';
            editor.style.border = '1px solid #ccc';
            editor.style.padding = '8px';
            editor.style.minHeight = '100px';

            editor.innerHTML = input.value || '';

            input.before(toolbar, editor);
            input.hidden = true;

            // Bold
            toolbar.querySelector('button').addEventListener('click', function () {
                editor.focus();
                document.execCommand('bold');
            });

            // ENTER = <br>
            editor.addEventListener('keydown', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    document.execCommand('insertLineBreak');
                }
            });

            // limpiar HTML (solo b + br)
            function cleanHTML(html) {
                const div = document.createElement('div');
                div.innerHTML = html;

                div.querySelectorAll('*').forEach(el => {
                    if (el.tagName !== 'B' && el.tagName !== 'BR') {
                        el.replaceWith(...el.childNodes);
                    }
                });

                return div.innerHTML;
            }

            // sincronizar en tiempo real
            editor.addEventListener('input', () => {
                input.value = cleanHTML(editor.innerHTML);
            });
        });
    }

    // inicializar en página
    initRichEditors();

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

                    // 🔥 IMPORTANTE: inicializar editores dentro del modal
                    setTimeout(() => {
                        initRichEditors();
                    }, 0);

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

        // 🔥 sincronizar editores antes de enviar
        form.querySelectorAll('[data-rich-editor]').forEach(input => {
            const editor = input.previousElementSibling;
            if (editor && editor.contentEditable === "true") {
                input.value = editor.innerHTML.trim();
            }
        });

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