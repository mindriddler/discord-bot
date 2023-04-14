from chatgpt.openai_api import chatgpt_response


def test_chatgpt_response(mocker):
    # Mock the openai.ChatCompletion.create method
    mock_create = mocker.patch("openai.ChatCompletion.create")

    # Define the mocked response
    mock_create.return_value = mocker.Mock(choices=[mocker.Mock(message={"content": "This is a test response."})])

    # Define the input prompt
    input_prompt = "What is the meaning of life?"

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
    assert response == "This is a test response."


def test_chatgpt_response_empty_response(mocker):
    # Mock the openai.ChatCompletion.create method
    mock_create = mocker.patch("openai.ChatCompletion.create")

    # Define the mocked response with an empty list of choices
    mock_create.return_value = mocker.Mock(choices=[])

    # Define the input prompt
    input_prompt = "What is the meaning of life?"

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

    # Assert that the response is empty
    assert response == ""
