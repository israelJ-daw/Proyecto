const buscadorSubtareas = document.getElementById("buscador-subtareas");

if (buscadorSubtareas) {

    const idTarea = buscadorSubtareas.dataset.tareaId;
    const tablaSubtareas = document.getElementById("tabla-subtareas");

    buscadorSubtareas.addEventListener("input", function() {

        const buscar = buscadorSubtareas.value;

        fetch(`/buscar_subtarea/${idTarea}/?buscar=${encodeURIComponent(buscar)}`)
            .then(response => response.json())
            .then(datos => {

                tablaSubtareas.innerHTML = "";

                if (datos.length === 0) {

                    tablaSubtareas.innerHTML = `
                        <tr>
                            <td colspan="3" class="text-center py-4">
                                🔍 No se encontraron subtareas
                            </td>
                        </tr>
                    `;

                    return;
                }

                datos.forEach(subtarea => {

                    const icono = subtarea.completada ? "✅" : "📌";

                    const estado = subtarea.completada
                        ? "Completada"
                        : "Completar";

                    tablaSubtareas.innerHTML += `
                        <tr>

                            <td>
                                <div class="fw-semibold fs-6">
                                    ${icono} ${subtarea.titulo}
                                </div>
                            </td>

                            <td class="text-center">

                                <span class="badge ${
                                    subtarea.completada
                                        ? "bg-success"
                                        : "bg-secondary"
                                }">
                                    ${estado}
                                </span>

                            </td>

                            <td>

                                <div class="d-flex gap-2">

                                    <a href="/editar_subtarea/${subtarea.id}/"
                                       class="btn btn-guapo btn-sm">
                                        ✏️ Editar
                                    </a>

                                  <form method="POST"
                                    action="/eliminar_subtarea/${subtarea.id}/">

                                    <input type="hidden"
                                        name="csrfmiddlewaretoken"
                                        value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">

                                    <button type="submit"
                                            class="btn-eliminar btn-sm">
                                        🗑️ Eliminar
                                    </button>

                                </form>

                                </div>

                            </td>

                        </tr>
                    `;

                });

            })
            .catch(error => {
                console.error("Error al buscar subtareas:", error);
            });

    });

}