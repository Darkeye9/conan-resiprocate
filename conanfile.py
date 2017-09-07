import tempfile
import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class ResiprocateConan(ConanFile):
    name = "resiprocate"
    version = "1.10.2"
    license = "https://github.com/resiprocate/resiprocate/blob/master/COPYING"
    url = "https://github.com/uilianries/conan-resiprocate"
    author = "Uilian Ries <uilianries@gmail.com>"
    description = "C++ implementation of SIP, ICE, TURN and related protocols"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "with_popt": [True,False], "with_geoip": [True, False]}
    default_options = "shared=True", "with_popt=False", "with_geoip=False"
    generators = "cmake"
    exports = "LICENSE"
    release_name = "%s-%s" % (name, version)
    install_dir = tempfile.mkdtemp(suffix=name)

    def source(self):
        tools.get("https://www.resiprocate.org/files/pub/reSIProcate/releases/resiprocate-%s.tar.gz" % self.version)

    def config_options(self):
        if self.settings.os != "Linux":
            del self.options.with_popt
            del self.options.with_geoip

    def system_requirements(self):
        if self.settings.os == "Linux":
            package_names = []
            if self.options.with_popt:
                package_names.append("libpopt-dev")
            if self.options.with_geoip:
                package_names.append("libgeoip-dev")
            if package_names:
                package_manager = tools.SystemPackageTool()
                package_manager.install(packages=' '.join(package_names))

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.fpic = True
        env_build.cxx_flags.append("-w")
        with tools.environment_append(env_build.vars):
            configure_args = ['--prefix=%s' % self.install_dir]
            configure_args.append("--with-popt" if self.options.with_popt else "")
            configure_args.append("--with-geoip" if self.options.with_geoip else "")
            configure_args.append("--enable-silent-rules")
            with tools.chdir(self.release_name):
                env_build.configure(args=configure_args)
                env_build.make(args=["--quiet", "all"])
                if self.scope.dev == True:
                    env_build.make(args=["--quiet", "check"])
                env_build.make(args=["install"])

    def package(self):
        self.copy("LICENSE", src=self.release_name, dst=".", keep_path=False)
        self.copy(pattern="*", dst="include", src=os.path.join(self.install_dir, "include"))
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            self.copy(pattern="*.la", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["resip", "rutil", "dum", "resipares"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
