import allure
from hw_12.pages.registration_page import RegistrationFormPage


@allure.title("Successful fill form")
def test_student_registration_form():
    with allure.step("Open registration form"):
        registration_page = RegistrationFormPage()

    with allure.step("Fill form"):
        registration_page.open()
        (
            registration_page
            .fill_first_name('Masha')
            .fill_last_name('Www')
            .fill_user_email('test@gmail.com')
            .fill_gender('Female')
            .fill_user_number('1234456789')
            .fill_day_of_birth('1999', 'May', '11')
            .fill_subject('Maths')
            .fill_hobbies('Sports')
            .fill_picture('picture.jpg')
            .fill_current_address('Quitzon Common, South Kraigville')
            .fill_state('NCR')
            .fill_city('Delhi')
            .click_submit()
        )

    with allure.step("Check form results"):
        registration_page.should_have_registered('Masha Www', 'test@gmail.com', 'Female', '1234456789', '11 May,1999',
                                                 'Maths', 'Sports', 'picture.jpg',
                                                 'Quitzon Common, South Kraigville', 'NCR Delhi')
