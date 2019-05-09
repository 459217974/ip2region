import socket
import struct

cdef int INDEX_BLOCK_LENGTH = 12
cdef int TOTAL_HEADER_LENGTH = 8192
cdef unsigned int INDEX_S_PTR
cdef unsigned int INDEX_L_PTR
cdef unsigned int INDEX_COUNT

cdef unsigned int get_long(bytes b, int offset):
    _ = b[offset:offset + 4]
    if len(_) == 4:
        return struct.unpack('I', _)[0]
    return 0


cdef unsigned int ip2int(ip_str):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(ip_str))[0])

class IP2Region(object):

    def __init__(self):
        global INDEX_BLOCK_LENGTH
        global INDEX_S_PTR
        global INDEX_L_PTR
        global INDEX_COUNT
        with open('ip2region.db', 'rb') as f:
            self.db = f.read()
        INDEX_S_PTR = get_long(self.db, 0)
        INDEX_L_PTR = get_long(self.db, 4)
        INDEX_COUNT = int((INDEX_L_PTR - INDEX_S_PTR) / INDEX_BLOCK_LENGTH) + 1

    def return_data(self, int data_ptr):
        data_len = (data_ptr >> 24) & 0xFF
        data_ptr = data_ptr & 0x00FFFFFF
        data = self.db[data_ptr:data_ptr + data_len]
        return {
            "city_id": get_long(data, 0),
            "region": data[4:].decode()
        }

    def search(self, ip):
        global INDEX_BLOCK_LENGTH
        global INDEX_S_PTR
        global INDEX_COUNT
        cdef int l, h, data_ptr, m, p
        cdef unsigned int ip_int, sip, eip
        ip_int = ip2int(ip)
        l = 0
        h = INDEX_COUNT
        data_ptr = 0
        while l <= h:
            m = (l + h) >> 1
            p = INDEX_S_PTR + m * INDEX_BLOCK_LENGTH
            sip = get_long(self.db, p)

            if ip_int < sip:
                h = m - 1
            else:
                eip = get_long(self.db, p + 4)
                if ip_int > eip:
                    l = m + 1
                else:
                    data_ptr = get_long(self.db, p + 8)
                    break

        if data_ptr == 0:
            raise ValueError('Data pointer not found')

        return self.return_data(data_ptr)
