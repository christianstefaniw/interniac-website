def paginate(context):
    """
    This function returns the number of pages should be displayed in the paginated menu

    @param context: the information being passed to the html page
    @type context: `dict`
    """
    paginator = context.get('paginator')
    num_pages = paginator.num_pages
    current_page = context.get('page_obj')
    page_no = current_page.number

    if num_pages <= 15 or page_no <= 6:
        pages = [x for x in range(1, min(num_pages + 1, 16))]
    elif page_no > num_pages - 6:
        pages = [x for x in range(num_pages - 14, num_pages + 1)]
    else:
        pages = [x for x in range(page_no - 5, page_no + 6)]

    return pages
