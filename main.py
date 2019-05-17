from pyftdi.i2c import I2cController


if __name__ == '__main__':
    i2c = I2cController()
    i2c.configure('ftdi:///?')
