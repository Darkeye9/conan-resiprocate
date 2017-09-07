import copy
from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="resiprocate:shared")
    extra_builds = copy.deepcopy(builder.builds)
    for settings, options, env_vars, build_requires in extra_builds:
        options["resiprocate:with_popt"] = True
        options["resiprocate:with_geoip"] = True
        options["resiprocate:with_repro"] = True
        options["resiprocate:with_tfm"] = True
        options["resiprocate:with_mysql"] = True
        options["resiprocate:with_ssl"] = True
        options["resiprocate:enable_ipv6"] = True
    builder.builds.extend(extra_builds)
    builder.run()
