__all__ = ['request_interview_msg', 'reject_msg', 'accept_msg', 'applied_msg']


def request_interview_msg(company):
    return f'''
Congratulations, you have moved onto the next stage of the recruitment process for {company.employer_profile.company_name}.
{company.employer_profile.company_name} will schedule an interview with you shortly, if you have any questions please email 
{company.email} or reply to this email.

From, the Interniac Team
                            '''


def reject_msg(company, title):
    return f'''
We are sorry to inform you that you have not been selected for the {title} internship from {company}.
If you have any questions for {company}, email them at {company.email} or reply to this message.
Better luck next time.

From, the Interniac Team
                    '''


def accept_msg(company, title):
    return f'''
Congratulations! You have been accepted to the {title} internship from {company}! 
If you have any questions for {company}, email them at {company.email} or reply to this message.
Good luck! 

From, the Interniac Team
                '''

# message sent to employer upon student application


def applied_msg(student_name, title):
    return f'''
        {student_name} has applied for {title}

        From, the Interniac Team
                        '''
