import sys
from baserunner import Runner, main


if __name__ == '__main__':
    import platform
    platform_sys = platform.system()
    Runner.info(f'platform.system() is {platform_sys}')
    if platform_sys=='Linux':
        from linuxrunner import LinuxRunner
        main(LinuxRunner)
    elif platform_sys=='Darwin':
        from macrunner import MacRunner
        main(MacRunner)
    elif platform_sys=='Windows':
        from winrunner import WinRunner
        main(WinRunner)
    else:
        Runner.err(f'ERROR: No runner implementation for platform "{platform_sys}"')
        sys.exit(1)
