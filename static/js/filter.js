ids = {
    type: 'id_type',
    where: 'id_where',
    career: 'id_career',
    filtersForm: 'filters'
}

function filter(){
    const type = $(`#${ids.type}`).val()
    const where = $(`#${ids.where}`).val()
    const career = $(`#${ids.career}`).val()
    console.log(type)
    $.ajax({
        type: 'GET',
        url:`/marketplace/filter/?type=${type}&where=${where}&career=${career}`,
        success: function (data) {
            $('#listings').html(data)
        }
    })
}
