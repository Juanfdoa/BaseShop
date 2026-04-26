const sweetAlert = {

    confirm: ({ title = "¿Estás seguro?", text = "Esta acción no se puede deshacer" } = {}) => {
        return Swal.fire({
            title,
            text,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3D5A80",
            cancelButtonColor: "#aaa",
            confirmButtonText: "Sí, confirmar",
            cancelButtonText: "Cancelar"
        });
    },

    success: ({ title = "Éxito", text = "", timer = 1500 } = {}) => {
        return Swal.fire({
            icon: "success",
            title,
            text,
            timer,
            showConfirmButton: false
        });
    },

    error: ({ title = "Error", text = "" } = {}) => {
        return Swal.fire({
            icon: "error",
            title,
            text
        });
    }

};