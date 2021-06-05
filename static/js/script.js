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
        unhideInputAndLabel(ids.location)
    } else {
        hideInputAndLabel(ids.location)
    }
})

$(`#${ids.careerType}`).change(function () {
    let career = $(this).val().toLowerCase()
    if (career === '') {
        unhideInputAndLabel(ids.newCareer)
    } else {
        hideInputAndLabel(ids.newCareer)
    }
})

$(`#${ids.internType}`).change(function () {
    let type = $(this).val().toLowerCase()
    if (type === 'paid') {
        unhideInputAndLabel(ids.pay)
    } else {
        hideInputAndLabel(ids.pay)
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
    if (state === 'employer') {
        unhide(ids.companyName)
    } else {
        hide(ids.companyName)
    }
})

$(function () {
    if ($('body').hasClass('hide-inputs')) {
        let hide = $('form p').children()
        for (let i = 0; i in hide; i++) {

            if (myGetElem($(hide[i]), ids.newCareer)) {
                if ($(`#${ids.careerType}`).val() !== '') {
                    $(`#${ids.newCareer}`).hide()
                    $(`label[for=${ids.newCareer}]`).hide()
                }
                continue
            }

            if (myGetElem($(hide[i]), ids.pay)) {
                if ($(`#${ids.internType}`).val() !== 'Paid') {
                    $(hide[i]).hide();
                }
                continue;
            }

            if (myGetElem($(hide[i]), ids.location)) {
                if ($(`#${ids.internWhere}`).val() !== 'In-Person') {
                    $(hide[i]).hide();
                }
                continue;
            }
        }
    }
});

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
    if (elId === ids.companyName) {
        el.addClass('mb-5')
    }
    el.show()
}

function unhideInputAndLabel(elId) {
    let el = $(`#${elId}`)
    let label = $(`label[for=${elId}]`)
    el.show()
    label.show()
}

function hideInputAndLabel(elId) {
    let el = $(`#${elId}`)
    let label = $(`label[for=${elId}]`)
    el.hide()
    label.hide()
}


$(document).ready(function () {
    $('body').tooltip({ selector: '[data-toggle=tooltip]' });
    $('input[type=url]').each(function (_, el) { $(el).tooltip({ 'trigger': 'focus', 'title': 'Must start with "http"' }) });
});