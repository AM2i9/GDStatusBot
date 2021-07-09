"""
Entrypoint file.
This file is for running the bot, mainly because I can only
package a single file for pyinstaller.
"""

try:
    from gdsb import main
    main()
except Exception as e:
    raise e
finally:
    input("Program stopped. Press RETURN to close")