const buscador = document.getElementById("buscador");

const tabla = document.getElementById("tabla-tareas");

const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

buscador.addEventListener("input", function() {

    fetch("/buscar_tarea/?buscar=" + buscador.value)
        .then(response => response.json())
        .then(datos => {

            tabla.innerHTML = "";

            // Si no hay resultados
            if (datos.length === 0) {

                tabla.innerHTML = `
                    <tr>
                        <td colspan="8" class="text-center">
                            🔎 No se encontraron tareas
                        </td>
                    </tr>
                `;

                return;
            }

            // Crear una fila por cada tarea
            datos.forEach(tarea => {

                const fila = document.createElement("tr");

                fila.innerHTML = `

                    <!-- TÍTULO -->
                    <td>

                        <div class="fw-semibold fs-6">
                            📋 ${tarea.titulo}
                        </div>

                        ${
                            tarea.descripcion
                                ? `
                                    <small class="text-muted">
                                        ${tarea.descripcion}
                                    </small>
                                  `
                                : ""
                        }

                    </td>


                    <!-- ESTADO -->
                    <td>

                        <span class="badge
                            ${
                                tarea.estado === "pendiente"
                                    ? "bg-warning text-dark"
                                    : tarea.estado === "en_progreso"
                                        ? "bg-info text-dark"
                                        : tarea.estado === "completada"
                                            ? "bg-success"
                                            : "bg-secondary"
                            }">

                            ${
                                tarea.estado === "pendiente"
                                    ? "Pendiente"
                                    : tarea.estado === "en_progreso"
                                        ? "En progreso"
                                        : tarea.estado === "completada"
                                            ? "Completada"
                                            : tarea.estado
                            }

                        </span>

                    </td>


                    <!-- PRIORIDAD -->
                    <td>

                        <span class="badge
                            ${
                                tarea.prioridad === "alta"
                                    ? "bg-danger"
                                    : tarea.prioridad === "media"
                                        ? "bg-warning text-dark"
                                        : "bg-success"
                            }">

                            ${
                                tarea.prioridad === "alta"
                                    ? "Alta"
                                    : tarea.prioridad === "media"
                                        ? "Media"
                                        : "Baja"
                            }

                        </span>

                    </td>


                    <!-- FECHA -->
                    <td>

                        ${
                            tarea.fecha_vencimiento
                                ? tarea.fecha_vencimiento
                                : `<span class="text-muted">—</span>`
                        }

                    </td>


                    <!-- PROYECTO -->
                    <td>

                        ${
                            tarea.proyecto
                                ? `
                                    <a href="/detalle-proyecto/${tarea.proyecto.id}"
                                       class="btn-proyecto">

                                        📁 ${tarea.proyecto.nombre}

                                    </a>
                                  `
                                : `
                                    <a href="/asignar-proyecto-tarea/${tarea.id}"
                                       class="btn btn-proyecto btn-sm">

                                        ➕ Añadir

                                    </a>
                                  `
                        }

                    </td>


                    <!-- CATEGORÍA -->
                    <td>

                        ${
                            tarea.categoria
                                ? `
                                    <div class="border rounded-3 p-2">

                                        <div class="fw-semibold">
                                            🏷️ ${tarea.categoria.nombre}
                                        </div>

                                        ${
                                            tarea.categoria.descripcion
                                                ? `
                                                    <small class="text-muted">
                                                        ${tarea.categoria.descripcion}
                                                    </small>
                                                  `
                                                : ""
                                        }

                                        <div class="mt-2">

                                            <a href="/asignar-categoria-tarea/${tarea.id}"
                                               class="btn btn-guapo2 btn-sm w-100">

                                                🔄 Cambiar

                                            </a>

                                        </div>

                                    </div>
                                  `
                                : `
                                    <a href="/asignar-categoria-tarea/${tarea.id}"
                                       class="btn btn-proyecto btn-sm">

                                        ➕ Añadir

                                    </a>
                                  `
                        }

                    </td>


                    <!-- COMPLETADA -->
                    <td class="text-center">

                        <form method="post"
                            action="/eliminar/tarea/${tarea.id}"
                            class="form-completar">

                            <input type="hidden"
                                name="csrfmiddlewaretoken"
                                value="${csrfToken}">

                            <label class="check-completar">

                                <input
                                    type="checkbox"
                                    class="completar-tarea"
                                    ${tarea.completada ? "checked" : ""}
                                >

                                <span class="texto-completar">

                                    ${
                                        tarea.completada
                                            ? "Completada"
                                            : "Completar"
                                    }

                                </span>

                            </label>

                        </form>

                    </td>


                    <!-- ACCIONES -->
                    <td>

                        <div class="d-flex flex-column gap-2">

                            <a href="/editar/tarea/${tarea.id}"
                               class="btn btn-guapo btn-sm">
                                ✏️ Editar
                            </a>

                            <form method="post"
                                action="/eliminar/tarea/${tarea.id}">

                                <input type="hidden"
                                    name="csrfmiddlewaretoken"
                                    value="${csrfToken}">

                                <button type="submit"
                                        class="btn-eliminar w-100">
                                    🗑️ Eliminar

                                </button>

                            </form>

                            <a href="/listar_subtareas/${tarea.id}/"
                                class="btn-proyecto text-center">

                                    📋 Subtareas

                            </a>

                        </div>

                    </td>

                `;

                tabla.appendChild(fila);

            });

        });

});