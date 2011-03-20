

class privatar():

    def xor_md5s (self, md5a, md5b ) :
        """Return the XOR result of the inputs"""
        return "%032x" % ( int(md5a, 16) ^ int(md5b, 16) )