function TableHideShow(obj) {
    let checkbox_name = obj.id;
    if (obj.checked === false) {
        let filterElements_head = document.querySelectorAll('#document_head th');
        filterElements_head.forEach(item => {
            if (item.id.indexOf(checkbox_name) > -1) {
                item.setAttribute('hidden', '');
            }
        });

        let filterElements_body = document.querySelectorAll('#document_data td');
        filterElements_body.forEach(item => {
            if (item.id.indexOf(checkbox_name) > -1) {
                item.setAttribute('hidden', '');
            }
        })
    } else {
        let filterElements_head = document.querySelectorAll('#document_head th');
        filterElements_head.forEach(item => {
            if (item.id.indexOf(checkbox_name) > -1) {
                item.removeAttribute('hidden');
            }
        });

        let filterElements_body = document.querySelectorAll('#document_data td');
        filterElements_body.forEach(item => {
            if (item.id.indexOf(checkbox_name) > -1) {
                item.removeAttribute('hidden');
            }
        })
    }
}

function show_by_status(obj) {
    if (obj.name === "show_work") {
        filter = "в работе";
    } else if (obj.name === 'show_pending') {
        filter = "в ожидании";
    } else if (obj.name === 'show_not_passed') {
        filter = "не использован"
    } else {
        filter = "в архиве";
    }

    let filterElements = document.querySelectorAll('#document_data');
    filterElements.forEach(item => {
        if (item.querySelector('#document_status').innerHTML.toLowerCase().indexOf(filter) > -1) {
            item.removeAttribute('hidden');
        } else {
            item.setAttribute('hidden', '');
        }
    })
}

function crossing_point_choice(obj) {
    let filter = obj.options[obj.selectedIndex].text.toLowerCase();
    if (filter === 'любой') {
        let filterElements = document.querySelectorAll('#document_data');
        filterElements.forEach(item => {
            item.removeAttribute('hidden');
        })
    } else {
        let filterElements = document.querySelectorAll('#document_data');
        filterElements.forEach(item => {
            if (item.querySelector('#document_crossing_point').innerHTML.toLowerCase().indexOf(filter) > -1) {
                item.removeAttribute('hidden');
            } else {
                item.setAttribute('hidden', '');
            }
        })
    }
}

function reset_filters() {
    let filterElements_head_th = document.querySelectorAll('#document_head th');
    filterElements_head_th.forEach(item => {
        item.removeAttribute('hidden');
    });

    let filterElements_body_td = document.querySelectorAll('#document_data td');
    filterElements_body_td.forEach(item => {
        item.removeAttribute('hidden');
    });

    let filterElements_body_tr = document.querySelectorAll('#document_data');
    filterElements_body_tr.forEach(item => {
        item.removeAttribute('hidden');
    })

    let checkboxes = document.querySelectorAll('#popup input');
    checkboxes.forEach(item => {
        item.checked = false;
    })

    let checkpoint_choice = document.getElementById('checkpoint_choice')
    checkpoint_choice.options[0].selected = true;
}

document.addEventListener('DOMContentLoaded', () => {

    const getSort = ({target}) => {
        const order = (target.dataset.order = -(target.dataset.order || -1));
        const index = [...target.parentNode.cells].indexOf(target);
        const collator = new Intl.Collator(['en', 'ru'], {numeric: true});
        const comparator = (index, order) => (a, b) => order * collator.compare(
            a.children[index].innerHTML,
            b.children[index].innerHTML
        );

        for (const tBody of target.closest('table').tBodies)
            tBody.append(...[...tBody.rows].sort(comparator(index, order)));

        for (const cell of target.parentNode.cells)
            cell.classList.toggle('sorted', cell === target);
    };

    document.querySelectorAll('.table_sort thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));

});

function HideShow(obj) {
    let form;
    if (obj.id === 'automobile_checkbox') {
        form = document.getElementById('automobile_form')
    } else {
        form = document.getElementById('driver_form')
        if (obj.checked === false) {
            document.getElementById('automobile_checkbox').classList.add('d-none');
        } else {
            document.getElementById('automobile_checkbox').classList.remove('d-none');
        }
    }

    if (obj.checked === true) {
        form.setAttribute('hidden', '')
    } else {
        form.removeAttribute('hidden')
    }
}

function OneTimePass(obj) {
    if (obj.checked) {
        document.getElementById('date_end_div').setAttribute('hidden', '');
    } else {
        document.getElementById('date_end_div').removeAttribute('hidden');
    }
}

function CreateError(error_text, error_to) {
    const div = document.createElement("div");
    div.className = "alert alert-danger alert-dismissible fade show my-2";

    const strong = document.createElement("strong");
    const strongText = document.createTextNode("Ошибка! ");
    strong.appendChild(strongText);
    div.appendChild(strong);

    const span = document.createElement("span");
    span.id = "basic-addon1";
    const spanText = document.createTextNode(error_text);
    span.appendChild(spanText);
    div.appendChild(span);

    const button = document.createElement("button");
    button.type = "button";
    button.className = "btn-close shadow-none";
    button.setAttribute("data-bs-dismiss", "alert");
    div.appendChild(button);

    document.getElementById(error_to).appendChild(div);
}

$(document).on('submit', '#automobile_form', function (e) {
    e.preventDefault();

    let data = $('#automobile_form').serializeArray();
    data.push({name: "form_to_check_automobile", value: ""});

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (response) {
            if ('error_automobile' in response) {
                CreateError(response['error_automobile'], 'error_automobile');
            } else if ('automobile_update' in response) {
                document.getElementById('automobile_form').setAttribute('hidden', '');
                document.getElementById('automobile_checkbox').setAttribute('hidden', '');
                document.getElementById('driver_form').setAttribute('hidden', '');
                document.getElementById('driver_checkbox').setAttribute('hidden', '');
                let select = document.getElementById('auto_select');
                select.querySelector(`[value='${response['auto_id']}']`).remove();
                let new_auto = document.createElement('option');
                new_auto.value = response['auto_id'];
                new_auto.innerHTML = response['license_plate'];
                $('#auto_select').append(new_auto);
                select.querySelector(`[value='${response['auto_id']}']`).selected = true;
            } else {
                document.getElementById('automobile_form').setAttribute('hidden', '');
                document.getElementById('automobile_checkbox').setAttribute('hidden', '');
                document.getElementById('driver_form').setAttribute('hidden', '');
                document.getElementById('driver_checkbox').setAttribute('hidden', '');
                let new_auto = document.createElement('option');
                new_auto.value = response['auto_id'];
                new_auto.innerHTML = response['license_plate'];
                $('#auto_select').append(new_auto);
                let select = document.getElementById('auto_select');
                select.querySelector(`[value='${response['auto_id']}']`).selected = true;
            }
        }
    });
})

$(document).on('submit', '#driver_form', function (e) {
    e.preventDefault();

    let data = $('#driver_form').serializeArray();
    data.push({name: "form_to_check_driver", value: ""});

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        success: function (response) {
            if ('error_driver' in response) {
                CreateError(response['error_driver'], 'error_driver');
            } else if ('driver_update' in response) {
                document.getElementById('driver_form').setAttribute('hidden', '');
                document.getElementById('driver_checkbox').setAttribute('hidden', '');
                let select = document.getElementById('driver_select');
                select.querySelector(`[value='${response['driver_id']}']`).remove();
                let new_auto = document.createElement('option');
                new_auto.value = response['driver_id'];
                new_auto.innerHTML = response['driver'];
                $('#driver_select').append(new_auto);
                select.querySelector(`[value='${response['driver_id']}']`).selected = true;
            } else {
                document.getElementById('driver_form').setAttribute('hidden', '');
                document.getElementById('driver_checkbox').setAttribute('hidden', '');
                let new_auto = document.createElement('option');
                new_auto.value = response['driver_id'];
                new_auto.innerHTML = response['driver'];
                $('#driver_select').append(new_auto);
                let select = document.getElementById('driver_select');
                select.querySelector(`[value='${response['driver_id']}']`).selected = true;
            }
        }
    });
})

$(document).on('submit', '#document_form', function () {
    if (document.getElementById('one_time_pass').checked) {
        document.getElementById('date_end').value = document.getElementById('date_start').value;
    }
})

function selectAll() {
    const checkboxes = document.querySelectorAll('input[id="document_choose_checkbox"]');
    let button = document.getElementById('select_all_button');
    checkboxes.forEach(function (checkbox) {
        if (checkbox.checked) {
            checkbox.checked = !checkbox.checked
            button.innerHTML = "Выбрать все записи";
        } else {
            checkbox.checked = !checkbox.checked
            button.innerHTML = "Выбрать все записи ✔";
        }
    });
}

$(document).ready(function () {
    $('.status_select').select2({
        theme: 'bootstrap-5'
    })
    $('.custom_status_select').select2({
        theme: 'bootstrap-5'
    })
    $('.auto_select').select2({
        theme: 'bootstrap-5'
    });
    $('.driver_select').select2({
        theme: 'bootstrap-5'
    });
    $('.crossing_point_name_select').select2({
        theme: 'bootstrap-5'
    });
})

function AddCurrentDate() {
    let currentdate = new Date();
    let comment_object = document.getElementById('comment_for_security');
    let datetime = "";
    if (comment_object.value !== "") {
        datetime = "\n";
    }
    datetime +=
        + currentdate.getDate() + "."
        + (currentdate.getMonth() + 1) + "."
        + currentdate.getFullYear() + " "
        + currentdate.getHours() + ":"
        + currentdate.getMinutes() + ":"
        + currentdate.getSeconds();
    document.getElementById('comment_for_security').value += datetime;
}

jQuery.datetimepicker.setLocale('ru');
jQuery('#date_start').datetimepicker({
    timepicker: false,
    format: 'd.m.Y'
});
jQuery('#date_end').datetimepicker({
    timepicker: false,
    format: 'd.m.Y'
});
jQuery('#date_of_birth').datetimepicker({
    timepicker: false,
    format: 'd.m.Y'
});
