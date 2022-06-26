# Changelog

All notable changes to this project will be documented in this file. 

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

_Note: 'Unreleased' section below is used for untagged changes that will be issued with the next version bump_

### [Unreleased] - 2022-00-00 
#### Added
#### Changed
#### Deprecated
#### Removed
#### Fixed
#### Security
__BEGIN-CHANGELOG__
 
### [1.0.5] - 2022-06-25
#### Added
 - `gunicorn` to requirements (oof)
 - Darkmode styles to page
 - `/projects` route
 - Actor Inner Join project
#### Changed
 - Bootstrap CSS update
#### Deprecated
#### Removed
#### Fixed
#### Security
 
### [1.0.4] - 2022-06-25
#### Added
 - Better error handlers
 - Logging w/ loguru (via `pukr`)
 - Test binding to gunicorn logger and transmitting levels through that instance to the app
#### Removed
 - Unneeded code in `/koned`
#### Fixed
 - `pyproject.toml` was still building with Python 3.8 whooops
 
### [1.0.3] - 2022-06-17
#### Added
 - SMS support for verification
#### Fixed
 - Add deny message to deny call
 
### [1.0.2] - 2022-06-17
#### Added
 - Flask log
 - Allowlist for incoming calls
 
### [1.0.1] - 2022-06-17
#### Added
 - Twilio receive call support
#### Changed
 - Moved `tests` to outside of project
 - Shift to `pathlib` over `os`
#### Fixed
 - `Flask-SQLAlchemy` wasn't in requirements
 - `tox` called Python 3.8 instead of 3.10
 
### [1.0.0] - 2022-04-20
#### Added
 - CHANGELOG
 - New way of managing package

__END-CHANGELOG__