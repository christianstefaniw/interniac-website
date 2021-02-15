ids={
    studentRadio: 'id_is_student',
    employerRadio: 'id_is_employer',
}


$(`#${ids.employerRadio}`).change(function (){
    let bool = $(`#${ids.employerRadio}:checked`).val()
    console.log(bool)
    if (bool === 'on'){
        disable(ids.studentRadio)
    } else {
        undisable(ids.studentRadio)
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
