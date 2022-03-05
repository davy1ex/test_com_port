import sys
import glob
import serial
from serial.tools import list_ports


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        # ports = ['COM%s' % (i + 1) for i in range(256)]
        ports = serial.tools.list_ports.comports()
        print(len(ports))
        for p in ports:
            print(p.device)
        # print("oh, this is winddow: ", list_ports.comports())
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    # result = []
    # for port in ports:
    #     try:
    #         s = serial.Serial(port)
    #         s.close()
    #         result.append(port)
    #         # print("port {}: success connect".format(port))
    #     except serial.serialutil.SerialException:
    #         print("gg")
    #         exit()
    return result


if __name__ == '__main__':
    print(serial_ports())