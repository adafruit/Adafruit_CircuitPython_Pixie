Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-pixie/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/pixie/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_Pixie/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_Pixie/actions/
    :alt: Build Status

.. A driver for Pixie - 3W Chainable Smart LED Pixel

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-pixie/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-pixie

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-pixie

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-pixie

Usage Example
=============

.. code-block::python

    import time
    import board
    import adafruit_pixie
    import busio

    uart = busio.UART(board.TX, rx=None, baudrate=115200)

    num_pixies = 2  # Change this to the number of Pixies LEDs you have.
    pixies = adafruit_pixie.Pixie(uart, num_pixies, brightness=0.2, auto_write=False)


    def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return 0, 0, 0
    if pos < 85:
        return int(255 - pos * 3), int(pos * 3), 0
    if pos < 170:
        pos -= 85
        return 0, int(255 - pos * 3), int(pos * 3)
    pos -= 170
    return int(pos * 3), 0, int(255 - (pos * 3))


    while True:
    for i in range(255):
        for pixie in range(num_pixies):
            pixies[pixie] = wheel(i)
        pixies.show()

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_pixie/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
