# Contributing to ChatGPT-Discord-Bot

First off, thank you for considering contributing to ChatGPT-Discord-Bot! Your help and contributions are greatly appreciated.

The following guidelines will help you get started and ensure a smooth contribution process. Please read them carefully before contributing.

## Table of Contents

- [Contributing to ChatGPT-Discord-Bot](#contributing-to-chatgpt-discord-bot)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [How to Contribute](#how-to-contribute)
    - [Reporting Bugs](#reporting-bugs)
    - [Suggesting Enhancements](#suggesting-enhancements)
    - [Code Contributions](#code-contributions)
      - [Pull Requests](#pull-requests)
    - [Running with Docker](#running-with-docker)
      - [Building Your Own Image](#building-your-own-image)
      - [Use pre-built Docker Image](#use-pre-built-docker-image)
  - [Styleguides](#styleguides)
    - [Git Commit Messages](#git-commit-messages)
    - [Python Styleguide](#python-styleguide)
    - [Documentation Styleguide](#documentation-styleguide)
  - [Conclusion](#conclusion)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How to Contribute

### Reporting Bugs

If you find a bug or issue, please report it by [creating a new issue](https://github.com/mindriddler/chatgpt-discord-bot/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5BBUG%5D). Be sure to follow the bug report template and provide as much information as possible.

### Suggesting Enhancements

If you have an idea for a new feature or enhancement, please [create a new issue](https://github.com/mindriddler/chatgpt-discord-bot/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=%5BFeature%5D) to discuss it. Be sure to follow the feature request template and provide a clear and concise description of your suggestion.

### Code Contributions

To contribute code, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your fork of the repository locally.
3. Create a new branch for your changes (`git checkout -b feature/my-new-feature`).
4. Make your changes in the new branch.
5. Test your changes locally and ensure they are working correctly.
6. Commit your changes, following the [Git Commit Messages](#git-commit-messages) styleguide.
7. Push your branch to your fork on GitHub (`git push origin feature/my-new-feature`).
8. [Create a new pull request](https://github.com/mindriddler/chatgpt-discord-bot/compare) from your fork to the main repository.

#### Pull Requests

- Please ensure your pull request adheres to the [Python Styleguide](#python-styleguide) and [Documentation Styleguide](#documentation-styleguide).
- Make sure your pull request is based on the latest version of the `main` branch.
- Describe your changes clearly in the pull request description.
- Include relevant issue numbers in your pull request description, if applicable.
- Once submitted, a maintainer will review your pull request and provide feedback. Please be patient and address any requested changes.

### Running with Docker

If you want to run ChatGPT-Discord-Bot in a container, you need to provide the necessary API keys as environment variables. You can either build your own image or pull the pre-built images from GitHub Container Registry (GHCR).

#### Building Your Own Image

When building the Docker image, pass the required keys as build arguments. For example:

```bash
docker build --build-arg GITHUB_ACTION=true \
             --build-arg DISCORD_TOKEN=<your_discord_token> \
             --build-arg OPENAI_API_KEY=<your_openai_api_key> \
             --file ./Docker/Dockerfile \
             --tag <your_image_tag> .
```
#### Use pre-built Docker Image 
```bash
docker pull ghcr.io/mindriddler/chatgpt-discord-bot:<image_tag>
```
```bash
docker run -d --name chatgpt-discord-bot \
           -e DISCORD_TOKEN=<your_discord_token> \
           -e OPENAI_API_KEY=<your_openai_api_key> \
           <your_image_tag>
```
## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line
- When only changing documentation, include `[ci skip]` in the commit title

### Python Styleguide

- All Python code must adhere to the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008)
- Use 4 spaces for indentation.
- Use snake_case for function and variable names.
- Use CamelCase for class names.
- Keep lines to a maximum of 79 characters.
- Add comments and docstrings to explain your code where necessary.
- Write clean, concise, and efficient code, making use of Python's built-in functions and libraries when appropriate.
- Use type hints to help with readability and understanding of the code.
- Handle exceptions appropriately and provide useful error messages.
- Organize your imports at the beginning of the file, and follow the order: standard library imports, third-party imports, and local application imports.

### Documentation Styleguide

- Write clear and concise documentation that is easy to understand.
- Use [Markdown](https://guides.github.com/features/mastering-markdown/) for formatting.
- Organize your documentation into sections and subsections using headers.
- Use code blocks to show examples or command-line instructions.
- When documenting code, use inline code formatting for variable names, function names, and other code-related elements.
- Proofread your documentation for grammar and spelling errors.
- Keep your documentation up-to-date as the codebase evolves.

## Conclusion

We appreciate your interest in contributing to ChatGPT-Discord-Bot and look forward to working with you. By following these guidelines, you'll help ensure a smooth and efficient contribution process. If you have any questions or concerns, please don't hesitate to reach out to the maintainers or open an issue. Happy coding!
