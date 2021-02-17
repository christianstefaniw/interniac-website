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