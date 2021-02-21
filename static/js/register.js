ids={
    studentRadio: 'id_is_student',
    employerRadio: 'id_is_employer',
}


$(`#${ids.employerRadio}`).change(function (){
    let bool = $(`#${ids.employerRadio}:checked`).val()
    if (bool === 'on'){
        disable(ids.studentRadio)
        unhide('company-name')
    } else {
        undisable(ids.studentRadio)
        hide('company-name')
    }
})

$(`#${ids.studentRadio}`).change(function (){
    let bool = $(`#${ids.studentRadio}:checked`).val()
    if (bool === 'on'){
        disable(ids.employerRadio)
    } else {
        undisable(ids.employerRadio)
    }
})


function disable(elId){
    $(`#${elId}`).attr('disabled', true)
}

function undisable(elId){
    $(`#${elId}`).attr('disabled', false)
}


function hide(elId){
    $(`#${elId}`).hide()
}

function unhide(elId){
    $(`#${elId}`).show()
}