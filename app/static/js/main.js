/**
 * Generadores de Números Pseudoaleatorios · 901N
 * Utilidades de interfaz: carrete de dígitos, histograma y exportación.
 */

// ---------------------------------------------------------------------------
// Carrete de dígitos (elemento firma de la portada)
// ---------------------------------------------------------------------------
function initDigitReel(contenedor, etiquetaRi) {
  if (!contenedor) return;
  const NUM_DIGITOS = 8;

  contenedor.innerHTML = "";
  const slots = [];
  for (let i = 0; i < NUM_DIGITOS; i++) {
    const slot = document.createElement("div");
    slot.className = "digit-slot";
    slot.textContent = "0";
    contenedor.appendChild(slot);
    slots.push(slot);
  }

  function girar() {
    let cadena = "";
    slots.forEach((slot) => {
      const digito = Math.floor(Math.random() * 10);
      slot.textContent = digito;
      cadena += digito;
    });
    if (etiquetaRi) {
      const ri = parseFloat("0." + cadena);
      etiquetaRi.textContent = ri.toFixed(4);
    }
  }

  girar();
  setInterval(girar, 900);
}

// ---------------------------------------------------------------------------
// Histograma simple (barras) para revisar uniformidad de los Ri generados
// ---------------------------------------------------------------------------
function dibujarHistograma(contenedor, valores, bins) {
  if (!contenedor || !valores || valores.length === 0) return;
  bins = bins || 10;

  const conteos = new Array(bins).fill(0);
  valores.forEach((v) => {
    let idx = Math.floor(v * bins);
    if (idx >= bins) idx = bins - 1;
    if (idx < 0) idx = 0;
    conteos[idx]++;
  });

  const maximo = Math.max(...conteos, 1);
  contenedor.innerHTML = "";

  conteos.forEach((conteo, i) => {
    const barra = document.createElement("div");
    barra.className = "hist-bar";
    barra.title = `[${(i / bins).toFixed(1)} – ${((i + 1) / bins).toFixed(1)}): ${conteo}`;

    const relleno = document.createElement("div");
    relleno.className = "hist-bar-fill";
    relleno.style.height = "0%";

    const etiqueta = document.createElement("span");
    etiqueta.className = "hist-bar-label";
    etiqueta.textContent = conteo;

    barra.appendChild(relleno);
    barra.appendChild(etiqueta);
    contenedor.appendChild(barra);

    requestAnimationFrame(() => {
      relleno.style.height = (conteo / maximo) * 100 + "%";
    });
  });
}

// ---------------------------------------------------------------------------
// Copiar / exportar la tabla de resultados
// ---------------------------------------------------------------------------
function configurarExportacion(idTabla, idBtnCopiar, idBtnExportar, nombreArchivo) {
  const tabla = document.getElementById(idTabla);
  const btnCopiar = document.getElementById(idBtnCopiar);
  const btnExportar = document.getElementById(idBtnExportar);
  if (!tabla) return;

  function obtenerCSV() {
    const filas = [];
    tabla.querySelectorAll("tr").forEach((tr) => {
      const celdas = [...tr.children].map((celda) =>
        celda.innerText.trim().replace(/\s+/g, " ")
      );
      filas.push(celdas.join(","));
    });
    return filas.join("\n");
  }

  if (btnCopiar) {
    btnCopiar.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(obtenerCSV());
        const original = btnCopiar.innerHTML;
        btnCopiar.innerHTML = '<i class="bi bi-check2"></i> Copiado';
        btnCopiar.disabled = true;
        setTimeout(() => {
          btnCopiar.innerHTML = original;
          btnCopiar.disabled = false;
        }, 1400);
      } catch (err) {
        console.warn("No se pudo copiar al portapapeles:", err);
      }
    });
  }

  if (btnExportar) {
    btnExportar.addEventListener("click", () => {
      const blob = new Blob([obtenerCSV()], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const enlace = document.createElement("a");
      enlace.href = url;
      enlace.download = `${nombreArchivo || "resultados"}.csv`;
      document.body.appendChild(enlace);
      enlace.click();
      enlace.remove();
      URL.revokeObjectURL(url);
    });
  }
}

// ---------------------------------------------------------------------------
// Cierre automático de alertas tras unos segundos
// ---------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".app-alert").forEach((alerta) => {
    setTimeout(() => {
      const instancia = bootstrap.Alert.getOrCreateInstance(alerta);
      instancia.close();
    }, 8000);
  });
});