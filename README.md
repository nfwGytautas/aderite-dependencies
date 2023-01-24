# Project used to build aderite dependencies

To build all dependencies just pull the repository and run
`git submodule update --init --recursive`
then run 
`python BuildDependencies.py`

## List of dependencies:
### Runtime:
- https://github.com/glfw/glfw  (Used to create windows)
- https://github.com/bkaradzic/bgfx (Used to provide the graphics API)
- https://github.com/NVIDIAGameWorks/PhysX (Physics engine)
- https://github.com/mono/mono (Scripting)
- https://github.com/gabime/spdlog (Logging API)
- https://github.com/g-truc/glm (Math library)
- https://github.com/assimp/assimp (Mesh and object loading)
- https://github.com/nothings/stb (Image loading)
- https://github.com/jbeder/yaml-cpp (Serialization)

### Editor:
- https://github.com/ocornut/imgui (Editor UI)
- https://github.com/Nelarius/imnodes (Graphs)
- https://github.com/samhocevar/portable-file-dialogs (File selection API)
