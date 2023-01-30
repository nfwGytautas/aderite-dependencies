# Project used to build aderite dependencies

To build all dependencies just pull the repository and run
`git submodule update --init --recursive`
then run
`python BuildDependencies.py`

## List of dependencies:
### Runtime:
- https://github.com/glfw/glfw  (Used to create windows)
- https://github.com/nfwGytautas/aderite-glad (OpenGL loading)
- https://github.com/gabime/spdlog (Logging API)
