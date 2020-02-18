# By Vorono4ka (https://vk.com/vorono4ka_id0_id1_id228_id1488)

from io import BufferedReader, BytesIO
from struct import *
import os


class Reader(BufferedReader):
    def __init__(self, initial_bytes):
        super().__init__(BytesIO(initial_bytes))

    def readInteger(self, length: int = 1):
        return int.from_bytes(self.read(length), 'big', signed=True)

    def readUInt32(self):
        return unpack('>I', self.read(4))[0]

    def readString(self):
        return self.read(self.readInteger(2)).decode('utf-8')

    def readUShort(self):
        return unpack('>H', self.read(2))[0]

    def readShort(self):
        return unpack('>h', self.read(2))[0]

    def readFloat(self):
        return unpack('>f', self.read(4))[0]

    def readUByte(self):
        return unpack('>B', self.read(1))[0]

    def readVertex(self):
        vertex = []
        self.readString()
        self.readUByte()  # index
        self.readUShort()
        scale = self.readFloat()
        count = self.readUInt32()
        for x1 in range(count):
            vertex.append([self.readShort() / 32767 * scale, self.readShort() / 32767 * scale, self.readShort() / 32767 * scale])
        return vertex

    def readTexCoord(self):
        vertex = []
        self.readUByte()  # index
        self.readUShort()
        scale = self.readFloat()
        count = self.readUInt32()
        for x1 in range(count):
            vertex.append([self.readShort() / 32512 * scale, 1-self.readShort() / 32512 * scale])
        return vertex

    def readColor(self):
        vertex = []
        self.readUByte()  # index
        vertex_shorts = self.readUShort()
        scale = self.readFloat()
        count = self.readUInt32()
        for x1 in range(count):
            for x2 in range(vertex_shorts):
                vertex.append(self.readShort() / 32512 * scale)
        return vertex


class Struct(Reader):
    def __init__(self, filename):
        path = f'scw/{filename}'
        data = open(path, 'rb').read()
        reader, chunks, i = Reader(data), [], 0
        reader.read(4)
        while i < len(data) and data[i + 8:i + 12] != b'WEND':
            chunklen = reader.readInteger(4) + 8
            chunks.append(reader.read(chunklen))
            i += chunklen + 4
        for chunk in chunks:
            cr = Reader(chunk)  # chunkreader
            if cr.read(4) == b'GEOM':
                name = cr.readString()
                group = cr.readString()
                if not os.path.isdir(f'obj/{filename[:-4]}'):
                    os.mkdir(f'obj/{filename[:-4]}')
                if not os.path.isdir(f'obj/{filename[:-4]}/{group}'):
                    os.mkdir(f'obj/{filename[:-4]}/{group}')
                path = f'obj/{filename[:-4]}/{group}/{name}.obj'
                obj = open(path, 'w')
                vertex_count = cr.readUByte()
                if vertex_count > 0:
                    vertex = cr.readVertex()
                    obj.write(''.join([f'v {" ".join([str(y) for y in x])}\n' for x in vertex]))
                if vertex_count > 1:
                    vertex = cr.readVertex()
                    obj.write(''.join([f'vn {" ".join([str(y) for y in x])}\n' for x in vertex]))
                if vertex_count > 2:
                    if cr.readString() == 'TEXCOORD':
                        vertex = cr.readTexCoord()
                        obj.write(''.join([f'vt {" ".join([str(y) for y in x])}\n' for x in vertex]))
                    else:
                        cr.readColor()
                if vertex_count > 3:
                    if cr.readString() == 'TEXCOORD':
                        vertex = cr.readTexCoord()
                        print(len(vertex))
                        obj.write(''.join([f'vt {" ".join([str(y) for y in x])}\n' for x in vertex]))
                    else:
                        cr.readColor()
                if vertex_count > 4:
                    if cr.readString() == 'TEXCOORD':
                        vertex = cr.readTexCoord()
                        obj.write(''.join([f'vt {" ".join([str(y) for y in x])}\n' for x in vertex]))
                    else:
                        cr.readColor()
                if cr.readUByte() == 1:
                    cr.read(64)
                for x in range(cr.readUByte()):
                    cr.readString()
                    cr.read(64)
                for x in range(cr.readUInt32()):
                    cr.read(12)
                for x in range(cr.readUByte()):
                    obj.write(f'\no {name}_cms\n\n')
                    cr.readString()
                    cr.readString()
                    count = cr.readUShort()
                    mode1 = cr.readUByte()
                    mode2 = cr.readUByte()
                    for x1 in range(count):
                        poly = []
                        for x2 in range(3):
                            if mode1 > 0:
                                v = f'{cr.readUShort() + 1}' if mode2 == 2 else f'{cr.readUByte() + 1}'
                                if mode1 > 1:
                                    vn = f'{cr.readUShort() + 1}' if mode2 == 2 else f'{cr.readUByte() + 1}'
                                else:
                                    vn = v
                                if mode1 > 2:
                                    vt = f'{cr.readUShort() + 1}' if mode2 == 2 else f'{cr.readUByte() + 1}'
                                else:
                                    vt = vn
                                if mode1 > 3:
                                    vt = f'{cr.readUShort() + 1}' if mode2 == 2 else f'{cr.readUByte() + 1}'
                                else:
                                    vt = vn
                                poly.append(f'{v}/{vt}/{vn}')
                        obj.write(f'f {" ".join(poly)}\n')


if not os.path.isdir('scw/'):
    os.mkdir('scw')

if not os.path.isdir('obj/'):
    os.mkdir('obj/')

for filename in os.listdir('scw/'):
    modeldata = Struct(filename)


# By Vorono4ka (https://vk.com/vorono4ka_id0_id1_id228_id1488)
