# Development

## Install dependencies

Note: No virtual environments are assumed, but they are suggested.
Run `make init-dev` to install developer dependencies and install
this library in `develop` mode to your active python environment.

## Running

To run the app in development mode from source with your current python environment,
run `make m`.

## Testing

Run test suite to ensure everything works `make test`

## Release

To run tests, publish your plugin to pypi test and prod, sdist and wheels are
registered, created and uploaded with `make release`