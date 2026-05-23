# Changelog

## [1.2.0]
- Add correlated subquery detection rule
- Add comprehensive unit tests for all rules
- Fix: missing index rule was flagging column aliases incorrectly

## [1.1.0]
- Add rich terminal output with colour-coded severity
- Add --file flag for analyzing .sql files
- Improve LIKE wildcard rule to only flag leading wildcards

## [1.0.0]
- Initial release
- SELECT *, missing index, function-on-column, leading wildcard rules
- CLI with --query and --file flags