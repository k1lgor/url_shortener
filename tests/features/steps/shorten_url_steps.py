from behave import given, when, then
from playwright.sync_api import expect


@when('I visit the URL shortener page')
@given('I am on the URL shortener page')
def step_impl(context):
    context.page.goto('http://localhost:5000')


@then('I should see the URL input form')
def step_impl(context):
    form = context.page.locator('form')
    expect(form).to_be_visible()


@when('I enter "{url}" into the URL input')
def step_impl(context, url):
    context.page.fill('input[name="url"]', url)


@when('I submit the form')
def step_impl(context):
    context.page.click('button[type="submit"]')


@then('I should see a result')
def step_impl(context):
    result = context.page.locator('#result')
    expect(result).to_be_visible()
    expect(result).not_to_be_empty()


@then('I should see a validation message')
def step_impl(context):
    input_element = context.page.locator('input[name="url"]')

    # Force the input to lose focus to trigger validation
    context.page.press('input[name="url"]', 'Tab')

    # Check if the input is invalid
    is_invalid = input_element.evaluate('(el) => !el.checkValidity()')
    assert is_invalid, "Expected input to be invalid"

    # Get the validation message
    validation_message = input_element.evaluate('(el) => el.validationMessage')
    print(f"Validation message: {validation_message}")

    assert validation_message, "Expected a non-empty validation message"
