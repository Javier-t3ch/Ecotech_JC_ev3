import os
import sys
from getpass import getpass


def _capturar_caracteres(mensaje, leer_caracter):
    caracteres = []
    sys.stdout.write(mensaje)
    sys.stdout.flush()
    while True:
        caracter = leer_caracter()
        if caracter == "":
            sys.stdout.write("\n")
            sys.stdout.flush()
            raise EOFError
        if caracter in ("\r", "\n"):
            sys.stdout.write("\n")
            sys.stdout.flush()
            return "".join(caracteres)
        if caracter in ("\x03",):
            sys.stdout.write("\n")
            sys.stdout.flush()
            raise KeyboardInterrupt
        if caracter in ("\x04", "\x1a"):
            sys.stdout.write("\n")
            sys.stdout.flush()
            raise EOFError
        if caracter in ("\b", "\x7f"):
            if caracteres:
                caracteres.pop()
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue
        if caracter and caracter.isprintable():
            caracteres.append(caracter)
            sys.stdout.write("*")
            sys.stdout.flush()


def _leer_windows(mensaje):
    import msvcrt

    def leer_caracter():
        while True:
            caracter = msvcrt.getwch()
            if caracter in ("\x00", "\xe0"):
                msvcrt.getwch()
                continue
            return caracter

    return _capturar_caracteres(mensaje, leer_caracter)


def _leer_unix(mensaje):
    import termios
    import tty

    descriptor = sys.stdin.fileno()
    estado = termios.tcgetattr(descriptor)
    try:
        tty.setraw(descriptor)
        return _capturar_caracteres(mensaje, lambda: sys.stdin.read(1))
    finally:
        termios.tcsetattr(descriptor, termios.TCSADRAIN, estado)


def leer_con_asteriscos(mensaje):
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return getpass(mensaje)
    if os.name == "nt":
        return _leer_windows(mensaje)
    return _leer_unix(mensaje)
