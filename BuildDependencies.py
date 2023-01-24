import pathlib
from pathlib import Path
import subprocess
import shutil
import os
import glob
import sys

# Shared constants
libDir = "build/lib/x64/"
includeDir = "build/include/"
sourcesDir = "sources/"

# Generate the output folders
print("Generating output directories")
Path(libDir).mkdir(parents=True, exist_ok=True)
Path(includeDir).mkdir(parents=True, exist_ok=True)


# Class to represent a base aderite dependency
class Dependency:
    name = ""
    buildType = ""
    includeFiles = []
    libFiles = []

    def __init__(self, name: str, buildType : str):
        self.name = name
        self.buildType = buildType
        pass

    def build(self):
        if self.buildType == "CMake":
            self.__cmake_build()
            return

        sys.exit("[0] Unspecified build type for {}".format(self.name))

    def __cmake_build(self):
        # TODO: Check that library directory exists
        # TODO: Error check

        print("CMake build for {}".format(self.name))

        lib_dir = "{}{}".format(libDir, self.name)
        build_path = "{}{}/build/".format(sourcesDir, self.name)

        print("Build path:", build_path)
        Path(build_path).mkdir(parents=True, exist_ok=True)

        print("Generating cmake")
        cmake_options = ""
        # if "CmakeOptions" in lib_entry:
        #     cmake_options = lib_entry["CmakeOptions"]

        cmake = subprocess.Popen(["cmake", cmake_options, ".."], cwd=build_path)
        cmake.wait()

        print("Compiling")
        cmake = subprocess.Popen(["make", "-j8"], cwd=build_path)
        cmake.wait()

        # Copy over necessary files
        Path(include_path).mkdir(parents=True, exist_ok=True)

        for lib in self.libFiles:
            shutil.copy("{}{}".format(build_path, lib), libDir)

        for include_file in self.includeFiles:
            if "*" in include_file:
                for file in glob.glob("{}/{}".format(lib_dir, include_file)):
                    if Path(file).is_dir():
                        shutil.copytree(file, include_path + Path(file).stem, dirs_exist_ok=True)
                    else:
                        shutil.copy(file, include_path)
            else:
                shutil.copy("{}/{}".format(lib_dir, include_file), include_path)

# TODO: Check that we are in dependencies folder
# TODO: Check that cmake is installed

# Describe dependencies
glfw = Dependency("glfw", "CMake");
glfw.includeFiles.append("include/GLFW/*")
glfw.libFiles.append("src/libglfw3.a")

dependencies = [glfw]
for i, dependency in enumerate(dependencies):
    print("Building {}/{}".format(i + 1, len(dependencies)))
    dependency.build()

# # Library list
# # ( name, [includes], override for the library file )
# libraries = [
#     {
#         "Name": "pugixml",
#         "IncludeFiles": ["src/pugixml.hpp", "src/pugiconfig.hpp"],
#         "LibFiles": ["libpugixml.a"],
#     },
#     {
#         "Name": "spdlog",
#         "IncludeFiles": ["include/spdlog/**"],
#         "LibFiles": ["libspdlog.a"],
#     },
#     {
#         "Name": "glfw",
#         "IncludeFiles": ["include/GLFW/**"],
#         "LibFiles": ["src/libglfw3.a"],
#     },
#     {
#         "Name": "vex-glad",
#         "IncludeFiles": ["glad/include/**"],
#         "LibFiles": ["libglad.a"],
#         "IncludeOutputOverride": ""
#     },
#     {
#         "Name": "efsw",
#         "IncludeFiles": ["include/**"],
#         "LibFiles": ["libefsw.a"],
#         "IncludeOutputOverride": "",
#         "CmakeOptions": "-DBUILD_SHARED_LIBS=OFF"
#     },
#     {
#         "Name": "glm",
#         "IncludeFiles": ["glm/**"],
#         "LibFiles": ["glm/libglm_static.a"],
#         "IncludeOutputOverride": "glm/",
#     },
# ]
