ids={
    location: 'id_location',
    internWhere: 'id_where',
    careerType: 'id_career',
    newCareer: 'id_new_career',
    internType: 'id_type',
    pay: 'id_pay',
    timeCommitment: 'id_time_commitment',
    appDeadline: 'id_application_deadline',
    description: 'id_description',
    title: 'id_title',
    applicationUrl: 'id_application_url'
}


function unhide (id){
    $(`#${id}`).show()
    $('label[for='+id+']').show()
}

function hide (id){
    $(`#${id}`).hide()
    $('label[for='+id+']').hide()
}

$(`#${ids.internWhere}`).change(function (){
    let where = $(this).val().toLowerCase()
    if (where === 'in-person'){
        unhide(ids.location)
    } else {
        hide(ids.location)
    }
})

$(`#${ids.careerType}`).change(function (){
    let career = $(this).val().toLowerCase()
    if (career === ''){
        unhide(ids.newCareer)
    } else {
        hide(ids.newCareer)
    }
})

$(`#${ids.internType}`).change(function (){
    let type = $(this).val().toLowerCase()
    if (type === 'paid'){
        unhide(ids.pay)
    } else {
        hide(ids.pay)
    }
})


$(document).ready(function () {
    let hide = $('form p').children()
    for (let i = 0; i in hide; i++){
        if (myGetElem($(hide[i]), ids.internType)){continue;}
        if (myGetElem($(hide[i]), ids.internWhere)){continue;}
        if (myGetElem($(hide[i]), ids.careerType)){continue}
        if (myGetElem($(hide[i]), ids.newCareer)){
            if ($(`#${ids.careerType}`).val() != ''){
                $(`#${ids.newCareer}`).hide()
                $(`label[for=${ids.newCareer}]`).hide()
            }
            continue
        }
        if (myGetElem($(hide[i]), ids.appDeadline)){continue}
        if (myGetElem($(hide[i]), ids.timeCommitment)){continue}
        if (myGetElem($(hide[i]), ids.description)){continue}
        if (myGetElem($(hide[i]), ids.title)){continue}
        if (myGetElem($(hide[i]), ids.applicationUrl)){continue}
        if (myGetElem($(hide[i]), ids.pay)){$(hide[i]).hide(); continue;}
        if (myGetElem($(hide[i]), ids.location)){$(hide[i]).hide(); continue;}
        $(hide[i]).remove()
    }
})

function myGetElem(el, id){
    return el.attr('for') === id || el.attr('id') === id;
}