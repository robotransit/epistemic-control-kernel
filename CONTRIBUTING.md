# Contributing to EBA Core

Thank you for your interest in contributing to **EBA Core**.

EBA Core is an experimental, reliability-focused autonomous agent kernel.  
Contributions are welcome, but the project prioritizes **clarity, safety, and explicit control flow** over feature velocity.

## Project Philosophy

Before contributing, please understand the core design principles:

- Reliability and predictability over cleverness
- Explicit control flow (no hidden side effects)
- Conservative defaults and clear failure modes
- Minimal dependencies
- Framework-agnostic design

Contributions that significantly increase complexity, implicit behaviour, or hidden coupling are unlikely to be accepted.

## What Contributions Are Welcome

- Bug fixes
- Tests (especially unit tests for core seams)
- Documentation improvements
- Small, well-scoped enhancements
- Examples demonstrating safe usage or integrations
- Improvements to error handling, validation, or safeguards

## What Is Likely Out of Scope

- Large architectural rewrites
- Parallel or multi-agent execution models
- Opinionated frameworks or UI layers
- Tool-heavy agents without clear safety boundaries
- Features that bypass prediction, evaluation, or drift checks

If you are unsure whether something fits, please open an issue to discuss it first.

## Development Setup

```
git clone https://github.com/robotransit/eba-core.git
cd eba-core
pip install -e .
```

'Python' 3.10+ is required.

## Testing

We value tests that verify **reliability and safety behaviour**.  
If you add or modify core logic, please include or update tests where appropriate.

Tests are located in the `tests/` directory and can be run with:

```
pytest
```

## Style & Guidelines

- Keep functions small and explicit
- Prefer pure functions where possible
- Avoid global state
- Use clear, descriptive naming
- Add docstrings for public functions
- Do not introduce new dependencies without strong justification

## Issues & Pull Requests

- Open an issue for discussion before submitting major changes
- Keep pull requests focused and scoped
- Clearly explain why a change is needed, not just what it does

All contributions are reviewed with an emphasis on safety, maintainability, and alignment with the project’s goals.

## Code of Conduct

All contributors are expected to follow basic standards of respect and constructive collaboration. For details, see the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) (standard, widely used).

## Acknowledgements

This project has been developed with the assistance of AI-based coding tools.
All design decisions and final implementations are reviewed and owned by the maintainer.
