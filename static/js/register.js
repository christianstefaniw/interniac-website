ids = {
    studentRadio: 'id_is_student',
    employerRadio: 'id_is_employer',
}

function checkEmployer() {
    let bool = $(`#${ids.employerRadio}:checked`).val()
    if (bool === 'on') {
        disable(ids.studentRadio)
        unhide('company-name')
    } else {
        undisable(ids.studentRadio)
        hide('company-name')
    }
}


function checkStudent() {
    let bool = $(`#${ids.studentRadio}:checked`).val()
    if (bool === 'on') {
        disable(ids.employerRadio)
    } else {
        undisable(ids.employerRadio)
    }
}

$(`#${ids.employerRadio}`).change(checkEmployer)

$(`#${ids.studentRadio}`).change(checkStudent)


function disable(elId) {
    $(`#${elId}`).attr('disabled', true)
}

function undisable(elId) {
    $(`#${elId}`).attr('disabled', false)
}


function hide(elId) {
    $(`#${elId}`).hide()
}

function unhide(elId) {
    $(`#${elId}`).show()
}
