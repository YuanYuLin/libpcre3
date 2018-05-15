import ops
import iopc

pkg_path = ""
output_dir = ""
arch = ""
src_lib_dir = ""
src_usr_lib_dir = ""
dst_lib_dir = ""
src_include_dir = ""
dst_include_dir = ""
tmp_include_dir = ""
src_pkgconfig_dir = ""
dst_pkgconfig_dir = ""
install_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global arch
    global src_lib_dir
    global dst_lib_dir
    global src_usr_lib_dir
    global src_include_dir
    global dst_include_dir
    global tmp_include_dir
    global src_pkgconfig_dir
    global dst_pkgconfig_dir
    global install_dir
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    if arch == "armhf":
        src_lib_dir = iopc.getBaseRootFile("lib/arm-linux-gnueabihf")
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/arm-linux-gnueabihf")
    elif arch == "armel":
        src_lib_dir = iopc.getBaseRootFile("lib/arm-linux-gnueabi")
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/arm-linux-gnueabi")
    elif arch == "x86_64":
        src_lib_dir = iopc.getBaseRootFile("lib/x86_64-linux-gnu")
        src_usr_lib_dir = iopc.getBaseRootFile("usr/lib/x86_64-linux-gnu")
    else:
        sys.exit(1)
    dst_lib_dir = ops.path_join(output_dir, "lib")
    install_dir = ops.path_join(output_dir, "pkgconfig")

    src_include_dir = iopc.getBaseRootFile("/usr/include")
    dst_include_dir = ops.path_join("include",args["pkg_name"])
    tmp_include_dir = ops.path_join(output_dir, ops.path_join("include",args["pkg_name"]))

    src_pkgconfig_dir = ops.path_join(pkg_path, "pkgconfig")
    dst_pkgconfig_dir = ops.path_join(install_dir, "pkgconfig")

def MAIN_ENV(args):
    set_global(args)
    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.mkdir(dst_lib_dir)
    ops.copyto(ops.path_join(src_lib_dir, "libpcre.so.3.13.3"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libpcre.so.3.13.3", "libpcre.so.3.13")
    ops.ln(dst_lib_dir, "libpcre.so.3.13.3", "libpcre.so.3")
    ops.ln(dst_lib_dir, "libpcre.so.3.13.3", "libpcre.so")

    ops.mkdir(dst_lib_dir)
    ops.copyto(ops.path_join(src_usr_lib_dir, "libpcreposix.so.3.13.3"), dst_lib_dir)
    ops.ln(dst_lib_dir, "libpcreposix.so.3.13.3", "libpcreposix.so.3.13")
    ops.ln(dst_lib_dir, "libpcreposix.so.3.13.3", "libpcreposix.so.3")
    ops.ln(dst_lib_dir, "libpcreposix.so.3.13.3", "libpcreposix.so")

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(build_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)
    return False

def MAIN_BUILD(args):
    set_global(args)

    ops.mkdir(tmp_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pcre.h"), tmp_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pcre_scanner.h"), tmp_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pcre_stringpiece.h"), tmp_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pcrecpp.h"), tmp_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pcrecpparg.h"), tmp_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(src_include_dir, "pcreposix.h"), tmp_include_dir)

    ops.mkdir(dst_pkgconfig_dir)
    ops.copyto(ops.path_join(src_pkgconfig_dir, '.'), dst_pkgconfig_dir)

    return False

def MAIN_INSTALL(args):
    set_global(args)

    iopc.installBin(args["pkg_name"], ops.path_join(dst_lib_dir, "."), "lib") 
    iopc.installBin(args["pkg_name"], ops.path_join(tmp_include_dir, "."), dst_include_dir)
    iopc.installBin(args["pkg_name"], ops.path_join(dst_pkgconfig_dir, '.'), "pkgconfig")

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)
    return False

def MAIN(args):
    set_global(args)

