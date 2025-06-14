let params = null; // Parameters
let colsEdi = null;
const newColHtml = '<div class="btn-group pull-right">' +
    '<button id="bEdit" type="button" class="btn btn-sm btn-default" onclick="rowEdit(this);">' +
    '<span class="glyphicon glyphicon-pencil"> </span>' +
    '</button>' +
    '<button id="bElim" type="button" class="btn btn-sm btn-default" onclick="rowElim(this);">' +
    '<span class="glyphicon glyphicon-trash"> </span>' +
    '</button>' +
    '<button id="bAcep" type="button" class="btn btn-sm btn-default" style="display:none;" onclick="rowAcep(this);">' +
    '<span class="glyphicon glyphicon-ok"> </span>' +
    '</button>' +
    '<button id="bCanc" type="button" class="btn btn-sm btn-default" style="display:none;" onclick="rowCancel(this);">' +
    '<span class="glyphicon glyphicon-remove"> </span>' +
    '</button>' +
    '</div>';
const colEdicHtml = '<td name="buttons">' + newColHtml + '</td>';

HTMLElement.prototype.SetEditable = function (options) {
    const defaults = {
        columnsEd: null, // Index to editable columns. If null all td editables. Ex.: "1,2,3,4,5"
        addButton: null, // DOM object of "Add" button
        onEdit: function () { }, // Called after edition
        onBeforeDelete: function () { }, // Called before deletion
        onDelete: function () { }, // Called after deletion
        onAdd: function () { } // Called when added a new row
    };
    params = Object.assign(defaults, options);

    const theadRow = this.querySelector('thead tr');
    const th = document.createElement('th');
    th.setAttribute('name', 'buttons');
    theadRow.appendChild(th);

    const tbodyRows = this.querySelectorAll('tbody tr');
    tbodyRows.forEach(row => {
        row.insertAdjacentHTML('beforeend', colEdicHtml);
    });

    const tabedi = this;

    // Process "addButton" parameter
    if (params.addButton) {
        params.addButton.addEventListener('click', function () {
            rowAddNew(tabedi.id);
        });
    }

    // Process "columnsEd" parameter
    if (params.columnsEd) {
        colsEdi = params.columnsEd.split(',');
    }
};

function IterarCamposEdit(cols, tarea) {
    // Itera por los campos editables de una fila
    let n = 0;
    for (let i = 0; i < cols.length; i++) {
        const col = cols[i];
        n++;
        if (col.getAttribute('name') === 'buttons') continue; // excluye columna de botones
        if (!EsEditable(n - 1)) continue; // no es campo editable
        tarea(col);
    }

    function EsEditable(idx) {
        // Indica si la columna pasada está configurada para ser editable
        if (colsEdi === null) { // no se definió
            return true; // todas son editable
        } else { // hay filtro de campos
            for (let i = 0; i < colsEdi.length; i++) {
                if (idx === parseInt(colsEdi[i])) return true;
            }
            return false; // no se encontró
        }
    }
}

function FijModoNormal(but) {
    const parent = but.parentNode;
    const bAcep = parent.querySelector('#bAcep');
    const bCanc = parent.querySelector('#bCanc');
    const bEdit = parent.querySelector('#bEdit');
    const bElim = parent.querySelector('#bElim');
    bAcep.style.display = 'none';
    bCanc.style.display = 'none';
    bEdit.style.display = 'inline-block';
    bElim.style.display = 'inline-block';
    const row = but.closest('tr');
    row.removeAttribute('id');
}

function FijModoEdit(but) {
    const parent = but.parentNode;
    const bAcep = parent.querySelector('#bAcep');
    const bCanc = parent.querySelector('#bCanc');
    const bEdit = parent.querySelector('#bEdit');
    const bElim = parent.querySelector('#bElim');
    bAcep.style.display = 'inline-block';
    bCanc.style.display = 'inline-block';
    bEdit.style.display = 'none';
    bElim.style.display = 'none';
    const row = but.closest('tr');
    row.setAttribute('id', 'editing');
}

function ModoEdicion(row) {
    return row.getAttribute('id') === 'editing';
}

function rowAcep(but) {
    // Acepta los cambios de la edición
    const row = but.closest('tr');
    const cols = row.querySelectorAll('td');
    if (!ModoEdicion(row)) return; // Ya está en edición
    // Está en edición. Hay que finalizar la edición
    IterarCamposEdit(cols, function (td) {
        const input = td.querySelector('input');
        const cont = input.value;
        td.innerHTML = cont;
    });
    FijModoNormal(but);
    params.onEdit(row);
}

function rowCancel(but) {
    // Rechaza los cambios de la edición
    const row = but.closest('tr');
    const cols = row.querySelectorAll('td');
    if (!ModoEdicion(row)) return; // Ya está en edición
    // Está en edición. Hay que finalizar la edición
    IterarCamposEdit(cols, function (td) {
        const div = td.querySelector('div');
        const cont = div.innerHTML;
        td.innerHTML = cont;
    });
    FijModoNormal(but);
}

function rowEdit(but) {
    // Inicia la edición de una fila
    const row = but.closest('tr');
    const cols = row.querySelectorAll('td');
    if (ModoEdicion(row)) return; // Ya está en edición
    // Pone en modo de edición
    IterarCamposEdit(cols, function (td) {
        const cont = td.innerHTML;
        const div = document.createElement('div');
        div.style.display = 'none';
        div.innerHTML = cont;
        const input = document.createElement('input');
        input.className = 'form-control input-sm';
        input.value = cont;
        td.innerHTML = '';
        td.appendChild(div);
        td.appendChild(input);
    });
    FijModoEdit(but);
}

function rowElim(but) {
    // Elimina la fila actual
    const row = but.closest('tr');
    params.onBeforeDelete(row);
    row.remove();
    params.onDelete();
}

function rowAddNew(tabId) {
    // Agrega fila a la tabla indicada.
    const tab_en_edic = document.getElementById(tabId);
    const filas = tab_en_edic.querySelectorAll('tbody tr');
    if (filas.length === 0) {
        // No hay filas de datos. Hay que crearlas completas
        const row = tab_en_edic.querySelector('thead tr');
        const cols = row.querySelectorAll('th');
        // construye html
        let htmlDat = '';
        cols.forEach(col => {
            if (col.getAttribute('name') === 'buttons') {
                // Es columna de botones
                htmlDat += colEdicHtml;
            } else {
                htmlDat += '<td></td>';
            }
        });
        tab_en_edic.querySelector('tbody').insertAdjacentHTML('beforeend', '<tr>' + htmlDat + '</tr>');
    } else {
        // Hay otras filas, podemos clonar la última fila, para copiar los botones
        const ultFila = tab_en_edic.querySelector('tr:last-child');
        const newRow = ultFila.cloneNode(true);
        tab_en_edic.querySelector('tbody').appendChild(newRow);
        const cols = newRow.querySelectorAll('td');
        cols.forEach(col => {
            if (col.getAttribute('name') === 'buttons') {
                // Es columna de botones
            } else {
                col.innerHTML = '';
            }
        });
    }
    params.onAdd();
}

function TableToCSV(tabId, separator) {
    // Convierte tabla a CSV
    let datFil = '';
    let tmp = '';
    const tab_en_edic = document.getElementById(tabId);
    const rows = tab_en_edic.querySelectorAll('tbody tr');
    rows.forEach(row => {
        // Termina la edición si es que existe
        if (ModoEdicion(row)) {
            const bAcep = row.querySelector('#bAcep');
            bAcep.click(); // acepta edición
        }
        const cols = row.querySelectorAll('td');
        datFil = '';
        cols.forEach(col => {
            if (col.getAttribute('name') === 'buttons') {
                // Es columna de botones
            } else {
                datFil += col.innerHTML + separator;
            }
        });
        if (datFil !== '') {
            datFil = datFil.slice(0, -separator.length);
        }
        tmp += datFil + '\n';
    });
    return tmp;
}

const myTable = document.getElementById('mytable');
const addButton = document.getElementById('add');
myTable.SetEditable({
    addButton: addButton
});