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
    options = {"shared": [True, False], "with_popt": [True,False], "with_geoip": [True, False], "with_repro": [True, False], "with_tfm": [True, False], "with_mysql": [True, False], "with_ssl": [True, False], "enable_ipv6": [True, False]}
    default_options = "shared=True", "with_popt=False", "with_geoip=False", "with_repro=False", "with_tfm=False", "with_mysql=False", "with_ssl=False", "enable_ipv6=False"
    generators = "cmake"
    exports = "LICENSE"
    release_name = "%s-%s" % (name, version)
    install_dir = tempfile.mkdtemp(suffix=name)

    def source(self):
        tools.get("https://www.resiprocate.org/files/pub/reSIProcate/releases/resiprocate-%s.tar.gz" % self.version)

    def requirements(self):
        if self.options.with_ssl:
            self.requires.add("OpenSSL/1.0.2l@conan/stable")

    def configure(self):
        if self.options.with_tfm:
            self.options.with_repro = True
        if self.options.with_repro:
            self.options.with_popt = True

    def system_requirements(self):
        if self.settings.os == "Linux":
            package_names = []
            if self.options.with_popt:
                package_names.append("libpopt-dev")
            if self.options.with_geoip:
                package_names.append("libgeoip-dev")
            if self.options.with_repro:
                package_names.append("libdb5.3++-dev")
                package_names.append("libcajun-dev")
            if self.options.with_tfm or self.options.with_ssl:
                package_names.append("libboost-system-dev")
            if self.options.with_tfm:
                package_names.append("libcppunit-dev")
                package_names.append("libnetxx-dev")
            if self.options.with_mysql:
                package_names.append("libmysqlclient-dev")
            if self.options.with_ssl:
                package_names.append("libasio-dev")
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
            configure_args.append("--with-repro" if self.options.with_repro else "")
            configure_args.append("--with-tfm" if self.options.with_tfm else "")
            configure_args.append("--with-mysql" if self.options.with_mysql else "")
            configure_args.append("--with-ssl" if self.options.with_ssl else "")
            configure_args.append("--enable-ipv6" if self.options.enable_ipv6 else "")
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
        self.copy(pattern="*", dst="bin", src=os.path.join(self.install_dir, "sbin"), keep_path=False)
        if self.options.shared:
            self.copy(pattern="*.so*", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            self.copy(pattern="*.dylib", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)
            self.copy(pattern="*.la", dst="lib", src=os.path.join(self.install_dir, "lib"), keep_path=False)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.cpp_info.libs = ["resip", "rutil", "dum", "resipares"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
            if self.options.with_popt:
                self.cpp_info.libs.append("popt")
            if self.options.with_geoip:
                self.cpp_info.libs.append("GeoIP")
            if self.options.with_mysql:
                self.cpp_info.libs.append("mysqlclient")
            if self.options.with_repro:
                self.cpp_info.libs.append("db")
                self.cpp_info.libs.append("repro")
            if self.options.with_ssl or self.options.with_tfm:
                self.cpp_info.libs.append("boost_system")
            if self.options.with_tfm:
                self.cpp_info.libs.append("tfm")
                self.cpp_info.libs.append("tfmrepro")
                self.cpp_info.libs.append("cppunit")
                self.cpp_info.libs.append("Netxx")
            if self.options.with_ssl:
                self.cpp_info.libs.append("reTurnClient")
