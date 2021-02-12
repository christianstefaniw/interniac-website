ids={
    name: 'id_org_name',
    website: 'id_org_website',
    studentRadio: 'id_is_student',
    employerRadio: 'id_is_employer',
}


function unhide (id){
    $(`#${id}`).show()
    $('label[for='+id+']').show()
}

function hide (id){
    $(`#${id}`).hide()
    $('label[for='+id+']').hide()
}

$(`#${ids.employerRadio}`).change(function (){
    let bool = $(`#${ids.employerRadio}:checked`).val()
    console.log(bool)
    if (bool === 'on'){
        disable(ids.studentRadio)
        unHideAll()
    } else {
        undisable(ids.studentRadio)
        hideAll()
    }
})

$(`#${ids.studentRadio}`).change(function (){
    let bool = $(`#${ids.studentRadio}:checked`).val()
    if (bool === 'on'){
        disable(ids.employerRadio)
        hideAll()
    } else {
        undisable(ids.employerRadio)
    }
})

function hideAll() {
    hide(ids.website)
    hide(ids.name)
}

function unHideAll() {
    unhide(ids.website)
    unhide(ids.name)
}

function disable(elId){
    $(`#${elId}`).attr('disabled', true)
}

function undisable(elId){
    $(`#${elId}`).attr('disabled', false)
}

$(document).ready(function () {
    hideAll()
})