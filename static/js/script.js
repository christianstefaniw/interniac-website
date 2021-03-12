ids = {
    studentRadio: 'id_is_student',
    employerRadio: 'id_is_employer',
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

function unhide(id) {
    $(`#${id}`).show()
    $('label[for=' + id + ']').show()
}

function hide(id) {
    $(`#${id}`).hide()
    $('label[for=' + id + ']').hide()
}

$(`#${ids.internWhere}`).change(function () {
    let where = $(this).val().toLowerCase()
    if (where === 'in-person') {
        unhide(ids.location)
    } else {
        hide(ids.location)
    }
})

$(`#${ids.careerType}`).change(function () {
    let career = $(this).val().toLowerCase()
    if (career === '') {
        unhide(ids.newCareer)
    } else {
        hide(ids.newCareer)
    }
})

$(`#${ids.internType}`).change(function () {
    let type = $(this).val().toLowerCase()
    if (type === 'paid') {
        unhide(ids.pay)
    } else {
        hide(ids.pay)
    }
})


$(document).ready(function () {
    let hide = $('form p').children()
    for (let i = 0; i in hide; i++) {
        if (myGetElem($(hide[i]), ids.internType)) {
            continue;
        }
        if (myGetElem($(hide[i]), ids.internWhere)) {
            continue;
        }
        if (myGetElem($(hide[i]), ids.careerType)) {
            continue
        }
        if (myGetElem($(hide[i]), ids.newCareer)) {
            if ($(`#${ids.careerType}`).val() != '') {
                $(`#${ids.newCareer}`).hide()
                $(`label[for=${ids.newCareer}]`).hide()
            }
            continue
        }
        if (myGetElem($(hide[i]), ids.appDeadline)) {
            continue
        }
        if (myGetElem($(hide[i]), ids.timeCommitment)) {
            continue
        }
        if (myGetElem($(hide[i]), ids.description)) {
            continue
        }
        if (myGetElem($(hide[i]), ids.title)) {
            continue
        }
        if (myGetElem($(hide[i]), ids.applicationUrl)) {
            continue
        }
        if (myGetElem($(hide[i]), ids.pay)) {
            $(hide[i]).hide();
            continue;
        }
        if (myGetElem($(hide[i]), ids.location)) {
            $(hide[i]).hide();
            continue;
        }
        $(hide[i]).remove()
    }
})

function myGetElem(el, id) {
    return el.attr('for') === id || el.attr('id') === id;
}

$(function () {
    $("#lnch_btn").on("click", function () {
        setTimeout(function () {
            $("#lnch").addClass("launching").text("SENDING");
            $("#lnch_btn").addClass("launching");
        }, 0);
    });
});

function showFilters() {
    let filters = $('#filters-container');
    let showHideBtn = $('#show-hide-btn')
    if (filters.css('display') === 'none') {
        filters.css('display', 'block');
        showHideBtn.text('Hide Filters').button("refresh");

    } else {
        filters.css('display', 'none')
        showHideBtn.html('Show Filters')
    }
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

$(document).ready(function () {
        hide('company-name');
    }
)

anime({
    targets: '#404-row svg',
    autoplay: true,
    loop: true,
    easing: 'easeInOutSine',
    direction: 'alternate'
});


$(document).ready(function() {
    $('body').tooltip({ selector: '[data-toggle=tooltip]' });
});