import os

from helpers.email import send_email, send_email_thread


"""
Helper classes for sending emails after certian actions for the applications app
Currently we support the following 6 helper classes:

1. **`RequestInterview`** - implements helper methods for emailing an applicant about an interview request
2. **`RejectStudent`** - implements helper methods for emailing an applicant about a rejection
3. **`AcceptStudent`** - implements helper methods for emailing an applicant about an acceptance
4. **`ConfirmAcceptance`** - implements helper methods for emailing an employer about a confrimed acceptance
5. **`DeclineAcceptance`** - implements helper methods for emailing an employer about a declined acceptance
6. **`Applied`** - implements helper methods for emailing an employer about a new application
"""


class RequestInterview:

    @staticmethod
    def request_interview_msg(company, title) -> str:
        return f'''
Congratulations, you have moved onto the next stage of the recruitment process for {title}.
{company.employer_profile.company_name} will schedule an interview with you shortly, if you have any questions please email 
{company.email} or reply to this email.

From, the Interniac Team
                                '''

    @staticmethod
    def request_interview_email(student, listing) -> None:
        email = student.email
        message = RequestInterview.request_interview_msg(
            listing.company, listing.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[email], subject=f"Next steps for {listing.title}",
                   reply_to=[listing.company.email])


class RejectStudent:

    @staticmethod
    def reject_student_msg(company, title) -> str:
        return f'''
We are sorry to inform you that you have not been selected for the {title} internship from {company}.
If you have any questions for {company}, email them at {company.email} or reply to this message.
Check out other internship opprotunities on our website!

From, the Interniac Team
                        '''

    @staticmethod
    def reject_student_email(student, listing):
        email = student.email

        message = RejectStudent.reject_student_msg(
            listing.company, listing.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[email], subject=f"Response for {listing.title}",
                   reply_to=[listing.company.email])


class AcceptStudent:
    @staticmethod
    def accept_student_msg(company, title) -> str:
        return f'''
Congratulations! You have been accepted to the {title} internship from {company}! 
If you have any questions for {company}, email them at {company.email} or reply to this message. Please confirm that you still want this internship on the Interniac website.
Good luck! 

From, the Interniac Team
                    '''

    @staticmethod
    def accept_student_email(student, listing):
        message = AcceptStudent.accept_student_msg(
            listing.company, listing.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[
                       student.email], subject=f"Congratulations! ({listing.title})",
                   reply_to=[listing.company.email])


class ConfirmAcceptance:

    @staticmethod
    def confirmed_message(student_name, title) -> str:
        return f'''
{student_name} has accepted your offer for the {title} internship!

From, the Interniac Team
        '''

    @staticmethod
    def confirmed_acceptance_email(student, listing):
        message = ConfirmAcceptance.confirmed_message(
            f'{student.first_name} {student.last_name}', listing.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[listing.company.email], subject=f"Student Confirmed!",
                   reply_to=[student.email]
                   )


class DeclineAcceptance:

    @staticmethod
    def declined_message(student_name, title) -> str:
        return f'''
{student_name} has declined your offer for the {title} internship.

From, the Interniac Team
        '''

    @staticmethod
    def declined_acceptance_email(student, listing):
        message = DeclineAcceptance.declined_message(
            f'{student.first_name} {student.last_name}', listing.title)

        send_email(body=message, from_email=os.environ.get("EMAIL"),
                   to=[listing.company.email], subject=f"Student Declined",
                   reply_to=[student.email]
                   )


class Applied:

    @staticmethod
    def applied_msg(student_name, title) -> str:
        return f'''
{student_name} has applied for {title}
From, the Interniac Team
                        '''

    @staticmethod
    def applied_email(student, listing):
        name = f'{student.first_name} {student.last_name}'
        message = Applied.applied_msg(name, listing.title)

        send_email_thread(body=message, from_email=os.environ.get("EMAIL"), to=[listing.company.email],
                          subject=f"New Application ({listing.title})",
                          reply_to=[os.environ.get("EMAIL")])
