const buscadorProyectos = document.getElementById("buscador-proyectos");

if (buscadorProyectos) {

    const tablaProyectos = document.getElementById("tabla-proyectos");

    buscadorProyectos.addEventListener("input", function() {

        fetch("/buscar_proyecto/?buscar=" + encodeURIComponent(buscadorProyectos.value))
            .then(response => response.json())
            .then(datos => {

                tablaProyectos.innerHTML = "";

                if (datos.length === 0) {

                    tablaProyectos.innerHTML = `
                        <tr>
                            <td colspan="5" class="text-center py-4">
                                🔍 No se encontraron proyectos
                            </td>
                        </tr>
                    `;

                    return;
                }

                datos.forEach(proyecto => {

                    const fila = document.createElement("tr");

                    fila.innerHTML = `

                        <td>

                            <div class="fw-semibold fs-6">
                                📁

                                <a href="/detalle_proyecto/${proyecto.id}/"
                                   class="text-decoration-none">

                                    ${proyecto.nombre}

                                </a>

                            </div>

                        </td>

                        <td>
                            ${proyecto.descripcion
                                ? proyecto.descripcion
                                : '<span class="text-muted fst-italic">Sin descripción</span>'
                            }
                        </td>

                        <td>
                            ${proyecto.fecha_creacion}
                        </td>

                        <td>
                            ${proyecto.fecha_fin
                                ? proyecto.fecha_fin
                                : '<span class="text-muted">—</span>'
                            }
                        </td>

                        <td>

                            <div class="d-flex gap-2">

                                <a href="/editar_proyecto/${proyecto.id}/"
                                   class="btn btn-sm btn-guapo">

                                    ✏️ Editar

                                </a>

                                <a href="/detalle_proyecto/${proyecto.id}/"
                                   class="btn-proyecto">

                                    📋 Ver tareas

                                </a>

                            </div>

                        </td>

                    `;

                    tablaProyectos.appendChild(fila);

                });

            });

    });

}