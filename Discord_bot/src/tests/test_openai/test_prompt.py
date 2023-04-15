from chatgpt.openai_api import chatgpt_response


def test_chatgpt_response(mocker):
    # Mock the openai.ChatCompletion.create method
    mock_create = mocker.patch("openai.ChatCompletion.create")

    # Define the mocked response
    mock_create.return_value = mocker.Mock(choices=[mocker.Mock(message={"content": "Pass."})])

    # Define the input prompt
    input_prompt = "Does this test pass??"

    # Call the chatgpt_response function
    response = chatgpt_response(input_prompt)

    # Assert that the openai.ChatCompletion.create method was called with the correct parameters
    mock_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_prompt},
        ],
        temperature=1,
        max_tokens=4000,
    )

    # Assert that the response is as expected
    assert response == "Pass."


def test_chatgpt_response_empty_response(mocker):
    # Mock the openai.ChatCompletion.create method
    mock_create = mocker.patch("openai.ChatCompletion.create")
    mock_create.return_value = mocker.Mock(choices=[])
    input_prompt = "Does this test pass?"
    response = chatgpt_response(input_prompt)
    mock_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": input_prompt},
        ],
        temperature=1,
        max_tokens=4000,
    )

    assert response == ""
