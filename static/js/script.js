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
    applicationUrl: 'id_application_url',
    companyName: 'company-name',
    isStudent: 'id_student_employer_0',
    isEmployer: 'id_student_employer_1'
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

$(`#${ids.isStudent}`).change(function () {
    let state = $(this).val().toLowerCase()
    if (state === 'student') {
        hide(ids.companyName)
    } else {
        unhide(ids.companyName)
    }
})

$(`#${ids.isEmployer}`).change(function () {
    let state = $(this).val().toLowerCase()
    console.log(state)
    if (state === 'employer') {
        unhide(ids.companyName)
    } else {
        hide(ids.companyName)
    }
})

if (document.URL === 'http://127.0.0.1:8000/marketplace/createlisting/') {
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
            if ($(`#${ids.careerType}`).val() !== '') {
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
}

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


function disable(elId) {
    $(`#${elId}`).attr('disabled', true)
}

function undisable(elId) {
    $(`#${elId}`).attr('disabled', false)
}


function hide(elId) {
    let el = $(`#${elId}`)
    el.hide()
}

function unhide(elId) {
    let el = $(`#${elId}`)
    if (elId === ids.companyName){
        el.addClass('mb-5')
    }
    el.show()
}


anime({
    targets: '#404-row svg',
    autoplay: true,
    loop: true,
    easing: 'easeInOutSine',
    direction: 'alternate'
});


$(document).ready(function () {
    $('body').tooltip({selector: '[data-toggle=tooltip]'});
});