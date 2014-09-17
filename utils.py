import logging
import socket
import fcntl
import struct

LOG = logging.getLogger(__name__)


def fmt_print(msg):
    fmt = ' ' * 10
    print '%s%s' % (fmt, msg)


def fmt_msg(msg):
    fmt = ' ' * 10
    return '%s%s' % (fmt, msg)


def valid_print(key, value):
    fmt_print('%-40s: %s' % (key, value))


def check_ip(value):
    try:
        if len(value.split('.')) != 4:
            return False
        for i in value.split('.'):
            if int(i) < 0 or int(i) > 255:
                return False
    except:
        return False
    return True


def ask_user(promtp, accept_value=None, default_val=None, err_promtp=None,
             check=None):
    """ ask user, then get a config value, note: accept must be lower case """
    while True:
        value = raw_input(fmt_msg(promtp))

        if value:
            # if value is not null and not acceptable, ignore
            if accept_value and value.lower() not in accept_value:
                if err_promtp:
                    fmt_print(err_promtp)
                else:
                    fmt_print('you must input one of %s' % str(accept_value))
                continue
        else:
            # if value is null and there is no default value, ignore
            if not default_val:
                continue
            else:
                value = default_val
        # if it is running here, it indicate that we get a acceptable value
        if check and not check(value):
            if err_promtp:
                LOG.warn(err_promtp)
            else:
                LOG.warn('invalid input')
            continue

        return value


def get_hwaddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ''.join(['%02x:' % ord(char) for char in info[18:24]])[:-1]
