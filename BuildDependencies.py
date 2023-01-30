import pathlib
from pathlib import Path
import subprocess
import shutil
import os
import glob
import sys

# Config
makeCommand = "mingw32-make"
cCompiler = "gcc"

# Shared constants
outDir = "build/dependencies/"
libDir = "{}lib/".format(outDir)
includeDir = "{}include/".format(outDir)
sourcesDir = "sources/"

# Generate the output folders
print("Generating output directories")
Path(libDir).mkdir(parents=True, exist_ok=True)
Path(includeDir).mkdir(parents=True, exist_ok=True)

# TODO: Check that library directory exists
# TODO: Error check

# Class to represent a base aderite dependency
class Dependency:
    def __init__(self, name: str, buildType : str):
        self.name = name
        self.buildType = buildType
        self.includeFiles = []
        self.libFiles = []
        self.cmakeOptions = []

        self.libDir = "{}{}".format(libDir, self.name)
        self.buildPath = "{}{}/build/".format(sourcesDir, self.name)
        self.includePath = "{}include/{}".format(outDir, self.name)


    # Override the default output directory(dependency name) for dependency
    def override_include_directory(self, override) :
        self.includePath = "{}include/{}".format(outDir, override)


    # Prepare directories for building
    def prepare_directories(self):
        if Path(self.buildPath).exists():
            shutil.rmtree(self.buildPath, ignore_errors=False, onerror=None)

        Path(self.buildPath).mkdir(parents=True, exist_ok=True)
        Path(self.includePath).mkdir(parents=True, exist_ok=True)


    # Generate files for building
    def generate(self):
        if self.buildType == "CMake":
            print("Generating cmake for {}".format(self.name))

            cmake_options = ["cmake"]
            cmake_options.append("-DCMAKE_C_COMPILER={}".format(cCompiler))
            cmake_options.append("-DCMAKE_MAKE_PROGRAM={}".format(makeCommand))
            cmake_options.append("-G Unix Makefiles")
            cmake_options = cmake_options + self.cmakeOptions
            cmake_options.append("..") # In build directory generate from root

            cmake = subprocess.Popen(cmake_options, cwd=self.buildPath)
            cmake.wait()
            return

        sys.exit("[0] Unspecified build type for {}".format(self.name))


    # Build the dependency
    def build(self):
        if self.buildType == "CMake":
            print("Compiling", self.name)
            make = subprocess.Popen([makeCommand, "-j8"], cwd=self.buildPath)
            make.wait()
            return

        sys.exit("[0] Unspecified build type for {}".format(self.name))


    # Copy dependency outputs
    def copy_outputs(self):
        print("Copying outputs for", self.name)
        for lib in self.libFiles:
            shutil.copy("{}{}".format(self.buildPath, lib), libDir)

        for include_file in self.includeFiles:
            if "*" in include_file:
                for file in glob.glob("{}{}/{}".format(sourcesDir, self.name, include_file)):
                    if Path(file).is_dir():
                        shutil.copytree(file, self.includePath + Path(file).stem, dirs_exist_ok=True)
                    else:
                        shutil.copy(file, self.includePath )
            else:
                shutil.copy("{}/{}".format(self.libDir, include_file), self.includePath)


# TODO: Check that we are in dependencies folder
# TODO: Check that cmake is installed
# TODO: Check outputs for errors

# Describe dependencies
glfw = Dependency("glfw", "CMake")
glfw.includeFiles.append("include/GLFW/**")
glfw.libFiles.append("src/libglfw3.a")

glad = Dependency("glad", "CMake")
glad.includeFiles.append("debug/include/**")
glad.override_include_directory("")
glad.libFiles.append("libglad_debug.a")

spdlog = Dependency("spdlog", "CMake")
spdlog.includeFiles.append("include/**")
spdlog.override_include_directory("")
spdlog.cmakeOptions.append("-DSPDLOG_BUILD_EXAMPLE=OFF")
spdlog.libFiles.append("libspdlog.a")

dependencies = [glfw, glad, spdlog]
for i, dependency in enumerate(dependencies):
    print("Building {}/{}".format(i + 1, len(dependencies)))
    dependency.prepare_directories()
    dependency.generate()
    dependency.build()
    dependency.copy_outputs()
